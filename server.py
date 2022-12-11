from flask import Flask, request, abort
import json
import random
from config import me
from mock_data import catalog
from config import db
from bson import ObjectId

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
    # read from the db
    cursor = db.Products.find({})
    results = []
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)

    return json.dumps(results)


# Post /api/catalog
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

    #  save producr to the database
    # save the object, will assign an _id:ObjectID(uniquevalue)
    db.Products.insert_one(product)
    # fix the _id value
    product["_id"] = str(product["_id"])

    return json.dumps(product)


@app.get("/api/test/count")
def num_of_products():
    count = db.Products.count_documents({})
    return json.dumps({"total": count})


@app.get("/api/catalog/<category>")
def by_category(category):
    results = []
    cursor = db.Products.find({"category": category})
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)

    return json.dumps(results)


@app.get("/api/catalog/search/<text>")
def search_by_text(text):
    text = text.lower()
    results = []
    cursor = db.Products.find({"title": {"$regex": text, "$options": "i"}})
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)

    return json.dumps(results)


@app.get("/api/categories")
def get_categories():
    results = []
    cursor = db.Products.distinct("category")
    for cat in cursor:
        results.append(cat)

    return json.dumps(results)


@app.get("/api/test/value")
def total_value():
    total = 0
    cursor = db.Products.find({})
    for prod in cursor:
        total += prod["price"]

    return json.dumps(total)


# create an endpoint that returns the cheapest product
@app.get("/api/product/cheapest")
def cheapest_product():
    cursor = db.Products.find({})
    cheapest = cursor[0]
    for prod in cursor:
        if prod["price"] < cheapest["price"]:
            cheapest = prod

    return json.dumps(cheapest)


@app.get("/api/product/<id>")
def search_by_id(id):
    objId = ObjectId(id)
    prod = db.Products.find_one({"_id": objId})
    if not prod:
        return abort(404, "Product not found")

    prod["_id"] = str(prod["_id"])
    return json.dumps(prod)


# app.run(debug=True)


############################################################################
############################# COUPON CODES###################################
#
# save
# save: POST /api/coupons# get all: GET /api/coupons# get by id: GET /api/coupons/<id>
@app.post("/api/coupons")
def save_coupon():
    coupon = request.get_json()
    # validate the coupon
    if "code" not in coupon:
        return abort(400, "Code is required")
    # must have a discount
    if "discount" not in coupon:
        return abort(400, "Discount is required")

    db.Coupons.insert_one(coupon)

    # fix the _id value
    coupon["_id"] = str(coupon["_id"])

    return json.dumps(coupon)

# get al


@app.get("/api/coupons")
def all_coupons():
    results = []
    cursor = db.Coupons.find({})
    results = []
    for coupon in cursor:
        coupon["_id"] = str(coupon["_id"])
        results.append(coupon)

    return json.dumps(results)

# get by id


@app.get("/api/coupons/<id>")
def coupon_id(id):
    objId = ObjectId(id)
    coupon = db.Coupons.find_one({"_id": objId})
    if not coupon:
        return abort(404, "Coupon not found")

    coupon["_id"] = str(coupon["_id"])
    return json.dumps(coupon)

# get by code


@app.get("/api/coupons/validate/<code>")
def coupon_code(code):
    coupon = db.Coupons.find_one({"code": code})
    if not coupon:
        return abort(404, "Invalid code")

    coupon["_id"] = str(coupon["_id"])
    return json.dumps(coupon)
