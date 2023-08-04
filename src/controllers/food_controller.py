from flask import Blueprint, request
from init import db, ma
from models.food import Food, food_schema, foods_schema
from models.restaurant import Restaurant, restaurant_schema, restaurants_schema
from models.user import User
from models.review import Review
from controllers.review_controller import reviews_bp
from controllers.auth_controller import admin_required
from flask_jwt_extended import jwt_required

# Create blueprint with prefix "/foods"
foods_bp = Blueprint('foods', __name__, url_prefix='/foods')
# Register review blueprint here as reviews belongs to one food
foods_bp.register_blueprint(reviews_bp, url_prefix='/<int:food_id>/reviews')

# Create new food under one existing restaurant
@foods_bp.route('/<int:restaurant_id>', methods=['POST'])
@jwt_required()
def create_food(restaurant_id):
    body_data = request.get_json()
    stmt = db.select(Restaurant).filter_by(id=restaurant_id)
    restaurant = db.session.scalar(stmt)
    if restaurant:
        food = Food (
            name=body_data.get('name'),
            description=body_data.get('description'),
            price=body_data.get('price'),
            restaurant=restaurant,
        )
        db.session.add(food)
        db.session.commit()
        return food_schema.dump(food), 201
    else:
        return {'error': f'Restaurant with id {restaurant_id} not found'}, 404
    

@foods_bp.route('/<int:food_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_food(food_id):
    stmt = db.select(Food).filter_by(id=food_id)
    food = db.session.scalar(stmt)
    if food:
        db.session.delete(food)
        db.session.commit()
        return {'msg': f'Food {food.name} deleted successfully'}
    else:
        return {'error': f'Food with id {food_id} not found'}, 404
    

@foods_bp.route('/')
@jwt_required()
def get_all_foods():
    stmt = db.select(Food).order_by(Food.name.asc())
    foods = db.session.scalars(stmt)
    return foods_schema.dumps(foods)


@foods_bp.route('/<int:food_id>')
@jwt_required()
def get_one_food(food_id):
    stmt = db.select(Food).filter_by(id=food_id)
    food = db.session.scalar(stmt)
    return food_schema.dumps(food)


@foods_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@admin_required
def update_food(id):
    body_data = food_schema.load(request.get_json(), partial=True)
    stmt = db.select(Food).filter_by(id=id)
    food = db.session.scalar(stmt)
    if food:
        food.name = body_data.get('name') or food.name
        food.description = body_data.get('description') or food.description
        food.price = body_data.get('price') or food.price
        db.session.commit()
        return food_schema.dump(food)
    else:
        return {'error': f'Food with id {id} not found'}, 404