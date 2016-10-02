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


from flask import Flask
import os

app = Flask(__name__)
app.secret_key = "ABC123"  # For demo only.
# entries = {
#     topLeft: "O",
#     bottomRight: "X",
# }

# entryPositionNames = {
#     'top-left': True,
#     'top-middle': True,
#     'top-right': True,
#     'middle-left': True,
#     'middle': True,
#     'middle-right': True,
#     'bottom-left': True,
#     'bottom-middle': True,
#     'bottom-right': True,
# }

# def verifyPosition(position):
#     if entryPositionNames[position]:

print "hello"

@app.route('/')
def home():

    return "Hello"

@app.route('/board')
def board():

    return "[.][.][.]<br>[.][.][.]<br>[.][.][.]"

# @app.route('/play')
# def 

if __name__ == '__main__':


    DEBUG = "NO_DEBUG" not in os.environ
    PORT = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)