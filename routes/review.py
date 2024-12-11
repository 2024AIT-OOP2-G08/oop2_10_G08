from flask import Blueprint, render_template, request, redirect, url_for
from models import Review, User, Product
from datetime import datetime



# Blueprintの作成
review_bp = Blueprint('review', __name__, url_prefix='/reviews')



@review_bp.route('/', methods=['GET', 'POST'])
def list():
    review = Review.select()
    return render_template("review_list.html", title="レビュー", items = review)

@review_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        user_id = request.form['user_id']
        product_id = request.form['product_id']
        review_count = request.form['review_count']
        review_comment = request.form['review_comment']
        Review.create(user=user_id, product=product_id, review_count=review_count, review_comment=review_comment)
        return redirect(url_for('review.list'))
      
    users = User.select()
    products = Product.select()
    return render_template('review_add.html', users=users, products=products)

@review_bp.route('/edit/<int:review_id>', methods=['GET', 'POST'])
def edit(review_id):
    review = Review.get_or_none(Review.id == review_id)
    if not review:
        return redirect(url_for('review.list'))

    if request.method == 'POST':
        review.user = request.form['user_id']
        review.product = request.form['product_id']
        review.review_count = request.form['review_count']
        review.review_comment = request.form['review_comment']
        review.save()
        return redirect(url_for('review.list'))

    users = User.select()
    products = Product.select()
    return render_template('review_edit.html', review=review, users=users, products=products)
