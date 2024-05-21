from flask import Flask, render_template
import json
# import othello
import othello_interface
import time

app = Flask(__name__, template_folder='templates', static_folder='static')

game = othello_interface.Othello()
game.initialisation()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/initialisation')
def initialisation():
    game.initialisation()
    return game.board_json()

@app.route('/placement/<id>')
def placement(id):
    return game.interface_handler(id)

B:int = -1
W:int = 1

@app.route('/ai_move_white/<heuristique>')
def ai_move_white(heuristique):
    return game.ai_move(W, 3, heuristique, 3, 15)

@app.route('/ai_move_black/<heuristique>')
def ai_move_black(heuristique):
    return game.random_ai(B)

if __name__ == "__main__":
    app.run(debug=True)