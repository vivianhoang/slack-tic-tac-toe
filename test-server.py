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


from flask import Flask, request, redirect
import requests
import os
from slackclient import SlackClient

SLACK_TOKEN = os.environ.get('SLACK_TOKEN', None)

slack_client = SlackClient(SLACK_TOKEN)

app = Flask(__name__)
app.secret_key = "ABC123"  # For example only


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
}

def send_message(channel_id, message):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username='tic-tac-toe',
        icon_emoji=':robot_face'
    )


# need to make sure I validate keys or team ID

@app.route('/', methods=["POST"])
def state():
    if currentState.get("in_progress","") == False:
        user_id = request.form.get('user_id')
        user_name = request.form.get('user_name')
        invited_player = request.form.get('text')
        currentState['creator'] = '@' + user_name
        currentState['invited_user_name'] = invited_player
        currentState['players'][user_name] = {
            "user_name": user_name,
            "user_id": user_id,
            "letter": "X"
        }
        channel_id = request.form.get('channel_id')
        message = "%s wants to play tic-tac-toe with %s. %s, do you want to /accept or /decline?" % (user_name, invited_player, invited_player)

        print "1 ", currentState['players']

        # r = requests.post('https://hooks.slack.com/services/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', json={"text": "%s wants to play tic-tac-toe with %s." % (user_name, invited_player),
        #                       "attachments": [  
        #                      {"text": "%s, do you /accept or /decline?" % (invited_player)}
        #                 ]})


        return send_message(channel_id, message)
        # return response.send({"response_type": "in_channel",
        #                       "text": "%s wants to play tic-tac-toe with %s." % (user_name, invited_player),
        #                       "attachments": [
        #                      {"text": "%s, do you /accept or /decline?" % (invited_player)}
        #                 ]
        #             })

    else:
        return "A game is already in session between %s and %s. To see the current game," \
            "enter '/board'" % (currentState['creator'], currentState['invited_user_name'])


@app.route('/accept', methods=["POST"])
def accept_invite():
    user_id2 = request.form.get('user_id')
    user_name2 = request.form.get('user_name')
    user_name2 = '@' + user_name2
    currentState['current_player'] = user_name2
    print "hello", currentState.get('current_player', "")
    currentState['players'][user_name2] = {
        "user_name": user_name2,
        "user_id": user_id2,
        "letter": "O"
    }
    if currentState.get("in_progress","") == True:
        return "There is already a game in progress between %s and %s." % (user_name2, currentState['creator'])

    return redirect('/board')

@app.route('/decline', methods=["POST"])
def decline():
    declined = request.form.get('user_name')
    declined = '@' + declined

    if currentState.get('invited_user_name', "") == declined and currentState.get("in_progress", "") == False:
        return "%s has declined the game." % currentState['invited_user_name']
    else:
        return "You do have permission to do this at this time."


@app.route('/end_game')
def end():
    # if user is creator or invited
    if currentState.get('in_progress', "") == True:
        currentState['in_progress'] = False
        return "The game has ended."
    else:
        return "You do not have permission to do this at this time."


@app.route('/board')
def board():
    # need to check if game is in session

    return "```| %s | %s | %s |\n|---+---+---|\n| %s | %s | %s |\n|---+---+---|\n| %s | %s | %s |\nIt is %s's turn.```" \
    % (entryPositionNames['top-left'],
       entryPositionNames['top-middle'],
       entryPositionNames['top-right'],
       entryPositionNames['middle-left'],
       entryPositionNames['middle'],
       entryPositionNames['middle-right'],
       entryPositionNames['bottom-left'],
       entryPositionNames['bottom-middle'],
       entryPositionNames['bottom-right'],
       currentState['current_player'])


@app.route('/move', methods=["POST"])
def move():
    person_submitted = request.form.get('user_name')
    person_submitted_id = request.form.get('user_id')
    current = currentState.get('current_player', "")

    if current == ('@' + person_submitted):
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
            if currentPositionEntry != " ":
                return "This square is already taken. Please choose another."
            else:
                print "yes ", current
                current_letter = currentState['players'][person_submitted]['letter']
                print "no ", current_letter
                entryPositionNames[position] = current_letter
                # usernames = currentState['players'].keys()
                # user_info = usernames.keys()
                for key in currentState['players'].keys():
                    for key2, val in currentState['players'].items():
                        if key2 == "letter" and val != current_letter:
                            currentState['current_player'] = key
                            print 'uh oh', currentState['current_player']
                # set current user to the next user
                return redirect('/board')
        else:
            #if wrong move, list out available move
            available_moves = []
            for key in entryPositionNames.keys():
                available_moves.append(key)
            return "Please enter a valid move: %s." % (", ".join(available_moves))

    else:
        return

if __name__ == '__main__':


    DEBUG = "NO_DEBUG" not in os.environ
    PORT = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)