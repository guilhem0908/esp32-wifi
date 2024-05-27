import os
from flask import Flask, Response, request, jsonify
import threading
import time

app = Flask(__name__)

volet_status = {"status": "unknown"}  # Variable globale pour stocker l'état du volet

@app.route("/")
def home():
    return Response("Thank you for connecting\r\n", mimetype='text/plain')

@app.route("/update_status", methods=['POST'])
def update_status():
    global volet_status
    volet_status['status'] = request.form.get('status')
    return jsonify(volet_status)

@app.route("/get_status")
def get_status():
    return jsonify(volet_status)

shutdown_event = threading.Event()

def run_flask():
    port = int(os.getenv('PORT', 8080))

    def check_shutdown():
        while not shutdown_event.is_set():
            time.sleep(0.1)
        os._exit(0)

    check_thread = threading.Thread(target=check_shutdown)
    check_thread.start()

    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

if __name__ == "__main__":
    run_flask()
