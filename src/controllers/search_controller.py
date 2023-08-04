from init import db, ma  
from models.restaurant import Restaurant, restaurant_schema, restaurants_schema, VALID_TYPES
from models.food import Food, food_schema, foods_schema
from flask import Blueprint
from flask_jwt_extended import jwt_required

# Create blueprint
search_bp  = Blueprint('search', __name__, url_prefix='/search')

# Search a keyword in the food name and description eg) 'burger'
@search_bp.route('/food/<string:keyword>')
@jwt_required()
def search_food(keyword):
    # Select Foods containing keyword in name or description
    stmt = db.select(Food).where(db.or_(Food.description.ilike(f'%{keyword}%'), Food.name.ilike(f'%{keyword}%')))
    results = db.session.scalars(stmt)
    if results:
        return foods_schema.dump(results)
    else:
        return {'error': f'Could not find foods with keyword {keyword}'}, 404


# Search a location in the location field
@search_bp.route('/location/<string:keyword>')
@jwt_required()
def search_location(keyword):
    # Select Restaurant containing keyword in location
    stmt = db.select(Restaurant).where(Restaurant.location.ilike(f'%{keyword}%'))
    results = db.session.scalars(stmt)
    if results:
        return restaurants_schema.dump(results)
    else:
        return {'error': f'Could not find restaurants in {keyword}'}, 404


# Search for food items with a max price
@search_bp.route('/price/max/<int:price>')
@jwt_required()
def search_max_price(price):
    # Select Foods lower or equal to the max price 
    stmt = db.select(Food).where(Food.price<=price)
    results = db.session.scalars(stmt)
    if results:
        return foods_schema.dump(results)
    else:
        return {'error': f'Could not find foods under ${price}'}, 404

# Search for certain types of restaurants
#  0 - Vegan, 1 - Vegetarian, 2 - Vegan options available
@search_bp.route('/type/<int:type>')
@jwt_required()
def search_by_type(type):
    if type < 0 or type >= len(VALID_TYPES):
        return {'error': 'Invalid type'}, 401
    # Select Restaurant according to type (0 -  vegan, 1 - vegetarian, 2 - vegan options)
    stmt = db.select(Restaurant).where(Restaurant.type==VALID_TYPES[type])
    results = db.session.scalars(stmt)
    return restaurants_schema.dumps(results)