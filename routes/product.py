from flask import Blueprint, render_template, request, redirect, url_for
from models import Product

# Blueprintの作成
product_bp = Blueprint('product', __name__, url_prefix='/products')


@product_bp.route('/')
def list():
    products = Product.select()
    return render_template('product_list.html', title='製品一覧', items=products)


@product_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        Product.create(name=name, price=price)
        return redirect(url_for('product.list'))
    
    return render_template('product_add.html')


@product_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit(product_id):
    product = Product.get_or_none(Product.id == product_id)
    if not product:
        return redirect(url_for('product.list'))

    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.save()
        return redirect(url_for('product.list'))

    return render_template('product_edit.html', product=product)


@product_bp.route('/dash-pro')
def dashboard():
    # 今月の売上を計算
    sales_data = []
    products = Product.select()
    
    for product in products:
        # 各製品の売上数と価格を取得
        quantity_sold = product.quantity
        price = product.price
        sales_amount = quantity_sold * price
        
        sales_data.append({
            'name': product.name,
            'quantity': quantity_sold,
            'price': price,
            'sales_amount': sales_amount
        })
    
    return render_template('index.html', 
                         title='製品別売上ダッシュボード',
                         sales_data=sales_data)
