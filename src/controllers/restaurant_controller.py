from flask import Blueprint, request
from init import db
from models.restaurant import Restaurant, restaurant_schema, restaurants_schema, VALID_TYPES
from flask_jwt_extended import get_jwt_identity, jwt_required
from controllers.food_controller import foods_bp, admin_required

# Create blueprint with prefix "/restaurants"
restaurants_bp = Blueprint('restaurants', __name__, url_prefix='/restaurants')


@restaurants_bp.route('/')
def get_all_restaurants():
    # Select all restaurants in ascending order
    stmt = db.select(Restaurant).order_by(Restaurant.name.asc())
    restaurants = db.session.scalars(stmt)
    return restaurants_schema.dump(restaurants)


@restaurants_bp.route('/<int:id>')
def get_one_restaurant(id):
    # Select Restaurant with matching id 
    stmt = db.select(Restaurant).filter_by(id=id)
    restaurant = db.session.scalar(stmt)
    if restaurant:
        return restaurant_schema.dump(restaurant)
    else:
        return {'error': f'Restaurant with id {id} not found'}, 404


@restaurants_bp.route('/', methods=['POST'])
@jwt_required()
@admin_required
def create_restaurant():
    body_data = request.get_json()
    if body_data.get('type') not in VALID_TYPES:
        return {'error': f'Invalid type: {body_data.get("type")}'}, 400
    # Create new instance of Restaurant object
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
     # Select Restaurant with matching id
    stmt = db.select(Restaurant).filter_by(id=restaurant_id)
    restaurant = db.session.scalar(stmt)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return {'msg': f'Restaurant with id {restaurant_id} deleted successfully'}
    else:
        return {'error': f'Restaurant with id {restaurant_id} not found'}, 404
    

@restaurants_bp.route('/<int:restaurant_id>', methods=['PUT', 'PATCH'])
@jwt_required()
@admin_required
def update_restaurant(restaurant_id):
    body_data = restaurant_schema.load(request.get_json(), partial=True)
     # Select Restaurant with matching id
    stmt = db.select(Restaurant).filter_by(id=restaurant_id)
    restaurant = db.session.scalar(stmt)
    if restaurant:
        restaurant.name = body_data.get('name') or restaurant.name
        restaurant.location = body_data.get('location') or restaurant.location
        restaurant.contact_number = body_data.get('contact_number') or restaurant.contact_number
        restaurant.website = body_data.get('website') or restaurant.website
        restaurant.type = body_data.get('type') or restaurant.type
        db.session.commit()
        return restaurant_schema.dump(restaurant)
    else:
        return {'error': f'Restaurant with id {id} not found'}, 404