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


from flask import Flask, request
import os

app = Flask(__name__)
app.secret_key = "ABC123"  # For demo only.
# entries = {
#     topLeft: "O",
#     bottomRight: "X",
# }

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

# def verifyPosition(position):
#     if entryPositionNames[position]:

@app.route('/board')
def board():

    return "```| %s | %s | %s |\n|---+---+---|\n| %s | %s | %s |\n|---+---+---|\n| %s | %s | %s |```" \
    % (entryPositionNames['top-left'], \
       entryPositionNames['top-middle'], \
       entryPositionNames['top-right'], \
       entryPositionNames['middle-left'], \
       entryPositionNames['middle'], \
       entryPositionNames['middle-right'], \
       entryPositionNames['bottom-left'], \
       entryPositionNames['bottom-middle'], \
       entryPositionNames['bottom-right'])

@app.route('/move', methods=["POST"])
def move():
    position = 'hello'
    inputPosition = request.form.get('text')
    if inputPosition:
        position = inputPosition
    # check if position is valid and it doesnt have a value
    if position in entryPositionNames:
        return "Valid Move"
    else:
        return "Please enter a move."

if __name__ == '__main__':


    DEBUG = "NO_DEBUG" not in os.environ
    PORT = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)