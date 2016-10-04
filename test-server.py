# from flask import Flask, requests
# from flask_restful import Resource, Api

# app = Flask(__name__)
# api = Api(app)

# todos = {}

# class TodoSimple(Resource):
#     def get(self, todo_id):
#         return {todo_id: todos[todo_id]}

#     def put(self, todo_id):
#         todos[todo_id] = request.form['data']
#         return {todo_id: todos[todo_id]}

# api.add_resource(TodoSimple, '/<string:todo_id>')

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, redirect, Response, jsonify
# from helper import winner
import requests
import os
from slackclient import SlackClient

SLACK_TOKEN = os.environ['SLACK_TOKEN']
TOKEN = os.environ['BOT_TOKEN']
slack_client = SlackClient(TOKEN)

app = Flask(__name__)
app.secret_key = "ABC123"  # For example only

def winner(entryPositionNames):
    """If there is a winner, the function will return true."""

    # top row
    if ((entryPositionNames.get('top-left') != "    ") and
        entryPositionNames.get('top-left') ==
        entryPositionNames.get('top-middle') ==
            entryPositionNames.get('top-right')):
        return True

    # middle row
    if ((entryPositionNames.get('middle-left') != "    ") and
        entryPositionNames.get('middle-left') ==
        entryPositionNames.get('middle') ==
            entryPositionNames.get('middle-right')):
        return True

    # bottom row
    if ((entryPositionNames.get('bottom-left') != "    ") and
        entryPositionNames.get('bottom-left') ==
        entryPositionNames.get('bottom-middle') ==
            entryPositionNames.get('bottom-right')):
        return True

    # diagonals
    if ((entryPositionNames.get('top-left') != "    ") and
        entryPositionNames.get('top-left') ==
        entryPositionNames.get('middle') ==
            entryPositionNames.get('bottom-right')):
        return True

    if ((entryPositionNames.get('top-right') != "    ") and
        entryPositionNames.get('top-right') ==
        entryPositionNames.get('middle') ==
            entryPositionNames.get('bottom-left')):
        return True

    else:
        return False

entryPositionNames = {
    'top-left': "    ",
    'top-middle': "    ",
    'top-right': "    ",
    'middle-left': "    ",
    'middle': "    ",
    'middle-right': "    ",
    'bottom-left': "    ",
    'bottom-middle': "    ",
    'bottom-right': "    ",
}

currentState = {
    "in_progress": False,
    "creator": " ",
    "invited_user_name": " ",
    "accepted_invite": False,
    "players": {},
    "current_player": " ",
    "winner": False,
    "squares_available": True,
}

# def send_message(channel_id, message):
#     slack_client.api_call(
#         "chat.postMessage",
#         channel=channel_id,
#         text=message,
#         username='tic-tac-toe',
#         icon_emoji=':robot_face'
#     )


# need to make sure I validate keys AND TEAM/CHANNEL ID or one game throughout whole slack test group

@app.route('/', methods=["POST"])
def state():
    if currentState.get("in_progress","") == False:
        user_id = request.form.get('user_id')
        user_name = str(request.form.get('user_name'))
        invited_player = request.form.get('text')
        # channel_name = request.form.get('channel_name')
        currentState['creator'] = user_name
        currentState['invited_user_name'] = invited_player
        currentState['players'][user_name] = {
            "user_name": user_name,
            "user_id": user_id,
            "letter": "X"
        }
        # channel_id = request.form.get('channel_id')
        message = "@%s wants to play tic-tac-toe with %s. %s, do you want to /accept or /decline?" % (user_name, invited_player, invited_player)

        print "1 ", currentState['players']

        # r = requests.post('https://hooks.slack.com/services/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', json={"text": "%s wants to play tic-tac-toe with %s." % (user_name, invited_player),
        #                       "attachments": [
        #                      {"text": "%s, do you /accept or /decline?" % (invited_player)}
        #                 ]})

        # slack_client.api_call("chat.postMessage", channel=channel_id, text='lol', username='tic-tac-toe', icon_emoji=':robot_face:')
        return jsonify({
            'response_type': 'in_channel',
            'text': message
            })
        # return send_message(channel_id, message)
        # return response.send({"response_type": "in_channel",
        #                       "text": "%s wants to play tic-tac-toe with %s." % (user_name, invited_player),
        #                       "attachments": [
        #                      {"text": "%s, do you /accept or /decline?" % (invited_player)}
        #                 ]
        #             })

    else:
        message = "A game is already in session between %s and %s. To see the current game," \
            "enter '/board'" % (currentState['creator'], currentState['invited_user_name'])
        return jsonify({
            'response_type': 'in_channel',
            'text': message
            })
        # return "A game is already in session between %s and %s. To see the current game," \
        #     "enter '/board'" % (currentState['creator'], currentState['invited_user_name'])


