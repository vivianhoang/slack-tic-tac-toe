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
    "in_progress": True,
    "players": {},
    "invited_user_name": " ",
    "current_player": " ",
}

counter = 0

@app.route('/', methods=["POST"])
def state():
    user_id = request.form.get('user_id')
    user_name = request.form.get('user_name')
    invited_player = request.form.get('text')
    currentState['invited_user_name'] = invited_player
    currentState['current_player'] = invited_player
    currentState['players'][user_name] = {
        "user_name": user_name,
        "user_id": user_id
    }

    return redirect('/board')

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
    current = currentState.get('current_player', "")

    if current == person_submitted:
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
        pass

if __name__ == '__main__':


    DEBUG = "NO_DEBUG" not in os.environ
    PORT = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)