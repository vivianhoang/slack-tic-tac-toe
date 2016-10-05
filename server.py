from flask import Flask, request, redirect, jsonify, url_for
from helper import restart_board
import os
from slackclient import SlackClient

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
TOKEN = os.environ.get('BOT_TOKEN')
slack_client = SlackClient(TOKEN)

app = Flask(__name__)
app.secret_key = "ABC123"  # For example only

channels = {}

entryPositionNames = {
    'top-left': " ",
    'top-middle': " ",
    'top-right': " ",
    'middle-left': " ",
    'middle': " ",
    'middle-right': " ",
    'bottom-left': " ",
    'bottom-middle': " ",
    'bottom-right': " ",
}

currentState = {
    "in_progress": False,
    "creator": " ",
    "invited_user_name": " ",
    "accepted_invite": False,
    "players": {},
    "current_player": " ",
    "winner": False,
    "channel_id": "",
}

# need to make sure I validate keys AND TEAM/CHANNEL ID or one game throughout whole slack test group


@app.route('/', methods=["POST"])
def state():
    channel_id = request.form.get('channel_id')
    currentState['channel_id'] = channel_id

    if currentState.get("in_progress") == False:
        user_id = request.form.get('user_id')
        # needed to convert to string to prevent saving user_name as type_unicode
        user_name = str(request.form.get('user_name'))
        invited_player = request.form.get('text')
        currentState['creator'] = user_name
        currentState['invited_user_name'] = invited_player[1:]
        currentState['players'][user_name] = {
            "user_name": user_name,
            "user_id": user_id,
            "letter": "X"
        }

        if currentState.get('creator') == currentState.get('invited_user_name'):
            return "You cannot invite yourself to play. You can invite another team member to play."

        message = "@%s wants to play Tic-Tac-Toe with @%s. @%s, do you want to /ttt-accept or /ttt-decline?" % \
                  (currentState['creator'], currentState['invited_user_name'], currentState['invited_user_name'])

        return jsonify({
            'response_type': 'in_channel',
            'text': message
            })

    else:
        return "A game is already in session between @%s and @%s. To see the current game," \
               "enter '/ttt-board'" % (currentState['creator'], currentState['invited_user_name'])


@app.route('/accept', methods=["POST"])
def accept_invite():
    current_channel = request.form.get("channel_id")

    if current_channel == currentState.get('channel_id'):

        user_id2 = request.form.get('user_id')
        user_name2 = str(request.form.get('user_name'))
        currentState['current_player'] = user_name2
        currentState['players'][user_name2] = {
            "user_name": user_name2,
            "user_id": user_id2,
            "letter": "O"
        }

        if currentState.get("in_progress","") == True:
            return "A game is already in session between @%s and @%s. To see the current game," \
                "enter '/ttt-board'" % (currentState['creator'], currentState['invited_user_name'])

        currentState['in_progress'] = True
        currentState['accepted_invite'] = True

        message = "To see available commands, enter /ttt-help."
        slack_client.api_call("chat.postMessage", channel=current_channel, text=message, username='Tic-Tac-Toe', icon_emoji=':robot_face:')

        return redirect(url_for('board', channel_id=current_channel))

    else:
        return "You do not have permission to do this at this time."


@app.route('/decline', methods=["POST"])
def decline():
    current_channel = request.form.get("channel_id")
    if current_channel == currentState.get('channel_id'):
        declined = request.form.get('user_name')

        if currentState.get('invited_user_name') == declined and currentState.get("in_progress") == False:
            message = "@%s has declined the game." % currentState['invited_user_name']
            return jsonify({
                'response_type': 'in_channel',
                'text': message
                })
        else:
            return "You do not have permission to do this at this time."

    else:
        return "You do not have permission to do this at this time."


