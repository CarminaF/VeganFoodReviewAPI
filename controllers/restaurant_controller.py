from flask import Blueprint, request
from init import db
from models.restaurant import Restaurant, restaurant_schema, restaurants_schema
from flask_jwt_extended import get_jwt_identity, jwt_required
from controllers.food_controller import foods_bp, admin_required

restaurants_bp = Blueprint('restaurants', __name__, url_prefix='/restaurants')


@restaurants_bp.route('/')
def get_all_restaurants():
    stmt = db.select(Restaurant).order_by(Restaurant.name.asc())
    restaurants = db.session.scalars(stmt)
    print(restaurants)
    return restaurants_schema.dump(restaurants)


@restaurants_bp.route('/<int:id>')
def get_one_restaurant(id):
    stmt = db.select(Restaurant).filter_by(id=id)
    restaurant = db.session.scalar(stmt)
    if restaurant:
        return restaurant_schema.dump(restaurant)
    else:
        return {'error': f'Restaurant with id {id} not found'}, 404


@restaurants_bp.route('/', methods=['POST'])
@jwt_required()
def create_restaurant():
    body_data = request.get_json()
    # Create new instance of Card object
    restaurant = Restaurant (
        name=body_data.get('name'),
        location=body_data.get('location'),
        contact_number=body_data.get('contact_number'),
        website=body_data.get('website'),
        type=body_data.get('type'),
    )
    db.session.add(restaurant)
    db.session.commit()
    return restaurant_schema.dump(restaurant), 201

@restaurants_bp.route('/<int:restaurant_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_restaurant(restaurant_id):
    stmt = db.select(Restaurant).filter_by(id=restaurant_id)
    restaurant = db.session.scalar(stmt)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return {'msg': f'Restaurant with id {restaurant_id} deleted successfully'}
    else:
        return {'error': f'Restaurant with id {restaurant_id} not found'}, 404
    
