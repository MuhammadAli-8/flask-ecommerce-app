from shop import db
from flask import render_template, redirect, flash, url_for, request, Blueprint
from shop.orders.forms import CheckoutForm
from shop.models import Product, CartItem, Order, OrderItem
from flask_login import current_user, login_required
from datetime import datetime



orders=Blueprint('orders', __name__)



@orders.route('/cart', methods=['GET','POST'])
@login_required
def view_cart():
    
    cart_items=CartItem.query.filter_by(user_id=current_user.id).all()
    return render_template('cart.html', cart_items=cart_items)

@orders.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):

    product = Product.query.get_or_404(product_id)
    cartitem=CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if cartitem:
        cartitem.quantity += 1
    else:
        new_cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(new_cart_item)
    
    db.session.commit()
    
    flash('Product added to cart successfully', 'success')
    return redirect(url_for('orders.view_cart'))


@orders.route('/update_cart/<int:cart_item_id>', methods=['POST'])
@login_required
def update_cart(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    new_quantity = request.form.get('quantity', '0')  # Default to '0' if no value is provided
    if int(new_quantity) <= cart_item.product.stock:
        try:
            new_quantity = int(new_quantity)
        except ValueError:
            new_quantity = 0  # or handle the error as needed
        if new_quantity > 0:
            cart_item.quantity = new_quantity
        else:
            db.session.delete(cart_item)
        db.session.commit()
        flash('Cart updated successfully', 'success')
    else:
        flash('There are no enough items in stock!', 'danger')
    
    return redirect(url_for('orders.view_cart'))


@orders.route('/remove_from_cart/<int:cart_item_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart', 'success')
    return redirect(url_for('orders.view_cart'))



@orders.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items=CartItem.query.filter_by(user_id=current_user.id).all()
    cart_total = 0
    cart_total = sum(item.product.price * item.quantity for item in cart_items)
    
    form=CheckoutForm()
    
    if request.method == 'POST':
        # Process the form data and create the order
        order = Order(
            user_id=current_user.id,
            total=cart_total,
            status='Pending',
            created_at=datetime.utcnow(),
            email=form.email.data,
            phone=form.phone.data,
            name=form.full_name.data,
            address=f'{form.address.data} {form.city.data}',
            zip_code=form.zip_code.data,
            note=form.order_notes.data,
            payment_method=form.payment_method.data
        )
        db.session.add(order)
        db.session.commit()

        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
            )
            item.product.stock-=item.quantity
            db.session.add(order_item)
            db.session.delete(item)
        db.session.commit()

        flash('Order placed successfully!', 'success')
        
        
        
        return redirect(url_for('main.home'))

    return render_template('checkout.html', form=form)


@orders.route('/account/orders')
@login_required
def view_orders():
    orders=Order.query.filter_by(user_id=current_user.id).all()
    return render_template('view_orders.html', orders=orders)
