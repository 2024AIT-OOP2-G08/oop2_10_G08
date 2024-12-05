from flask import Blueprint, render_template, request, redirect, url_for
from models import Product, InventoryManagement

# Blueprintの作成
inventoryManagement_bp = Blueprint('inventoryManagement', __name__, url_prefix='/inventoryManagements')

@inventoryManagement_bp.route('/')
def list():
    inventoryManagements = InventoryManagement.select()
    return render_template('inventory_list.html', title='在庫一覧', items=inventoryManagements)

@inventoryManagement_bp.route('/edit/<int:inventoryManagement_id>', methods=['GET', 'POST'])
def edit(inventoryManagement_id):
    inventoryManagement = InventoryManagement.get_or_none(InventoryManagement.id == inventoryManagement_id)
    if not inventoryManagement:
        return redirect(url_for('inventoryManagement.list'))

    if request.method == 'POST':
        inventoryManagement.product = request.form['product_id']
        inventoryManagement.quantity = request.form['quantity']
        inventoryManagement.save()
        return redirect(url_for('inventoryManagement.list'))

    products = Product.select()
    return render_template('inventory_edit.html', inventoryManagement=inventoryManagement, products=products)
