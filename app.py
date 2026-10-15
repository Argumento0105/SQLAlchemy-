from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///base_datos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock
        }


@app.route("/")
def index():
    return jsonify({
        "mensaje": "API de productos funcionando"
    })


# CREATE: crear un producto
@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json(silent=True) or {}

    if not data.get("name") or data.get("price") is None:
        return jsonify({
            "error": "El nombre y el precio son obligatorios"
        }), 400

    product = Product(
        name=data["name"],
        price=data["price"],
        stock=data.get("stock", 0)
    )

    db.session.add(product)
    db.session.commit()

    return jsonify(product.to_dict()), 201


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)