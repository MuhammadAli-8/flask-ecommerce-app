from flask import render_template, Blueprint
from shop.models import Product
from datetime import datetime, timedelta


main=Blueprint('main', __name__)






@main.route('/')
@main.route('/home')
def home():
    
    # Calculate the date two weeks ago from now
    time_period = datetime.utcnow() - timedelta(hours=48)

    # Query for products created within the last two weeks
    recent_products = Product.query.order_by(Product.created_at.desc()).limit(20).all()
    samsung_products = Product.query.filter(Product.brand == 'samsung').order_by(Product.created_at.desc()).limit(20).all()
    apple_products = Product.query.filter(Product.brand == 'apple').order_by(Product.created_at.desc()).limit(20).all()
    laptop_products = Product.query.filter(Product.category == 'laptop').order_by(Product.created_at.desc()).limit(20).all()
    headphone_products = Product.query.filter(Product.category == 'headphone').order_by(Product.created_at.desc()).limit(20).all()
    watch_products = Product.query.filter(Product.category == 'watch').order_by(Product.created_at.desc()).limit(20).all()
    camera_products = Product.query.filter(Product.category == 'camera').order_by(Product.created_at.desc()).limit(20).all()
    
    
    return render_template('home.html', title = 'Home', recent_products=recent_products, samsung_products=samsung_products,
                           apple_products=apple_products, headphone_products=headphone_products, watch_products=watch_products,
                           camera_products=camera_products, laptop_products=laptop_products)


@main.route('/about')
def about():
    return render_template('about.html', title = 'about')