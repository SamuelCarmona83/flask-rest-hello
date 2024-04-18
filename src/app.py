"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Drink, Order
import random
import math
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def handle_hello():

    users = User.query.all() # SELECT * from users;

    return jsonify([ person.serialize() for person in users ]), 200


@app.route('/drinks-paginated', methods=['GET'])
def drinks_paginated():

    page = int(request.args.get('page', 1))
    max_items = int(request.args.get('limit', 10))

    total_drinks = Drink.query.count()
    last_page = math.ceil( total_drinks / max_items )

    if page > last_page:
        return "Error page out of limit & the last page is " + str(last_page), 400
    
    drinks = Drink.query.offset( (page - 1) * max_items ).limit(max_items) # Objetos de Python
    results = [drk.serialize() for drk in drinks] # Diccionarios


    return jsonify({
        "results": results,
        "page": page,
        "total": total_drinks,
        "last_page": last_page
    }), 200

@app.route('/drink', methods=['POST', 'GET'])
def add_drink():
    if request.method == 'GET':
        drinks = Drink.query.all()
        return jsonify([ drink.serialize() for drink in drinks ]), 200
    body = request.json

    name = body.get("name")
    price = body.get("price")

    if name != None and price != None:
        new_drink = Drink(precio=price, name=name) # Constructor
        db.session.add(new_drink) # RAM
        db.session.commit() # ID 
        return jsonify(new_drink.serialize()), 201
    
    return jsonify({ "msg": "Error missing keys"}), 400

@app.route('/drink/<int:id>', methods=['PUT', 'DELETE'])
def handle_drink(id):
    search = Drink.query.filter_by(id=id).one_or_none() # WHERE
    if request.method == 'PUT':
        if search != None:
            body = request.json
            new_name = body.get("name", None)
            new_price = body.get("price", None)
            if new_name != None:
                search.name = new_name
            if new_price != None:
                search.precio = new_price
            db.session.commit()
            return jsonify(search.serialize()), 200
        return jsonify({ "msg": "Drink not found "}), 404
    else:
        if search != None:
            db.session.delete(search)
            db.session.commit()
            return jsonify({ "msg": "Removed with success" }), 200
        else:
            return jsonify({ "msg": "Drink not found "}), 404
    return jsonify({ "msg": "Something Happened!" }), 500


@app.route('/populate', methods=['POST'])
def generate_drinks():

    fruits = ['Limon', 'Naranja', 'Maracuya', 'Mango', 'Piña']

    alcohols = ['Ron','Vodka','Gin','Whiskey']

    add_ons = ['Copa','Caña', 'Pinta', 'Trago']
    try:
        for _ in range(0,100):

            drink_name = f"{random.choice(add_ons)} de {random.choice(alcohols)} con {random.choice(fruits)}"
            random_price = random.randint(4,12)
            new_drink = Drink.save(name=drink_name, price=random_price)
    except:
        return jsonify({ "msg": "Something happened!" }), 500
    return jsonify({ "msg": "Success!" }), 200




@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([ ord.serialize() for ord in orders ]), 200




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
