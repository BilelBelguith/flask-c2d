import subprocess
from flask import Flask, jsonify, render_template
import os ;
from flask import request

#app = Flask(__name__)

#@app.route('/')
#def home():
#    return render_template('index.html')

#if __name__ == '__main__':
#    app.run(debug=True)


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)