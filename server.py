from flask import Flask, request, redirect, jsonify, url_for
import helper
import os
from slackclient import SlackClient
from slacker import Slacker

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
TOKEN = os.environ.get('BOT_TOKEN')
slack_client = SlackClient(TOKEN)
slacker = Slacker(TOKEN)

app = Flask(__name__)
app.secret_key = "ABC123"  # For example only

channels = {}


@app.route('/', methods=["POST"])
def state():
    """Inviting someone to play a game."""

    channel_id = str(request.form.get('channel_id'))

    if channel_id not in channels.keys():
        channels[channel_id] = helper.new_state(channels, channel_id)

    if channels.get(channel_id, "").get("in_progress") == False:
        user_id = request.form.get('user_id')
        # needed to convert to string to prevent saving user_name as type_unicode
        user_name = str(request.form.get('user_name'))
        invited_player = request.form.get('text')

        if not invited_player:
            return "Please invite someone to play with."

        in_channel = channels[channel_id]
        in_channel['creator'] = user_name
        in_channel['invited_user_name'] = invited_player[1:]
        in_channel['players'][user_name] = {
            "user_name": user_name,
            "user_id": user_id,
            "letter": "X"
        }

        response = slacker.users.list()
        r = response.body['members']

        existing_users = []
        for i in r:
            for key, value in i.iteritems():
                if key == "name":
                    existing_users.append(value)

        # inviting yourself
        if (channels.get(channel_id).get("creator") ==
            channels.get(channel_id).get('invited_user_name')):
            return "You cannot invite yourself to play."

        # inviting someone non-existent in team
        if channels.get(channel_id).get('invited_user_name') not in existing_users:
            return "That username does not exists."

        message = "@%s wants to play Tic-Tac-Toe with @%s. @%s, do you want to /ttt-accept or /ttt-decline?" % \
                  (in_channel['creator'], in_channel['invited_user_name'], in_channel['invited_user_name'])

        return jsonify({
            'response_type': 'in_channel',
            'text': message
            })

    else:
        return "A game is already in session between @%s and @%s. To see the current game," \
               "enter '/ttt-board'" % (channels[channel_id]['creator'], channels[channel_id]['invited_user_name'])


@app.route('/accept', methods=["POST"])
def accept_invite():
    """Accepting the game invitation."""

    current_channel = request.form.get("channel_id")

    if current_channel in channels.keys():

        in_channel = channels[current_channel]
        if channels.get(current_channel, "").get("in_progress") == True:
            return "A game is already in session between @%s and @%s. To see the current game," \
                "enter '/ttt-board'" % (in_channel['creator'], in_channel['invited_user_name'])

        user_id2 = request.form.get('user_id')
        user_name2 = str(request.form.get('user_name'))
        in_channel['current_player'] = user_name2
        in_channel['players'][user_name2] = {
            "user_name": user_name2,
            "user_id": user_id2,
            "letter": "O"
        }

        in_channel['in_progress'] = True
        in_channel['accepted_invite'] = True

        message = "To see available commands, enter /ttt-help."
        slack_client.api_call("chat.postMessage", channel=current_channel,
                              text=message, username='Tic-Tac-Toe', icon_emoji=':ttt:')

        return redirect(url_for('board', channel_id=current_channel))

    else:
        return "You do not have permission to do this at this time."


