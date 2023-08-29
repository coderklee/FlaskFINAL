from flask import Blueprint, request, jsonify
from helpers import token_required
from models import db, Estimate, estimate_schema, estimates_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/estimates', methods = ['POST'])
@token_required
def add_estimate(current_user_token):
    name = request.json['name']
    phone_number = request.json['phone_number']
    email = request.json['email']
    address = request.json['address']
    description = request.json['description']
    user_token = current_user_token.token

    print(f"BIG TESTER: {current_user_token.token}")

    estimate = Estimate(name, phone_number, email, address, description, user_token=user_token)

    db.session.add(estimate)
    db.session.commit()

    response = estimate_schema.dump(estimate)
    return jsonify(response)

@api.route('/estimates', methods = ['GET'])
@token_required
def get_estimates(current_user_token):
    a_user = current_user_token.token
    estimate = Estimate.query.filter_by(user_token = a_user).all()
    response = estimates_schema.dump(estimate)
    return jsonify(response)

@api.route('/estimates/<id>', methods = ['POST', 'PUT'])
@token_required
def update_estimate(current_user_token, id):
    estimate = Estimate.query.get(id)
    estimate.name = request.json['name']
    estimate.phone_number = request.json['phone_number']
    estimate.email = request.json['email']
    estimate.address = request.json['address']
    estimate.description = request.json['description']
    estimate.user_token = current_user_token.token

    db.session.commit()
    response = estimate_schema.dump(estimate)
    return jsonify(response)

@api.route('/estimates/<id>', methods = ['DELETE'])
@token_required
def delete_estimate(current_user_token, id):
    estimate = Estimate.query.get(id)
    db.session.delete(estimate)
    db.session.commit()
    response = estimate_schema.dump(estimate)
    return jsonify(response)

@api.route('/estimates/<id>', methods = ['GET'])
@token_required
def get_single_estimate(current_user_token, id):
    estimate = Estimate.query.get(id)
    response = estimate_schema.dump(estimate)
    return jsonify(response)