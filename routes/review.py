from flask import Blueprint, render_template, request, redirect, url_for
from models import Review, User, Product
from datetime import datetime

# Blueprintの作成
review_bp = Blueprint('reveiw', __name__, url_prefix='/reveiws')

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
    return render_template('reviews_add.html', users=users, products=products)
