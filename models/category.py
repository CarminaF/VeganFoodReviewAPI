from init import db, ma 
from marshmallow import fields

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String)
    description = db.Column(db.String)

    restaurants = db.relationship('Restaurant', back_populates='category')

class CategorySchema(ma.Schema):
    restaurant = fields.Nested('RestaurantSchema', exclude=['category'])

    class Meta:
        fields = ('id', 'category', 'description', 'restaurants')

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)