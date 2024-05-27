import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Variable globale pour stocker l'état du volet
volet_status = {"status": "unknown"}

@app.route("/")
def home():
    return "Server is running."

@app.route("/button_pressed", methods=['POST'])
def button_pressed():
    action = request.form.get('action')
    if action in ["descend", "monte", "arret"]:
        volet_status["status"] = action
    return jsonify({"action": action})

@app.route("/update_status", methods=['POST'])
def update_status():
    status = request.form.get('status')
    if status in ["ferme", "ouvert"]:
        volet_status["status"] = status
    return jsonify(volet_status)

@app.route("/get_status", methods=['GET'])
def get_status():
    return jsonify(volet_status)

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
