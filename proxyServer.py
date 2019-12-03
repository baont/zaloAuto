import time
import requests
from flask import Flask
from flask import jsonify
from flask import request
from flask import send_file
from flask import Response
DURATION_BETWEEN_TWO_CALL = 10.0
app = Flask(__name__)
urlPool = [
    # url                                 last time call (default = 0.0)
    ["http://localhost:5001/getavatar?phone={}", 0.0],
    ["http://localhost:5002/getavatar?phone={}", 0.0],
]
@app.route('/getavatar')
def getAvatar():
    userPhoneNumb = request.args.get('phone')
    if not userPhoneNumb:
        return 'Need a phone number!'
    while 1:
        for pair in urlPool:
            fromLastCall =  time.time() - pair[1]
            if pair[1] == 0.0 or fromLastCall >= DURATION_BETWEEN_TWO_CALL:
                pair[1] = time.time()
                response = requests.get(pair[0].format(userPhoneNumb))
                return Response(response.content, mimetype="image/jpg")
        print("wait for available server")
