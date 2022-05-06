from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    description = db.Column(db.String(144), unique=False)
    price = db.Column(db.Integer, unique=False)


    def __init__(self, name, price):
        self.name = name
        self.price = price


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('name', 'price')


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Endpoint to create a new product
@app.route('/product', methods=["POST"])
def add_product():
    name = request.json['name']
    price = request.json['price']

    new_product = Product(name, price)

    db.session.add(new_product)
    db.session.commit()

    product = Product.query.get(new_product.id)

    return product_schema.jsonify(product)


# Endpoint to query all products
@app.route("/products", methods=["GET"])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


# Endpoint for querying a single product
@app.route("/product/<id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)


# Endpoint for updating a product
@app.route("/product/<id>", methods=["PUT"])
def product_update(id):
    product = Product.query.get(id)
    name = request.json['name']
    price = request.json['price']

    product.name = name
    product.price = price

    db.session.commit()
    return product_schema.jsonify(product)


# Endpoint for deleting a record
@app.route("/product/<id>", methods=["DELETE"])
def product_delete(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return "Product was successfully deleted"


if __name__ == '__main__':
    app.run(debug=True)