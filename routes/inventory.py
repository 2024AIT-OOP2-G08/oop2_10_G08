from flask import Blueprint, render_template, request, redirect, url_for
from models import Product, Order

# Blueprintの作成
inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory_bp.route('/')
def list():
    # 製品一覧を取得
    products = Product.select()
    return render_template('inventory_list.html', title='在庫一覧', products=products)

@inventory_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit(product_id):
    """
    在庫の編集
    """
    product = Product.get_or_none(Product.id == product_id)
    if not product:
        return redirect(url_for('product.list'))

    if request.method == 'POST':
        product.name = request.form['name']
        product.quantity = request.form['quantity']
        product.save()
        return redirect(url_for('inventory.list'))

    return render_template('inventory_edit.html', product=product)