from flask import Flask, jsonify, request, Blueprint, jsonify, request, json
import time

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    time.sleep(5)   # seconds
    #return 'Hello Flask'
    return jsonify({"result": "Hello Flask"}), 202

@app.route('/', methods=['POST'])
def index_post():
    time.sleep(5)   # seconds
    #return 'Hello Flask'
    return jsonify({"result": "POST RESULT"}), 202
    
@app.route('/info')
def info():
    return 'Info'


@app.route('/callback')
def callback():
    return 'I receive callback'

@app.route('/callback_post', methods=['POST'])
def callback_post():
    
    print("TEST callback_post")
    
    # Sample 
    '''
    params = json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return 'No parameter'

    params_str = ''
    for key in params.keys():
        params_str += 'key: {}, value: {}<br>'.format(key, params[key])
    return params_str
    '''

    return jsonify({"result": "Hello Flask"}), 202


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=19000)