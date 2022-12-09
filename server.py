from flask import Flask, request, abort
import json
import random
from config import me
from mock_data import catalog
from flask_cors import CORS
app = Flask("server")
CORS(app)

@app.get("/")
def home():
    return "Hello from Flask"


@app.get("/test")
def test():
    return "This is another endpoint"


# get /api/about
# return me as json
@app.get("/about")
def about():
    return "Brenda Allemand"


##################################################################
####################  CATALOG API ################################
##################################################################

@app.get("/api/version")
def version():
    version = {
        "v": "v1.0.4",
        "name": "zombie rabbit",
    }
    # parse a dictionary into json
    return json.dumps(version)


@app.get("/api/about")
def get_about():
    return json.dumps(me)


@app.get("/api/catalog")
def api_catalog():
    return json.dumps(catalog)


#Post /api/catalog
@app.post("/api/catalog")
def save_product():
    product = request.get_json()

    # validate the product
    if "title" not in product:
        return abort(400, "Title is required")

    # the title should have at least 5 characters
    if len(product["title"]) < 5:
        return abort(400, "Title should have at least 5 characters")

    # must have a category
    if "category" not in product:
        return abort(400, "Category is required")

    # must have a price
    if "price" not in product:
        return abort(400, "Price is required")

    if not isinstance(product["price"], (float, int)):
        return abort(400, "Price must be a number")

    # price should be greater than 0
    if product["price"] <= 0:
        return abort(400, "Price should be greater than 0")

    #  assign a unique id to the product
    product["_id"] = random.randint(1000, 10000)

    catalog.append(product)

    return json.dumps(product)


@app.get("/api/test/count")
def num_of_products():
    return len(catalog)


@app.get("/api/catalog/<category>")
def by_category(category):
    results = []
    category = category.lower()
    for product in catalog:
        if product["category"].lower() == category.lower():
            results.append(product)
    return json.dumps(results)


@app.get("/api/catalog/search/<text>")
def search_by_text(text):
    text = text.lower()
    results = []

    for product in catalog:
        if text in product["title"].lower():
            results.append(product)
    return json.dumps(results)


@app.get("/api/categories")
def get_categories():
    results = []
    for product in catalog:
        cat = product["category"]
        if cat not in results:
            results.append(cat)

    return json.dumps(results)


@app.get("/api/test/value")
def total_value():
    total = 0
    for product in catalog:
        # total += total + product["price"]
        total = total + product["price"]

    return json.dumps(total)


# create an endpoint that returns the cheapest product
@app.get("/api/product/cheapest")
def cheapest_product():
    cheapest = catalog[0]
    for product in catalog:
        if product["price"] < cheapest["price"]:
            cheapest = product
    return json.dumps(cheapest)


@app.get("/api/product/<_id>")
def search_by_id(_id):
    for product in catalog:
        if product["_id"] == _id:
            return json.dumps(product)

    return "Error: Product not found"


# app.run(debug=True)
