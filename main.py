from flask import Flask, Response, request
import os

app = Flask(__name__)

@app.route("/")
def home():
    return Response("Merci de vous être connecté\r\n", mimetype='text/plain')

@app.route("/button_pressed", methods=['POST'])
def button_pressed():
    action = request.form.get('action')
    if action == 'descend':
        # Gérer l'action de descente ici
        print("Bouton appuyé: DESCENDRE")
        return Response("Bouton appuyé: DESCENDRE", mimetype='text/plain')
    return Response("Action invalide", mimetype='text/plain')

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
