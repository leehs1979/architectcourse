from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello Flask'
    
@app.route('/info')
def info():
    return 'Info'


@app.route('/callback')
def callback():
    return 'I receive callback'