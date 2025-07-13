from flask import Blueprint, request, jsonify, g
from .. import db, auth
from ..models import Car
from ..utils.auth import role_required

car_bp = Blueprint('cars', __name__)


@car_bp.route('/', methods=['POST'])
@auth.login_required
@role_required('merchant')
def add_car():
    data = request.json
    make = data.get('make')
    model = data.get('model')
    year = data.get('year')
    price_per_day = data.get('price_per_day', 0.0)

    if not all([make, model, year]):
        return jsonify({"error": "Missing fields"}), 400

    new_car = Car(
        merchant_id=g.current_user.id,
        make=make,
        model=model,
        year=year,
        price_per_day=price_per_day
    )
    db.session.add(new_car)
    db.session.commit()

    return jsonify({"message": "Car added", "car_id": new_car.id}), 201


@car_bp.route('/<int:car_id>', methods=['PUT'])
@auth.login_required
@role_required('merchant')
def update_car(car_id):
    car = Car.query.get_or_404(car_id)

    data = request.json
    car.make = data.get('make', car.make)
    car.model = data.get('model', car.model)
    car.year = data.get('year', car.year)
    car.price_per_day = data.get('price_per_day', car.price_per_day)
    db.session.commit()

    return jsonify({"message": "Car updated"}), 200


@car_bp.route('/<int:car_id>', methods=['DELETE'])
@auth.login_required
@role_required('merchant')
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)

    db.session.delete(car)
    db.session.commit()

    return jsonify({"message": "Car deleted"}), 200


@car_bp.route('/', methods=['GET'])
@auth.login_required
def list_cars():
    # only lists available cars, not all of them
    cars = Car.query.filter_by(available=True).all()

    result = [{
        "id": c.id,
        "make": c.make,
        "model": c.model,
        "year": c.year,
        "price_per_day": c.price_per_day
    } for c in cars]

    return jsonify(result), 200
