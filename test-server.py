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
import os

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

counter = 0


@app.route('/', methods=["POST"])
def state():
    if currentState.get("in_progress","") == False:
        user_id = request.form.get('user_id')
        user_name = request.form.get('user_name')
        invited_player = request.form.get('text')
        invited_player = '@'+invited_player
        currentState['invited_user_name'] = invited_player
        currentState['players'][user_name] = {
            "user_name": user_name,
            "user_id": user_id
        }

        print currentState['players']

        return "%s wants to play tic-tac-toe with %s. %s, do you /accept or /decline?" % \
            (user_name, invited_player, invited_player)

    else:
        return "A game is already in session between %s and %s. To see the current game," \
            "enter '/board'" % (currentState['creator'], currentState['invited_user_name'])


@app.route('/accept', methods=["POST"])
def accept_invite():
    user_id2 = request.form.get('user_id')
    user_name2 = request.form.get('user_name')
    currentState[current_player] = user_id2
    currentState['players'][user_name2] = {
        "user_name": user_name2,
        "user_id": user_id2
    }
    currentState["in_progress"] == True:

    return redirect('/board')

@app.route('/decline')
def decline():

    return "%s has declined the game." % currentState[invited_player]


@app.route('/end_game')
def end():
    pass


@app.route('/board')
def board():

    return "```| %s | %s | %s |\n|---+---+---|\n| %s | %s | %s |\n|---+---+---|\n| %s | %s | %s |\nIt is %s's turn.```" \
    % (entryPositionNames['top-left'], \
       entryPositionNames['top-middle'], \
       entryPositionNames['top-right'], \
       entryPositionNames['middle-left'], \
       entryPositionNames['middle'], \
       entryPositionNames['middle-right'], \
       entryPositionNames['bottom-left'], \
       entryPositionNames['bottom-middle'], \
       entryPositionNames['bottom-right'], \
       currentState['current_player'])


@app.route('/move', methods=["POST"])
def move():
    person_submitted = request.form.get('user_name')
    person_submitted_id = request.form.get('user_id')
    current = currentState.get('current_player', "")
    print person_submitted
    print current

    if current == ('@' + person_submitted):
        position = 'hello'
        inputPosition = request.form.get('text')
        if inputPosition:
            position = inputPosition
        # check if position is valid and it doesnt have a value
        if position in entryPositionNames:
            global counter
            counter += 1
            return "Valid Move, %s, %s" % (counter, person_submitted)
            # create helper function to see if someone one
            # helper function to place X or O in correct position
        else:
            #if wrong move, list out available move

            return "Please enter a move."
    else:
        return "What a nice day."

if __name__ == '__main__':


    DEBUG = "NO_DEBUG" not in os.environ
    PORT = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)