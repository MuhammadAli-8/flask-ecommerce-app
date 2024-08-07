from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from shop.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    from shop.users.routes import users
    from shop.products.routes import products
    from shop.orders.routes import orders
    from shop.main.routes import main
    from shop.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(products)
    app.register_blueprint(orders)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    
    from shop.models import Product, CartItem
    
    # Import and register the context processor
    @app.context_processor
    def inject_common_data():
        # Get distinct brands
        brands = [brand[0] for brand in db.session.query(Product.brand.distinct()).all()]
        recent_products =  Product.query.order_by(Product.created_at.desc()).limit(20).all()
        
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
            cart_total=cart_total,
            recent_products=recent_products
        )
    
    return app