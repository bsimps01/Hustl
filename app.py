from flask import Flask, render_template
from pymongo import MongoClient
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def main_index():
    return render_template('main_index.html')

if __name__ == '__main__':
    app.run(debug=True)