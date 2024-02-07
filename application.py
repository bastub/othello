from flask import Flask, render_template
import json
import othello.py as othello 

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route('/background_process_test')
def command(FUNCTION=None):
    json_datas = {
        "pion_noir": ["00", "01"],
        "pion_blanc" : "12",
        "outline_pion_noir": "22",
        "outline_pion_blanc": "32",        
    }
    return json.dumps(json_datas)