#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries', methods=['GET'])
def get_bakeries():
    bakeries = Bakery.query.all()
    bakery_data = [bakery.to_dict() for bakery in bakeries]
    return jsonify(bakery_data)

@app.route('/bakeries/<int:id>', methods=['GET'])
def get_bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery is None:
        return jsonify({'error': 'Bakery not found'}), 404

    bakery_data = bakery.to_dict()
    bakery_data['baked_goods'] = [good.to_dict() for good in bakery.baked_goods]
    return jsonify(bakery_data)

@app.route('/baked_goods/by_price', methods=['GET'])
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_data = [good.to_dict() for good in baked_goods]
    return jsonify(baked_goods_data)

@app.route('/baked_goods/most_expensive', methods=['GET'])
def get_most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if baked_good is None:
        return jsonify({'error': 'No baked goods found'}), 404
    return jsonify(baked_good.to_dict())

if __name__ == '__main__':
    app.run()