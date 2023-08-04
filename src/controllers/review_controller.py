from flask import Blueprint, request
from init import db, ma
from models.food import Food, food_schema, foods_schema
from models.review import Review, review_schema, reviews_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime  import date

# Create blueprint. Registered in food.py
# Prefix for all routes is /foods/<int:food_id>/reviews
reviews_bp = Blueprint('reviews', __name__)

# Get all reviews under a certain food
#/foods/<int:food_id>/reviews
@reviews_bp.route('/')
@jwt_required()
def get_reviews(food_id):
    stmt = db.select(Review).filter_by(food_id=food_id)
    reviews = db.session.scalars(stmt)
    return reviews_schema.dump(reviews)


# Create a review for a food
# /foods/<int:food_id>/reviews
@reviews_bp.route('/', methods=['POST'])
@jwt_required()
def create_review(food_id):
    body_data = request.get_json()
    stmt = db.select(Food).filter_by(id=food_id)
    food = db.session.scalar(stmt)
    if food:
        review = Review (
            rating=body_data.get('rating'),
            review_title=body_data.get('review_title'),
            review_text=body_data.get('review_text'),
            timestamp=date.today(),
            user_id=get_jwt_identity(),
            food=food
        )
        db.session.add(review)
        db.session.commit()
        return review_schema.dump(review), 201
    else:
        return {'error': f'Food with id {food_id} not found'}, 404


# Users only have permission to delete their own reviews
# foods/<int:food_id>/reviews/<int:review_id>
@reviews_bp.route('/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(food_id, review_id):
    user_id = get_jwt_identity()
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    if review and int(review.user_id) == int(user_id):
        db.session.delete(review)
        db.session.commit()
        return {'msg': f'Review with title {review.review_title} has been deleted successfully'}
    elif review and int(review.user_id) != int(user_id):
        return {'error': f'Unauthorized to delete review with id {review_id}'}, 401
    else:
        return {'error': f'Could not find review with id {review_id} to delete'}, 404

# Users edit their own review
# foods/<int:food_id>/reviews/<int:review_id>
@reviews_bp.route('/<int:review_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_review(food_id, review_id):
    user_id = get_jwt_identity()
    body_data = review_schema.load(request.get_json(), partial=True)
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    if int(review.user_id) != int(user_id):
        return {'error': 'Only review writer authorized to update'}
    if review:
        review.rating = body_data.get('rating') or review.rating
        review.review_title = body_data.get('review_title') or review.review_title
        review.review_text = body_data.get('review_text') or review.review_text
        review.timestamp = date.today()
        db.session.commit()
        return review_schema.dump(review)
    else:
        return {'error': f'Card with id {id} not found'}, 404
    


