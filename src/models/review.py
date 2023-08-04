from init import db, ma 
from marshmallow import fields

# Create Review class as a model using extension of db.Model
# Rating is out of 5 stars
class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float, nullable=False)
    review_title = db.Column(db.String(100), nullable=False)
    review_text = db.Column(db.Text)
    timestamp = db.Column(db.Date) # Date user wrote the review

    
    # Define relationships
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'), nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    food = db.relationship('Food', back_populates='reviews') 
    user = db.relationship('User', back_populates='reviews')
   
# Initialise Review schema and nest food and user
class ReviewSchema(ma.Schema):
    food = fields.Nested('FoodSchema', exclude=['reviews'])
    user = fields.Nested('UserSchema', only=['username'])

    class Meta:
        fields = ('id', 'rating', 'review_title', 'review_text', 'timestamp', 'food', 'user')
        ordered = True

# Initialize schemas for retrieving one or multiple user entries
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)