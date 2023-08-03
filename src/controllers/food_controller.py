from flask import Blueprint, request
from init import db, ma
from models.food import Food, food_schema, foods_schema
from models.restaurant import Restaurant, restaurant_schema, restaurants_schema
from models.user import User
from controllers.review_controller import reviews_bp
from controllers.auth_controller import admin_required
from flask_jwt_extended import jwt_required

foods_bp = Blueprint('foods', __name__, url_prefix='/foods')
foods_bp.register_blueprint(reviews_bp, url_prefix='/<int:food_id>/reviews')


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
        return {'error': f'Restaurant with id {restaurant_id} not found'}
    

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