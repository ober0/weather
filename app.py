import pprint
from get_weather import get_weather
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return get_weather('Балашиха')

if __name__ == '__main__':
    app.run(debug=True)