@app.route('/board')
def board():
    current_channel = request.args.get("channel_id")
    if current_channel == currentState.get('channel_id') and currentState.get('in_progress') == True:
            message = "```| %s | %s | %s |\n|---+---+---|\n| %s | %s | %s |\n|---+---+---|\n| %s | %s | %s |\n```" \
                % (entryPositionNames['top-left'],
                   entryPositionNames['top-middle'],
                   entryPositionNames['top-right'],
                   entryPositionNames['middle-left'],
                   entryPositionNames['middle'],
                   entryPositionNames['middle-right'],
                   entryPositionNames['bottom-left'],
                   entryPositionNames['bottom-middle'],
                   entryPositionNames['bottom-right'])

            channel_id = request.args.get('channel_id')
            slack_client.api_call("chat.postMessage", channel=channel_id, text=message, username='Tic-Tac-Toe', icon_emoji=':robot_face:')

            # if there is a winner, end game
            if currentState.get('winner') == True:
                # refreshing necessary currentState keys
                for key in entryPositionNames.keys():
                    entryPositionNames[key] = " "

                restart_board()

                return jsonify({
                    'response_type': 'in_channel',
                    'text': ("Game over. @%s wins!" % (currentState['current_player']))
                    })

            # if board is full but no winners:
            if currentState.get('winner') == False:
                for value in entryPositionNames.values():
                    if value == " ":
                        #if there are still spaces available, continue
                        channel_id = request.form.get('channel_id')

                        return jsonify({
                            'response_type': 'in_channel',
                            'text': ("It is @%s's turn!" % (currentState['current_player']))
                            })

                # when the game ends in a draw:
                restart_board()

                return jsonify({
                    'response_type': 'in_channel',
                    'text': "Game over. It's a draw!"
                    })

    else:
        return "You do not have permission to do this at this time."


@app.route('/move', methods=["POST"])
def move():
    current_channel = request.form.get("channel_id")
    if (current_channel == currentState.get('channel_id')) and (currentState.get('accepted_invite') == True):
        person_submitted = str(request.form.get('user_name'))
        current = currentState.get('current_player')

        if current == person_submitted:
            position = " "

            # if player submits a text stating a move
            input_position = request.form.get('text')
            if input_position:
                position = input_position

            # check if position is valid
            if position in entryPositionNames:
                currentPositionEntry = entryPositionNames.get(position)
                # when a square is taken
                if currentPositionEntry != " ":
                    return "This square is already taken. Please choose another."

                # choosing an empty square
                else:
                    current_letter = currentState['players'][person_submitted]['letter']
                    entryPositionNames[position] = current_letter

                    # checks if the move constitues a win
                    if winner(entryPositionNames):
                        currentState['winner'] = True

                        return redirect(url_for('board', channel_id=current_channel))

                    # switching between current player and other player
                    if currentState.get('current_player') == currentState['creator']:
                        currentState['current_player'] = currentState['invited_user_name']

                    else:
                        currentState['current_player'] = currentState['creator']

                    return redirect(url_for('board', channel_id=current_channel))

            else:
                # if it is a wrong move, valid moves are listed out
                valid_moves = []
                for key in entryPositionNames.keys():
                    available_moves.append(key)

                valid_moves.sort()

                return "Please enter a valid move: %s." % (", ".join(valid_moves))

        else:
            return "Players make a move by entering /ttt-move [position]."

    else:
        return "You do not have permission to do this at this time."


@app.route('/more_help')
def help():
    """ """
    print "I am groot"
    return ("/ttt [@username] -- Invite a person to play Tic-Tac-Toe.\n"
            "/ttt-accept -- Accept the game invitation.\n"
            "/ttt-decline -- Decline the game invitation.\n"
            "/ttt-board -- View the game board.\n"
            "/ttt-move [position] -- Place a letter on an empty square. Positions include"
            "'top-left', 'top-middle', 'top-right', 'middle-left', 'middle-right',"
            "'bottom-left', 'bottom-middle', 'bottom-right'.\n"
            "/ttt-end -- End the game.")


@app.route('/end_game', methods=["POST"])
def end():
    """ """
    current_channel = request.form.get("channel_id")
    if current_channel == currentState.get('channel_id') and currentState.get('in_progress') == True:
        for key in entryPositionNames.keys():
            entryPositionNames[key] = " "

        restart_board()

        message = "The game has ended."
        return jsonify({
            'response_type': 'in_channel',
            'text': message
            })

    else:
        return "You do not have permission to do this at this time."

if __name__ == '__main__':


    DEBUG = "NO_DEBUG" not in os.environ
    PORT = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
