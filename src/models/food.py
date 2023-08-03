from init import db, ma 
from marshmallow import fields

class Food(db.Model):
    __tablename__ = 'foods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    average_rating = db.Column(db.Float, default=0.0)
    
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False) #?

    restaurant = db.relationship('Restaurant', back_populates='foods')
    reviews = db.relationship('Review', back_populates='food', cascade='all, delete')
   

class FoodSchema(ma.Schema):
    restaurant = fields.Nested('RestaurantSchema', only=['id', 'name', 'type'])
    reviews = fields.List(fields.Nested('ReviewSchema', exclude=['food']))

    class Meta:
        fields = ('id', 'name', 'description', 'price', 'average_rating', 'restaurant', 'reviews')
        ordered = True


food_schema = FoodSchema()
foods_schema = FoodSchema(many=True)