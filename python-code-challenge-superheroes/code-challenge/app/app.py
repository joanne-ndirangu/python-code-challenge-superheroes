#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    return ''


@app.route('/heroes')
def getheroes():

    heroes = []
    for hero in Hero.query.all():
        hero_dict = {
            "id": hero.id,
            "name": hero.name,
            "super name": hero.super_name,
            "created at": hero.created_at,
            "updated at": hero.updated_at
        }
        heroes.append(hero_dict)

    response = make_response(jsonify(heroes), 200)
    response.headers["Content-Type"] = "application/json"

    return response


@app.route('/heroes/<int:id>')
def gethero(id):
    ourhero = Hero.query.filter_by(id=id).first()

    if request.method == 'GET':
        heroobj = {
            "id": ourhero.id,
            "name": ourhero.name,
            "super name": ourhero.super_name,
            "created at": ourhero.created_at,
            "updated at": ourhero.updated_at
        }
        response = make_response(jsonify(heroobj), 200)
        return response

    if ourhero is None:
        return jsonify({"error": "Hero not found"}), 404


@app.route('/powers')
def getpowers():

    powers = []
    for power in Power.query.all():
        power_dict = {
            "id": power.id,
            "name": power.name,
            "description": power.description,
            "created at": power.created_at,
            "updated at": power.updated_at
        }
        powers.append(power_dict)

    response = make_response(jsonify(powers), 200)
    response.headers["Content-Type"] = "application/json"

    return response


@app.route('/powers/<int:id>', methods=['GET', 'PATCH'])
def getpower(id):
    ourpower = Power.query.filter_by(id=id).first()

    if ourpower is None:
        return jsonify({"error": "Power not found"}), 404

    if request.method == 'GET':
        powerobj = {
            "id": ourpower.id,
            "name": ourpower.name,
            "description": ourpower.description,
            "created at": ourpower.created_at,
            "updated at": ourpower.updated_at
        }
        response = make_response(jsonify(powerobj), 200)
        return response

    elif request.method == 'PATCH':
        power = Power.query.filter_by(id=id).first()

        for attr in request.form:
                setattr(power, attr, request.form.get(attr))

        db.session.add(power)
        db.session.commit()

        power_dict = power.to_dict()

        response = make_response(jsonify(power_dict), 200)

        return response


@app.route('/hero_powers', methods=['POST'])
def post_hero_powers():
    data = request.get_json()
    strength = data.get("strength")
    power_id = data.get("power_id")
    hero_id = data.get("hero_id")

    if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be one of: 'Strong', 'Weak', 'Average'")

    new_hero_power = HeroPower(
            strength=strength,
            hero_id=hero_id,
            power_id=power_id
        )

    db.session.add(new_hero_power)
    db.session.commit()

    hero_power_dict = new_hero_power.to_dict()

    response = make_response(jsonify(hero_power_dict), 201)

    return response


if __name__ == '__main__':
    app.run(port=5555)
