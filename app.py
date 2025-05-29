from flask import Flask
from vote_routes import vote_bp

app = Flask(__name__)
app.secret_key = "supersecret"
app.register_blueprint(vote_bp)

if __name__ == "__main__":
    app.run(debug=True)
