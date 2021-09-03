from flask import Flask, jsonify, request, url_for
from werkzeug.utils import redirect

from products import products


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('getProducts'))


@app.route('/products', methods=['GET'])
def getProducts():
    return jsonify({"products": products})


@app.route('/products/<int:product_id>', methods=['GET'])
def getProduct(product_id):
    productsFound = [product for product in products if product['id'] == product_id]
    if len(productsFound) > 0:
        return jsonify({"product": productsFound[0]})
    return jsonify(({"message": 'Producto no encontrado'}))


@app.route('/products', methods=['POST'])
def addProduct():
    new_product = {
        "id": request.json['id'],
        "name": request.json['name'],
        "price": request.json['price'],
        "quantity": request.json['quantity']
    }
    products.append(new_product)
    return jsonify({"message": "Product added succesfully", "products": products})


@app.route('/products/<int:product_id>', methods=['PUT'])
def editProduct(product_id):
    productFound = [product for product in products if product['id'] == product_id]
    if len(productFound) > 0:
        productFound[0]['name'] = request.json['name']
        productFound[0]['price'] = request.json['price']
        productFound[0]['quantity'] = request.json['quantity']
        return jsonify({
            "message": "Product updated",
            "product": productFound
        })
    else:
        return jsonify({"message": "Product not found"})


@app.route('/products/<int:product_id>', methods=['DELETE'])
def deleteProduct(product_id):
    productsFound = [product for product in products if product['id'] == product_id]
    if len(productsFound) > 0:
        products.remove(productsFound[0])
        return jsonify({
            "message": "Product deleted",
            "products": products
        })
    else:
        return jsonify({"message": "Product not found"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)