from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Store, Review, User, Image, ReviewImage, SettingsModel, Tag, Themes
import os
from flask import request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from . import db
import json
import random
import string
from sqlalchemy import func, desc, or_, and_
from .functions import *
from sqlalchemy.orm import sessionmaker, scoped_session

api = Blueprint('api', __name__)

@api.route('/delete_item_review', methods=['POST'])
def delete_item_review():
    review = json.loads(request.data)
    review_id = review['reviewid']
    review = Review.query.filter_by(id=review_id).first()
    db.session.delete(review)
    db.session.commit()
    
    return jsonify({})
@api.route('/delete_store', methods=['POST'])
def delete_store():
    store = json.loads(request.data)
    storeid = store['storeid']
    store = Store.query.filter_by(id=storeid).first()
    db.session.delete(store)
    db.session.commit()
    
    return jsonify({})

@api.route('add_to_favorites', methods=['POST'])
def add_to_favorites():
    # this function expects a JSON from the INDEX.js file
    store = json.loads(request.data)
    storeId = store['storeid']
    store = Store.query.get(storeId)
    if store in current_user.favorite_stores:
        current_user.favorite_stores.remove(store)
    else:
        current_user.favorite_stores.append(store)

    db.session.commit()

    return jsonify({})

@api.route('/search', methods=['GET'])
def search():
    q = request.args.get('q')
    stores = Store.query.filter(Store.name.contains(q)).all()
    return render_template("search.html",  qstores=stores, user=current_user)


@api.route('/adminsearch', methods=['GET'])
def adminsearch():
    q = str(request.args.get('q'))
    q = q.split('|')
    if q[1] == "reviews":
        reviews = Review.query.filter(
            or_(
                Review.title.contains(q[0]),
                Review.text.contains(q[0]),
                Review.username.contains(q[0])
            )
        ).all()
        return render_template("adminsearch.html", show=reviews, user=current_user, what="reviews")
    if q[1] == "stores":
        stores = Store.query.filter(Store.name.contains(q[0])).all()
        return render_template("adminsearch.html", show=stores, user=current_user, what="stores")
    if q[1] == "users":
        user = User.query.filter(User.username.contains(q[0])).all()
        return render_template("adminsearch.html", show=user, user=current_user, what="users")

    return render_template("adminsearch.html", user=current_user)

    