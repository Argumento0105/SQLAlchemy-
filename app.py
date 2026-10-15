from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///base_datos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


@app.route("/")
def index():
    return jsonify({
        "mensaje": "API de productos funcionando"
    })


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)