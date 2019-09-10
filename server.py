import requests
import operator
import redis
import os
from flask import Flask, render_template, request

app = Flask(__name__)

r = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=0)

@app.route('/setvalue/', methods=['POST'])
def setvalue():
    errors = []
    set_message_result = ""
    try:
        input_key = request.form['input_key']
        input_value = request.form['input_value']
    except Exception as e:
        errors.append(e)
    if input_key != "" and input_value != "":
        r.set(input_key, input_value)
        set_message_result = "Set value for Redis is successfuly"
    else:
        set_message_result = "Value that you enter not true!"

    return render_template('home.html', errors=errors, set_message_result=set_message_result)

@app.route('/getvalue/', methods=['POST'])
def getvalue():
    errors = []
    get_message_result = ""
    try:
        input_key_get = request.form['input_key_get']
    except Exception as e:
        errors.append(e)
    if input_key_get != "":        
        get_message_result = r.get(input_key_get)
        print(get_message_result)
        if get_message_result == None:
            get_message_result = "No value is exist on the system."
    else:
        get_message_result = "Please enter key to get value from Redis"
    return render_template('home.html', errors=errors, get_message_result=get_message_result)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)