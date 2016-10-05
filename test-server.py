from flask import Flask, request, redirect, Response, jsonify, url_for
import requests
import os
from slackclient import SlackClient

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
TOKEN = os.environ.get('BOT_TOKEN')
slack_client = SlackClient(TOKEN)

app = Flask(__name__)
app.secret_key = "ABC123"  # For example only

def winner(entryPositionNames):
    """If there is a winner, the function will return true."""

    # top row
    if ((entryPositionNames.get('top-left') != " ") and
        entryPositionNames.get('top-left') ==
        entryPositionNames.get('top-middle') ==
            entryPositionNames.get('top-right')):
        return True

    # middle row
    if ((entryPositionNames.get('middle-left') != " ") and
        entryPositionNames.get('middle-left') ==
        entryPositionNames.get('middle') ==
            entryPositionNames.get('middle-right')):
        return True

    # bottom row
    if ((entryPositionNames.get('bottom-left') != " ") and
        entryPositionNames.get('bottom-left') ==
        entryPositionNames.get('bottom-middle') ==
            entryPositionNames.get('bottom-right')):
        return True

    # left
    if ((entryPositionNames.get('top-left') != " ") and
        entryPositionNames.get('top-left') ==
        entryPositionNames.get('middle-left') ==
            entryPositionNames.get('bottom-left')):
        return True

    # middle
    if ((entryPositionNames.get('top-middle') != " ") and
        entryPositionNames.get('top-middle') ==
        entryPositionNames.get('middle') ==
            entryPositionNames.get('bottom-middle')):
        return True

    # right
    if ((entryPositionNames.get('top-right') != " ") and
        entryPositionNames.get('top-right') ==
        entryPositionNames.get('middle-right') ==
            entryPositionNames.get('bottom-right')):
        return True

    # diagonals
    if ((entryPositionNames.get('top-left') != " ") and
        entryPositionNames.get('top-left') ==
        entryPositionNames.get('middle') ==
            entryPositionNames.get('bottom-right')):
        return True

    if ((entryPositionNames.get('top-right') != " ") and
        entryPositionNames.get('top-right') ==
        entryPositionNames.get('middle') ==
            entryPositionNames.get('bottom-left')):
        return True

    else:
        return False

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
        channel_id = request.form.get('channel_id')

        if currentState.get('creator') == currentState.get('invited_user_name'):
            return jsonify({
                'response_type': 'in_channel',
                'text': "You cannot invite yourself to play! Try inviting someone else."
                })

        message = "@%s wants to play tic-tac-toe with @%s. @%s, do you want to /accept or /decline?" % \
                  (currentState['creator'], currentState['invited_user_name'], currentState['invited_user_name'])

        return jsonify({
            'response_type': 'in_channel',
            'text': message
            })

    else:
        message = "A game is already in session between @%s and @%s. To see the current game," \
                  "enter '/board'" % (currentState['creator'], currentState['invited_user_name'])
        return jsonify({
            'response_type': 'in_channel',
            'text': message
            })


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
            message = "A game is already in session between @%s and @%s. To see the current game," \
                "enter '/board'" % (currentState['creator'], currentState['invited_user_name'])
            return jsonify({
                'response_type': 'in_channel',
                'text': message
                })

        currentState["in_progress"] = True
        channel_id = request.form.get('channel_id')

        return redirect(url_for('board', channel_id=channel_id))

    else:
        message = "You do not have permission to do this at this time."
        return jsonify({
            'response_type': 'in_channel',
            'text': message
            })


@app.route('/decline', methods=["POST"])
def decline():
    current_channel = request.form.get("channel_id")
    if current_channel == currentState.get('channel_id'):
        declined = request.form.get('user_name')

        if currentState.get('invited_user_name', "") == declined and currentState.get("in_progress", "") == False:
            message = "@%s has declined the game." % currentState['invited_user_name']
            return jsonify({
                'response_type': 'in_channel',
                'text': message
                })
        else:
            message = "You do not have permission to do this at this time."
            return jsonify({
                'response_type': 'in_channel',
                'text': message
                })

    else:
        message = "You do not have permission to do this at this time."
        return jsonify({
            'response_type': 'in_channel',
            'text': message
            })


