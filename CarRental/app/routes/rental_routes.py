from flask import Blueprint, request, jsonify, g
from datetime import datetime
from .. import db, auth
from ..models import Car, Rental
from ..utils.auth import role_required

rental_bp = Blueprint('rentals', __name__)


@rental_bp.route('/rent/<int:car_id>', methods=['POST'])
@auth.login_required
@role_required('user')
def rent_car(car_id):

    active_rental = Rental.query.filter_by(user_id=g.current_user.id, end_date=None).first()
    if active_rental:
        return jsonify({"error": "Already renting a car"}), 400

    car = Car.query.get_or_404(car_id)
    if not car.available:
        return jsonify({"error": "Car not available"}), 400

    car.available = False
    rental = Rental(
        user_id=g.current_user.id,
        car_id=car.id,
        start_date=datetime.utcnow()
    )
    db.session.add(rental)
    db.session.commit()

    return jsonify({"message": "Car rented successfully"}), 201


@rental_bp.route('/return/<int:car_id>', methods=['POST'])
@auth.login_required
@role_required('user')
def return_car(car_id):

    rental = Rental.query.filter_by(
        car_id=car_id,
        user_id=g.current_user.id,
        end_date=None
    ).first()

    if rental is None:
        return jsonify({"error": "No active rental found"}), 404

    rental.end_date = datetime.utcnow()

    # price logic
    days = (rental.end_date - rental.start_date).days + 1
    rental.total_price = days * rental.car.price_per_day

    rental.car.available = True

    db.session.commit()

    return jsonify({
        "message": "Car returned successfully",
        "total_price": rental.total_price,
        "rental_days": days
    }), 200


@rental_bp.route('/history', methods=['GET'])
@auth.login_required
@role_required('user')
def rental_history():

    rentals = Rental.query.filter_by(user_id=g.current_user.id).all()
    result = []

    for r in rentals:
        result.append({
            "rental_id": r.id,
            "car": {
                "make": r.car.make,
                "model": r.car.model,
                "year": r.car.year
            },
            "start_date": r.start_date.isoformat(),
            "end_date": r.end_date.isoformat() if r.end_date else None,
            "total_price": r.total_price
        })

    return jsonify(result), 200
