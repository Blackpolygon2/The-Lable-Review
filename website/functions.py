from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user , AnonymousUserMixin
from .models import Store, Review, User, Image, ReviewImage, SettingsModel, Tag
import os
from flask import request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from . import db
import json
import random
import string
from sqlalchemy import func, desc

# this tekes in the store id and the reviwes and rturnes the avg for them to make a tag

def assign_tags_to_store(store_id, tag):
    store = Store.query.filter_by(id=store_id).first()
    VALID_TAGS = ["reliability", "affordability", "shipping", "support", "store_experience"]
    if store.tags:
        for tag in store.tags.name:
            for valid_tag in VALID_TAGS:
                if tag == valid_tag:
                    this_tag = Tag.query.filter_by(store_id=store_id, name=valid_tag).first()
                    if store.avg_reliability >= 4:
                        this_tag.Ratings = store.avg_reliability
                    else:
                        db.session.delete(this_tag)
                else:
                    if store.avg_reliability >= 4:
                        new_tag = Tag(name=valid_tag, store_id=store_id, Ratings=store.avg_reliability)
                        db.session.add(new_tag)


def user_favorite_store(user):
    if isinstance(user, AnonymousUserMixin):
        return None
    else:
        store = []
        for favstore in user.favorite_stores:
            store.append(favstore)
    return store
def get_rating_percentages(rating_counts):
  total = sum(rating_counts)
  return [
      (count / total * 100 if count > 0 else 0)
      for count in rating_counts
  ]

def get_store_rating_breakdown(store_id):
  
  # Get all reviews for store
  reviews = Review.query.filter_by(store_id=store_id).all()

  # Initialize rating count list
  rating_counts = [0, 0, 0, 0, 0]

  # Tally review ratings
  for review in reviews:
    rating_counts[review.stars - 1] += 1

  # Calculate percentages  
  rating_pcts = get_rating_percentages(rating_counts)

  return rating_pcts

def user_has_profile_picture():
    if isinstance(current_user, AnonymousUserMixin):
        return'none'
    else:    
        user = User.query.filter_by(id=current_user.id).first()
        if user.profile_pic:
            return "block"
        else:
            return "none"


def is_store_favorite(store_id):
    if isinstance(current_user, AnonymousUserMixin):
        return '0'
    store = Store.query.filter_by(id=store_id).first()
    if store in current_user.favorite_stores:
        return "1"
    else:
        return "0"


def get_all_stores():
    stores = Store.query.all()
    return stores


def get_top_stores():
    top_stores = Store.query.order_by(
        desc(Store.overall_rating)).limit(10).all()
    print(top_stores)
    return top_stores
def get_reccomended_stores():
    top_stores = Store.query.order_by(
        desc(Store.overall_rating)).limit(20).all()
    print(top_stores)
    return top_stores


def does_user_hav_review(user, store_id):
    if isinstance(user, AnonymousUserMixin):
        return False    
    else:    
        review = Review.query.filter_by(user_id=user.id, store_id=store_id).first()
        if review:
            return True
        else:
            return False
    
def get_all_reviews():
    reviews = Review.query.order_by(Review.created_at.desc()).limit(20).all()
    return reviews
def get_user_reviews(user , store_id):
    if isinstance(user, AnonymousUserMixin):
        return None
    else:
        reviews = Review.query.filter_by(user_id=user.id , store_id=store_id).first()
        return reviews
    pass