@app.route('/board')
def board():
    current_channel = request.form.get("channel_id")
    if current_channel == currentState.get('channel_id') and currentState.get('in_progress', "") == True:
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
            slack_client.api_call("chat.postMessage", channel=channel_id, text=message, username='tic-tac-toe', icon_emoji=':robot_face:')

            # if there is a winner, end game
            if currentState.get('winner', "") == True:
                # refreshing necessary currentState keys
                for key in entryPositionNames.keys():
                    entryPositionNames[key] = " "

                currentState['in_progress'] = False
                currentState['winner'] = False
                currentState['channel_id'] = " "
                currentState['players'] = {}
                currentState['accepted_invite'] = False

                return jsonify({
                    'response_type': 'in_channel',
                    'text': ("Game over. @%s wins!" % (currentState['current_player']))
                    })

            # if board is full but no winners:
            if currentState.get('winner', "") == False:
                for value in entryPositionNames.values():
                    if value == " ":
                        #if there are still spaces available, continue
                        channel_id = request.form.get('channel_id')

                        return jsonify({
                            'response_type': 'in_channel',
                            'text': ("It is @%s's turn !" % (currentState['current_player']))
                            })

                # when the game ends in a draw:
                currentState['in_progress'] = False

                return jsonify({
                    'response_type': 'in_channel',
                    'text': "Game over. It's a draw!"
                    })

    else:
        message = "You do not have permission to do this at this time."
        return jsonify({
            'response_type': 'in_channel',
            'text': message
            })

@app.route('/move', methods=["POST"])
def move():
    current_channel = request.form.get("channel_id")
    if (current_channel == currentState.get('channel_id')) and (currentState.get('accepted_invite') == True):
        #MUST MAKE SURE THEY ACCEPT THE GAME FIRST
        person_submitted = str(request.form.get('user_name'))
        current = currentState.get('current_player', "")
        channel_id = request.form.get('channel_id')

        if current == person_submitted:
            position = " "
            inputPosition = request.form.get('text')
            if inputPosition:
                position = inputPosition

            # check if position is valid and it doesnt have a value
            if position in entryPositionNames:
                currentPositionEntry = entryPositionNames.get(position, "")
                if currentPositionEntry != " ":
                    message = "This square is already taken. Please choose another."

                    return jsonify({
                        'response_type': 'in_channel',
                        'text': message
                        })

                else:
                    #### username = currentState['players'][person_submitted]['user_name']
                    current_letter = currentState['players'][person_submitted]['letter']
                    entryPositionNames[position] = current_letter

                    # checks if the move constitues a win
                    if winner(entryPositionNames):
                        currentState['winner'] = True

                        return redirect(url_for('board', channel_id=channel_id))

                    if currentState.get('current_player') == currentState['creator']:
                        currentState['current_player'] = currentState['invited_user_name']
                    else:
                        currentState['current_player'] = currentState['creator']

                    return redirect(url_for('board', channel_id=channel_id))

            else:
                #if wrong move, list out available move
                available_moves = []
                for key in entryPositionNames.keys():
                    available_moves.append(key)

                available_moves.sort()

                message = "Please enter a valid move: %s." % (", ".join(available_moves))
                return jsonify({
                    'response_type': 'in_channel',
                    'text': message
                    })

        else:
            message = "Players make a move by entering /move [position]."
            return jsonify({
                'response_type': 'in_channel',
                'text': message
                })

    else:
        return "You do not have permission to do this at this time."


@app.route('/end_game')
def end():
    current_channel = request.form.get("channel_id")
    if current_channel == currentState.get('channel_id'):
        # if user is creator or invited
        if currentState.get('in_progress', "") == True:
            currentState['in_progress'] = False
            for key in entryPositionNames.keys():
                entryPositionNames[key] = " "

            message = "The game has ended."
            return jsonify({
                'response_type': 'in_channel',
                'text': message
                })

        else:
            message = "You do not have permission to do this at this time."
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
