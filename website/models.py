from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import func 
from sqlalchemy.orm import column_property
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property

Favorites = db.Table(
    'favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('store_id', db.Integer, db.ForeignKey('store.id'))
)

Contributors = db.Table(
    'contributors',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('store_id', db.Integer, db.ForeignKey('store.id'))
)


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    address = db.Column(db.String(120))
    logo = db.Column(db.String(1000))
    description = db.Column(db.String(4000))
    images = db.relationship('Image', backref='store')
    reviews = db.relationship('Review', backref='store')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    store_link = db.Column(db.String(120))
    is_online = db.Column(db.Boolean, default=False)
    tags = db.relationship('Tag', backref='store')
    is_local = db.Column(db.Boolean)
    owner = db.relationship('User', backref='owned_store', uselist=False)
    themes = db.relationship('Themes', backref='store')
    overall_rating = db.Column(db.Integer)
    @hybrid_property
    def avg_reliability(self):
        reviews = Review.query.filter_by(store_id=self.id)  
        total = 0

        for review in reviews:
            total += review.reliability

        return total / len(reviews)

    @avg_reliability.expression
    def avg_reliability(cls):
        return (db.select([db.func.avg(Review.reliability)])
                .where(Review.store_id == cls.id)
                .label("avg_reliability")
                )
    @hybrid_property
    def avg_affordability(self):
        reviews = Review.query.filter_by(store_id=self.id)  
        total = 0

        for review in reviews:
            total += review.reliability

        return total / len(reviews)

    @avg_affordability.expression
    def avg_affordability(cls):
        return (db.select([db.func.avg(Review.reliability)])
                .where(Review.store_id == cls.id)
                .label("avg_reliability")
                )
    @hybrid_property
    def avg_shipping(self):
        reviews = Review.query.filter_by(store_id=self.id)  
        total = 0

        for review in reviews:
            total += review.reliability

        return total / len(reviews)

    @avg_shipping.expression
    def avg_shipping(cls):
        return (db.select([db.func.avg(Review.reliability)])
                .where(Review.store_id == cls.id)
                .label("avg_reliability")
                )
    @hybrid_property
    def avg_support(self):
        reviews = Review.query.filter_by(store_id=self.id)  
        total = 0

        for review in reviews:
            total += review.reliability

        return total / len(reviews)

    @avg_support.expression
    def avg_support(cls):
        return (db.select([db.func.avg(Review.reliability)])
                .where(Review.store_id == cls.id)
                .label("avg_reliability")
                )
    @hybrid_property
    def avg_store_experience(self):
        reviews = Review.query.filter_by(store_id=self.id)  
        total = 0

        for review in reviews:
            total += review.reliability

        return total / len(reviews)

    @avg_store_experience.expression
    def avg_store_experience(cls):
        return (db.select([db.func.avg(Review.reliability)])
                .where(Review.store_id == cls.id)
                .label("avg_reliability")
                )
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    username = db.Column(db.String(120), unique=False)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    profile_pic = db.Column(db.String(120))
    profile_pic_data = db.Column(db.LargeBinary)
    time_created = db.Column(db.DateTime(timezone=True), default=func.now())
    reviews = db.relationship('Review', backref='user')
    settings = db.relationship('SettingsModel', backref='user')
    owned_id = db.Column (db.Integer, db.ForeignKey('store.id'))
    favorite_stores = db.relationship(
        'Store', secondary=Favorites, backref='followers')
    contributed_stores = db.relationship(
        'Store', secondary=Contributors, backref='contributors_stores')
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    images = db.relationship('ReviewImage', backref='review')
    text = db.Column(db.String(300))
    title = db.Column(db.String(120))
    stars = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reliability = db.Column(db.Integer)
    affordability = db.Column(db.Integer)
    shipping = db.Column(db.Integer)
    support = db.Column(db.Integer)
    store_experience = db.Column(db.Integer)
    username = db.Column(db.String(120))
    userprofile_pic = db.Column(db.String(120))
    overall_rating = db.Column(db.Integer)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200))
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    name=db.Column(db.String(200))

class ReviewImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200))
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'))
    data = db.Column(db.LargeBinary)

class SettingsModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receive_email = db.Column(db.Boolean)
    is_owner = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    Ratings = db.relationship('Rating', backref='tag')
    

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = column_property(db.Column(db.Float))
    Tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
class Themes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))