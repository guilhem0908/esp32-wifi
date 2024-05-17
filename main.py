from flask import Flask, Response
import os

app = Flask(__name__)


@app.route("/")
def home():
    return Response("Thank you for connecting", mimetype='text/plain')


if __name__ == "__main__":
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
