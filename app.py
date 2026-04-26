from flask import Flask
from flask_cors import CORS

from routes.calculate_routes import calculate_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(calculate_bp)


@app.route("/")
def home():
    return "Cook Buddies Backend Running!"


if __name__ == "__main__":
    app.run(debug=True)