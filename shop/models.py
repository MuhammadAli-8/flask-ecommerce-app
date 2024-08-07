from shop import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(50), nullable=False, default='customer')
    
    orders = db.relationship('Order', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    cartitems = db.relationship('CartItem', backref='user', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.phone}')"
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(240), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    price_before = db.Column(db.Float, nullable=True)
    stock = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False, default='Other')
    brand = db.Column(db.String(50), nullable=False, default='Other')
    color = db.Column(db.String(50), nullable=True)
    size = db.Column(db.String(50), nullable=True)
    weight = db.Column(db.Float, nullable=True)
    camera = db.Column(db.String(120), nullable=True)
    screen = db.Column(db.String(50), nullable=True)
    ram = db.Column(db.String(50), nullable=True)
    cpu = db.Column(db.String(120), nullable=True)
    gpu = db.Column(db.String(50), nullable=True)
    os = db.Column(db.String(50), nullable=True)
    storage = db.Column(db.String(120), nullable=True)
    battery = db.Column(db.String(50), nullable=True)
    note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    rating = db.Column(db.Float, nullable=True, default=0)
    
    
    orderitems = db.relationship('OrderItem', backref='product', lazy=True)
    cartitems = db.relationship('CartItem', backref='product', lazy=True)
    reviews = db.relationship('Review', backref='product', lazy=True)
    pictures = db.relationship('ProductPicture', backref='product', lazy=True)
    
    def __repr__(self):
        return f"Product('{self.name}', '{self.price}', '{self.category}')"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    name = db.Column(db.String(120))
    address = db.Column(db.Text)
    zip_code = db.Column(db.String(20))
    payment_method = db.Column(db.String(50))
    note = db.Column(db.Text)
    
    items = db.relationship('OrderItem', backref='order', lazy=True)
    
    def __repr__(self):
        return f"Order('{self.user_id}', '{self.total}', '{self.status}')"
    

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"Item('{self.id}', '{self.quantity}', '{self.quantity}')"
    

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def __repr__(self):
        return f"Review('{self.id}', '{self.user_id}', '{self.product_id}')"
    
class ProductPicture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.Text, nullable=False)
    
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    
    def __repr__(self):
        return f"Picture('{self.id}', '{self.product_id}', '{self.img_url}')"
    
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Cart Item( '{self.id}', '{self.product_id}', '{self.user_id}')"