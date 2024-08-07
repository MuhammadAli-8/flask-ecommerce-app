from shop import db
from shop.models import Product, CartItem
from flask_login import current_user
from flask import current_app

@current_app.context_processor
def inject_common_data():
    # Get distinct brands
    brands = [brand[0] for brand in db.session.query(Product.brand.distinct()).all()]
    
    # Get distinct categories
    categories = [category[0] for category in db.session.query(Product.category.distinct()).all()]
    
    # Define is_admin function
    def is_admin(user):
        return user.role == 'admin' if user else False

    # Get cart items and calculate total
    cart_items = []
    cart_total = 0
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        cart_total = sum(item.product.price * item.quantity for item in cart_items)

    return dict(
        brands=brands,
        is_admin=is_admin,
        categories=categories,
        cart_items=cart_items,
        cart_total=cart_total
    )
