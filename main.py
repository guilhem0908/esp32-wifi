from flask import Flask, Response, request
import os

app = Flask(__name__)

# Variable globale pour stocker l'action
current_action = "arret"  # Valeur par défaut

@app.route("/")
def home():
    return Response("Merci de vous être connecté\r\n", mimetype='text/plain')

@app.route("/button_pressed", methods=['POST'])
def button_pressed():
    global current_action
    action = request.form.get('action')
    if action in ['descend', 'monte', 'ouvert', 'arret']:
        current_action = action
        print(f"Bouton appuyé: {action.upper()}")
        return Response(action, mimetype='text/plain')
    return Response("Action invalide", mimetype='text/plain')

@app.route("/get_action", methods=['GET'])
def get_action():
    return Response(current_action, mimetype='text/plain')

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