@app.route('/decline', methods=["POST"])
def decline():
    """Declining the game invitation."""

    current_channel = request.form.get("channel_id")
    if current_channel in channels.keys():
        declined = request.form.get('user_name')

        if (channels.get(current_channel, "").get('invited_user_name') ==
                declined and channels.get(current_channel, "").get("in_progress") == False):
            message = "@%s has declined the game." % channels[current_channel]['invited_user_name']

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
    """Displaying tic-tac-toe board."""

    current_channel = request.args.get("channel_id")
    if (current_channel in channels.keys() and
            channels.get(current_channel, " ").get('in_progress') == True):

            in_channel = channels[current_channel]

            message = "```| %s | %s | %s |\n|---+---+---|\n| %s | %s | %s |\n|---+---+---|\n| %s | %s | %s |\n```" \
                % (in_channel['top-left'],
                   in_channel['top-middle'],
                   in_channel['top-right'],
                   in_channel['middle-left'],
                   in_channel['middle'],
                   in_channel['middle-right'],
                   in_channel['bottom-left'],
                   in_channel['bottom-middle'],
                   in_channel['bottom-right'])

            slack_client.api_call("chat.postMessage", channel=current_channel,
                                  text=message, username='Tic-Tac-Toe', icon_emoji=':ttt:')

            in_channel = channels[current_channel]
            # if there is a winner, end game
            if channels.get(current_channel, " ").get('winner') == True:
                # refreshing all necessary dict keys
                helper.restart_board(channels, current_channel)

                return jsonify({
                    'response_type': 'in_channel',
                    'text': ("Game over. @%s wins!" % (in_channel['current_player']))
                    })

            # if board is/is not full but no winners:
            if channels.get(current_channel, " ").get('winner') == False:
                for value in in_channel.values():
                    if value == " ":

                        # if there are still spaces available, return turn. We can check
                        # for " " like this because all values with " " at this point
                        # are all square positions.

                        return jsonify({
                            'response_type': 'in_channel',
                            'text': ("It is @%s's turn!" % (in_channel['current_player']))
                            })

                # when the game ends in a draw:
                helper.restart_board(channels, current_channel)

                return jsonify({
                    'response_type': 'in_channel',
                    'text': "Game over. It's a draw!"
                    })

    else:
        return "You do not have permission to do this at this time."


@app.route('/move', methods=["POST"])
def move():
    """Placing a letter on a square."""

    current_channel = request.form.get("channel_id")
    if ((current_channel in channels.keys()) and
            (channels.get(current_channel, "").get('accepted_invite') == True)):

        person_submitted = str(request.form.get('user_name'))
        in_channel = channels[current_channel]
        current = in_channel.get('current_player')

        if current == person_submitted:
            position = " "

            # if player submits a text stating a move
            input_position = request.form.get('text')
            if input_position:
                position = input_position

            # check if position is valid
            if position in in_channel.keys():
                current_entry = channels.get(current_channel).get(position)
                # when a square is taken
                if current_entry != " ":
                    return "This square is already taken. Please choose another."

                # choosing an empty square
                else:
                    current_letter = in_channel['players'][person_submitted]['letter']
                    in_channel[position] = current_letter

                    # checks if the move constitues a win
                    if helper.winner(channels, current_channel):
                        in_channel['winner'] = True

                        return redirect(url_for('board', channel_id=current_channel))

                    # switching between current player and other player
                    if channels.get(current_channel).get('current_player') == in_channel['creator']:
                        in_channel['current_player'] = in_channel['invited_user_name']

                    else:
                        in_channel['current_player'] = in_channel['creator']

                    return redirect(url_for('board', channel_id=current_channel))

            else:
                # if it is a wrong move, valid moves are listed out

                return "Please enter a valid move: 'top-left', 'top-middle', " \
                       "top-right', 'middle-left', 'middle', 'middle-right', " \
                       "'bottom-left', 'bottom-middle', 'bottom-right'."

        else:
            return "Players make a move by entering /ttt-move [position]."

    else:
        return "You do not have permission to do this at this time."


@app.route('/more_help')
def help():
    """Displays slash command descriptions."""

    return ("/ttt [@username] -- Invite a person to play Tic-Tac-Toe.\n"
            "/ttt-accept -- Accept the game invitation.\n"
            "/ttt-decline -- Decline the game invitation.\n"
            "/ttt-board -- View the game board.\n"
            "/ttt-move [position] -- Place a letter on an empty square. Positions include"
            "'top-left', 'top-middle', 'top-right', 'middle-left', 'middle-right',"
            "'bottom-left', 'bottom-middle', 'bottom-right'.\n"
            "/ttt-end -- End the game.\n\n"
            "Check out https://en.wikipedia.org/wiki/Tic-tac-toe for more information.")


@app.route('/end_game', methods=["POST"])
def end():
    """Ends game."""

    current_channel = request.form.get("channel_id")
    if (current_channel in channels.keys() and
            channels.get(current_channel, "").get('in_progress') == True):

        helper.restart_board(channels, current_channel)

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
