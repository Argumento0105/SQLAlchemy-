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



@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "mensaje": "API de productos funcionando",
        "operaciones": {
            "crear": "POST /products",
            "listar": "GET /products",
            "consultar_por_id": "GET /products/<id>",
            "actualizar": "PUT /products/<id>",
            "eliminar": "DELETE /products/<id>",
            "insertar_datos_prueba": "POST /products/demo"
        }
    })




@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Debes enviar un JSON valido"}), 400

    name = data.get("name")
    price = data.get("price")
    stock = data.get("stock", 0)

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "El nombre es obligatorio"}), 400

    if (
        isinstance(price, bool)
        or not isinstance(price, (int, float))
        or price < 0
    ):
        return jsonify({"error": "El precio debe ser numerico y no negativo"}), 400

    if (
        isinstance(stock, bool)
        or not isinstance(stock, int)
        or stock < 0
    ):
        return jsonify({"error": "El stock debe ser un entero no negativo"}), 400

    product = Product(
        name=name.strip(),
        price=price,
        stock=stock
    )

    db.session.add(product)
    db.session.commit()

    return jsonify(product.to_dict()), 201



@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products]), 200




@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = db.session.get(Product, product_id)

    if product is None:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify(product.to_dict()), 200



@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = db.session.get(Product, product_id)

    if product is None:
        return jsonify({"error": "Producto no encontrado"}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({"error": "Debes enviar datos en formato JSON"}), 400

    if "name" in data:
        if not isinstance(data["name"], str) or not data["name"].strip():
            return jsonify({"error": "El nombre no puede estar vacio"}), 400
        product.name = data["name"].strip()

    if "price" in data:
        price = data["price"]
        if (
            isinstance(price, bool)
            or not isinstance(price, (int, float))
            or price < 0
        ):
            return jsonify({"error": "Precio invalido"}), 400
        product.price = price

    if "stock" in data:
        stock = data["stock"]
        if (
            isinstance(stock, bool)
            or not isinstance(stock, int)
            or stock < 0
        ):
            return jsonify({"error": "Stock invalido"}), 400
        product.stock = stock

    db.session.commit()

    return jsonify(product.to_dict()), 200




@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = db.session.get(Product, product_id)

    if product is None:
        return jsonify({"error": "Producto no encontrado"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({
        "mensaje": "Producto eliminado correctamente",
        "id": product_id
    }), 200



@app.route("/products/demo", methods=["POST"])
def insert_products():
    # Evita duplicar los datos si ya existen productos
    if Product.query.first():
        return jsonify({
            "mensaje": "Ya existen productos. No se agregaron duplicados.",
            "productos": [p.to_dict() for p in Product.query.all()]
        }), 200

    products = [
        Product(name="Laptop Gamer", price=1250.99, stock=10),
        Product(name="Mouse Inalambrico", price=25.50, stock=30),
        Product(name="Teclado Mecanico", price=75.00, stock=15)
    ]

    db.session.add_all(products)
    db.session.commit()

    return jsonify({
        "mensaje": "Tres productos creados correctamente",
        "productos": [p.to_dict() for p in products]
    }), 201



if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # Insertar 3 productos si la tabla esta vacia
        if not Product.query.first():
            productos = [
                Product(
                    name="Laptop Gamer",
                    price=1250.99,
                    stock=10
                ),
                Product(
                    name="Mouse Inalambrico",
                    price=25.50,
                    stock=30
                ),
                Product(
                    name="Teclado Mecanico",
                    price=75.00,
                    stock=15
                )
            ]

            db.session.add_all(productos)
            db.session.commit()

            print("¡Tres productos insertados correctamente!")
        else:
            print("La base de datos ya contiene productos.")

    app.run(debug=True)