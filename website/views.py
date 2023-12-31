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

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html",
                           user=current_user,
                           TopStores=get_all_stores(),
                           user_store_favorite=user_favorite_store(
                               current_user),
                           get_reccomended_stores=get_reccomended_stores(),
                           all_reviews=get_all_reviews(),)


@views.route('/stores', methods=['GET', 'POST'])
def stores():
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        logo = request.files['logo']
        description = request.form.get('description')
        store_link = request.form.get('store_link')
        pictures = request.files.getlist('pictures[]')

        with db.session.no_autoflush:
            new_store = Store(
                name=name,
                address=address,
                description=description,
                store_link=store_link,
                is_online=bool(store_link),
                is_local=bool(address),
            )

            # Save the new store to the database
            db.session.add(new_store)
            current_user.contributed_stores.append(new_store)
            if logo:
                filename = secure_filename(logo.filename)
                save_path = os.path.join('website/static/images', filename)
                while os.path.exists(save_path):
                    random_string = ''.join(random.choices(
                        string.ascii_lowercase + string.digits, k=8))
                    filename = secure_filename(f"{random_string}_{filename}")
                    save_path = os.path.join('website/static/images', filename)

                logo.save(save_path)
                new_store.logo = filename

            # Save the pictures files to the database
            for picture in pictures:
                filename = secure_filename(picture.filename)
                save_path = os.path.join('website/static/images', filename)
                while os.path.exists(save_path):
                    random_string = ''.join(random.choices(
                        string.ascii_lowercase + string.digits, k=8))
                    filename = secure_filename(f"{random_string}_{filename}")
                    save_path = os.path.join('website/static/images', filename)

                picture.save(save_path)
                new_image = Image(name=filename)
                new_store.images.append(new_image)

        db.session.commit()
        return redirect(url_for('views.store_details', store=new_store.id))
    else:
        pass
    return render_template("stores.html", user=current_user, stores=get_all_stores())


@views.route('/reviews')
def reviews():
    return render_template("reviews.html", user=current_user)


@views.route('/store/<string:store>', methods=['GET', 'POST'])
def store_details(store):
    split_store = store.split('?')
    store = split_store[0]
    if request.method == 'POST':
        # Get the form data from the request
        review_title = request.form.get('review_title')
        review_text = request.form.get('review')
        # Get the rating values from the form, similar to how you did it for the store creation form
        # For example:
        review_stars = int(request.form.get('store_experience'))
        review_reliability = int(request.form.get('reliability'))
        review_affordability = int(request.form.get('affordability'))
        review_shipping = int(request.form.get('shipping'))
        review_support = int(request.form.get('support'))

        review_images = request.files.getlist('reviewimages[]')
        # Assuming you have a logged-in user, get the user ID
        # Replace 'current_user_id' with the ID of the logged-in user
        current_user_id = current_user.id
        review_user = User.query.filter_by(id=current_user_id).first()

        # Get the store ID from the URL parameter
        # 'store' is the parameter name specified in the route
        store_id = store

        # Create a new Review object with the form data
        review = Review(
            text=review_text,
            stars=review_stars,
            user_id=current_user_id,
            store_id=store_id,
            reliability=review_reliability,
            affordability=review_affordability,
            shipping=review_shipping,
            support=review_support,
            title=review_title,
            # Using overall rating for store_experience, change as needed
            store_experience=review_stars,
            username=review_user.username,
            userprofile_pic=review_user.profile_pic
        )

        # Save the review to the database
        db.session.add(review)
        db.session.commit()
        # Handle the review images uploads here and associate them with the review if needed

        # Redirect to the same store details page after submitting the review
        for image in review_images:
            filename = secure_filename(image.filename)
            save_path = os.path.join('website/static/images', filename)
            while os.path.exists(save_path):
                random_string = ''.join(random.choices(
                    string.ascii_lowercase + string.digits, k=8))
                filename = secure_filename(f"{random_string}_{image.filename}")
                save_path = os.path.join('website/static/images', filename)

            image.save(save_path)
            # Save image data as LargeBinary
            review_image = ReviewImage(
                url=filename, review_id=review.id)
            db.session.add(review_image)

        # get the avg of the reviews and divide it by the number of reviews in that store
        for review in Review.query.filter_by(store_id=store_id):
            avg = (review.stars + review.reliability +
                   review.affordability + review.shipping + review.support) / 5
            review.overall_rating = avg

        # get the overlay rating of the store by dividing the overall rating by the number of reviews in a store
        store_1 = Store.query.filter_by(id=store_id).first()
        num_reviews = Review.query.filter_by(store_id=store_id).count()

        # Calculate the overall rating by summing up all review stars and dividing by the number of reviews
        overall_rating = Review.query.with_entities(
            func.sum(Review.stars)).filter_by(store_id=store_id).scalar()
        if overall_rating is None:
            overall_rating = 0
        else:
            overall_rating /= num_reviews

        # Set the overall_rating of the store
        store_1.overall_rating = overall_rating

        # Commit the changes to the database
        db.session.commit()
        assign_tags_to_store(store_id, "reliability")
        assign_tags_to_store(store_id, "affordability")
        assign_tags_to_store(store_id, "shipping")
        assign_tags_to_store(store_id, "support")
        assign_tags_to_store(store_id, "store_experience")
        
        db.session.commit()
        funcstore = Store.query.get(store_id) 
        db.session.refresh(funcstore)
        return redirect(url_for('views.store_details', store=store_id))
    else:
        
        q = request.args.get('q')
        filter_reviwes = None  # Initialize the variable outside the else block

        if q:
            has_query = True
            filter_reviwes = Review.query.filter(
                Review.stars.contains(q)
            )
        else:
            has_query = False
    return render_template('store.html',
                           store=Store.query.get(store),
                           user=current_user,
                           does_user_hav_review=does_user_hav_review(
                               current_user, store_id=store),
                           user_review=get_user_reviews(current_user, store),
                           users=User.query.all(),
                           user_profile_pic_has=user_has_profile_picture(),
                           user_store_favorite=is_store_favorite(
                               store_id=store),
                           store_rating_brackdown=get_store_rating_breakdown(
                               store_id=store),
                           has_query=has_query,
                           filter_reviwes=filter_reviwes,
                           
                           )


@views.route('/store/stores')
def storered():
    return redirect(url_for('views.stores'))


@views.route('user_profile/<string:user>', methods=['GET', 'POST'])
@login_required
def user_profile(user):
    if request.method == 'POST':
        current_user.username = request.form['username']
        current_user.first_name = request.form['firstname']
        current_user.last_name = request.form['lastname']
        current_user.email = request.form['email']
        profile_pic = request.files['profile_pic']

        filename = secure_filename(profile_pic.filename)
        save_path = os.path.join('website/static/images', filename)
        while os.path.exists(save_path):
            random_string = ''.join(random.choices(
                string.ascii_lowercase + string.digits, k=8))
            filename = secure_filename(
                f"{random_string}_{profile_pic.filename}")
            save_path = os.path.join('website/static/images', filename)
        current_user.profile_pic = filename
        db.session.commit()
    else:
        pass
    is_logged_in_user = (current_user.id == int(user))
    print(is_logged_in_user)
    return render_template('user.html', user=current_user,
                           user_profile=user,
                           is_logged_in_user=is_logged_in_user,
                           user_profile_pic_has=user_has_profile_picture(),)

@views.route('suscess', methods=['GET'])
def suscess():
    return render_template('success.html' , user=current_user)