@app.route('/accept', methods=["POST"])
def accept_invite():
    user_id2 = request.form.get('user_id')
    user_name2 = str(request.form.get('user_name'))
    currentState['current_player'] = user_name2
    print "hello", currentState.get('current_player', "")
    currentState['players'][user_name2] = {
        "user_name": user_name2,
        "user_id": user_id2,
        "letter": "O"
    }
    # user_name2 = '@' + user_name2

    if currentState.get("in_progress","") == True:
        message = "A game is already in session between %s and %s. To see the current game," \
            "enter '/board'" % (currentState['creator'], currentState['invited_user_name'])
        return jsonify({
            'response_type': 'in_channel',
            'text': message
            })
        # return "There is already a game in progress between %s and %s." % (user_name2, currentState['creator'])

    currentState["in_progress"] = True
    print "I just switched current state to true."

    return redirect('/board')


@app.route('/decline', methods=["POST"])
def decline():
    declined = request.form.get('user_name')
    declined = '@' + declined

    if currentState.get('invited_user_name', "") == declined and currentState.get("in_progress", "") == False:
        message = "%s has declined the game." % currentState['invited_user_name']
        return jsonify({
            'response_type': 'in_channel',
            'text': message
            })
        #return "%s has declined the game." % currentState['invited_user_name']
    else:
        message = "You do not have permission to do this at this time."
        return jsonify({
            'response_type': 'in_channel',
            'text': message
            })
        #return "You do have permission to do this at this time."


@app.route('/board')
def board():
    print "in board route", currentState.get('in_progress', "")
    if currentState.get('in_progress', "") == True:
        message = "| %s | %s | %s |\n|---+---+---|\n| %s | %s | %s |\n|---+---+---|\n| %s | %s | %s |\n" \
            % (entryPositionNames['top-left'],
               entryPositionNames['top-middle'],
               entryPositionNames['top-right'],
               entryPositionNames['middle-left'],
               entryPositionNames['middle'],
               entryPositionNames['middle-right'],
               entryPositionNames['bottom-left'],
               entryPositionNames['bottom-middle'],
               entryPositionNames['bottom-right'])

        # if there is a winner, end game
        if currentState.get('winner', "") == True:
            # refreshing moves once game is over
            for key in entryPositionNames.keys():
                entryPositionNames[key] = "    "

            currentState['in_progress'] = False
            currentState['winner'] = False
            return jsonify({
                'response_type': 'in_channel',
                'text': ("%s wins!" % (currentState['current_player'])),
                'attachments': [
                    {
                        'text': message
                    }
                ]
            })

        # if board is full but no winners:
        if currentState.get('winner', "") == False:
            for value in entryPositionNames.values():
                if value == "    ":
                    #if there are still spaces available, continue
                    return jsonify({
                        'response_type': 'in_channel',
                        'text': ("It is %s's turn !" % (currentState['current_player'])),
                        'attachments': [
                            {
                                'text': message
                            }
                        ]
                    })

            # when the game ends in a draw:
            currentState['in_progress'] = False
            return jsonify({
                'response_type': 'in_channel',
                'text': "It's a draw!",
                'attachments': [
                    {
                        'text': message
                    }
                ]
            })

    else:
        message = "hey! You do not have permission to do this at this time."
        return jsonify({
            'response_type': 'in_channel',
            'text': message
            })
    # return "```| %s | %s | %s |\n|---+---+---|\n| %s | %s | %s |\n|---+---+---|\n| %s | %s | %s |\nIt is %s's turn.```" \
    # % (entryPositionNames['top-left'],
    #    entryPositionNames['top-middle'],
    #    entryPositionNames['top-right'],
    #    entryPositionNames['middle-left'],
    #    entryPositionNames['middle'],
    #    entryPositionNames['middle-right'],
    #    entryPositionNames['bottom-left'],
    #    entryPositionNames['bottom-middle'],
    #    entryPositionNames['bottom-right'],
    #    currentState['current_player'])


@app.route('/move', methods=["POST"])
def move():
    #MUST MAKE SURE THEY ACCEPT THE GAME FIRST
    person_submitted = str(request.form.get('user_name'))
    # person_submitted_id = request.form.get('user_id')
    current = currentState.get('current_player', "")
    print "THIS IS THE %s %s" % (person_submitted, current)

    if current == person_submitted:
        position = 'hello'
        inputPosition = request.form.get('text')
        if inputPosition:
            position = inputPosition
        # check if position is valid and it doesnt have a value
        if position in entryPositionNames:
            # global counter
            # counter += 1
            # must include board view/change
            # return "Valid Move, %s, %s" % (counter, person_submitted)
            # create helper function to see if someone one
            # helper function to place X or O in correct position
            currentPositionEntry = entryPositionNames.get(position, "")
            if currentPositionEntry != "    ":
                message = "This square is already taken. Please choose another."
                return jsonify({
                    'response_type': 'in_channel',
                    'text': message
                    })
                # return "This square is already taken. Please choose another."
            else:
                print "oh gosh, ", currentState['players']
                username = currentState['players'][person_submitted]
                print "!", username

                current_letter = currentState['players'][person_submitted]['letter']
                print current_letter
                entryPositionNames[position] = current_letter

                # checks if the move constitues a win
                if winner(entryPositionNames):
                    currentState['winner'] = True
                    return redirect('/board')

                if currentState.get('current_player') == currentState['creator']:
                    currentState['current_player'] = currentState['invited_user_name']
                else:
                    currentState['current_player'] = currentState['creator']

                # current_letter = currentState['players'][person_submitted]['letter']
                print "this is the new current player: %s" % currentState['current_player']
                return redirect('/board')
        else:
            #if wrong move, list out available move
            available_moves = []
            for key in entryPositionNames.keys():
                available_moves.append(key)

            message = "Please enter a valid move: %s." % (", ".join(available_moves.sort()))
            return jsonify({
                'response_type': 'in_channel',
                'text': message
                })
            # return "Please enter a valid move: %s." % (", ".join(available_moves))

    else:
        message = "Select a box to make a move."
        return jsonify({
            'response_type': 'in_channel',
            'text': message
            })

@app.route('/end_game')
def end():
    # if user is creator or invited
    if currentState.get('in_progress', "") == True:
        currentState['in_progress'] = False
        for key in entryPositionNames.keys():
            entryPositionNames[key] = "    "
        message = "The game has ended."
        return jsonify({
            'response_type': 'in_channel',
            'text': message
            })
        # return "The game has ended."
    else:
        message = "You do not have permission to do this at this time."
        return jsonify({
            'response_type': 'in_channel',
            'text': message
            })
        # return "You do not have permission to do this at this time."

if __name__ == '__main__':


    DEBUG = "NO_DEBUG" not in os.environ
    PORT = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)