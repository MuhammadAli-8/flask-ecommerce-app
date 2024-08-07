from shop import db
from flask import render_template, redirect, flash, url_for, request, abort, Blueprint
from shop.products.forms import AddProductForm, ReviewForm, UpdateProductForm
from shop.models import Product, ProductPicture, Review
from flask_login import current_user, login_required
from datetime import datetime
from sqlalchemy import func
from collections import Counter
from shop.products.utils import add_pictures, ratings



products=Blueprint('products', __name__)

@products.route("/product/new", methods = ['GET', 'POST'])
@login_required
def add_product():
    if current_user.role!='admin':
        abort(403)
    form = AddProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            price_before=form.price_before.data,
            stock=form.stock.data,
            category=form.category.data,
            brand=form.brand.data,
            color=form.color.data,
            size=form.size.data,
            weight=form.weight.data,
            camera=form.camera.data,
            screen=form.screen.data,
            ram=form.ram.data,
            cpu=form.cpu.data,
            gpu=form.gpu.data,
            os=form.os.data,
            storage=form.storage.data,
            battery=form.battery.data,
            note=form.note.data,
            created_at=datetime.utcnow()
        )
        db.session.add(product)
        db.session.commit()
        for img in form.pictures.data:
            picture_name = add_pictures(img)
            picture = ProductPicture(img_url=picture_name, product=product)
            db.session.add(picture)
        db.session.commit()
        flash('The Product has been Added Successfully!', 'success')
        return redirect(url_for('products.product', product_id=product.id))
    return render_template('add_product.html', title='add a product', form=form)



@products.route("/shop/<int:product_id>", methods = ['GET', 'POST'])
def product(product_id):
    product = Product.query.filter_by(id=product_id).first_or_404()
    pictures = ProductPicture.query.filter_by(product_id=product.id)
    specifications = {
            "Color": product.color,
            "Size": product.size,
            "Weight": product.weight,
            "Camera": product.camera,
            "Screen": product.screen,
            "RAM": product.ram,
            "CPU": product.cpu,
            "GPU": product.gpu,
            "OS": product.os,
            "Storage": product.storage,
            "Battery": product.battery,
        }
    
    
    form=ReviewForm()
    if form.validate_on_submit():
        review=Review(
        user_id=current_user.id,
        product_id=product.id,
        rating=int(form.rating.data),
        review=form.review.data,
        created_at=datetime.utcnow()
        )
        db.session.add(review)
        db.session.commit()
        flash('Your Review has been Recorded', 'success')
    
    
    reviews = Review.query.filter_by(product_id=product.id)
    rating=ratings(reviews)
    product.rating=rating
    db.session.commit()
    
    one_rating_count = {}
    for i in range(1, 6):
        one_rating_count[i] = Review.query.filter_by(product_id=product.id, rating=i).count()
    
    rating_count = Review.query.filter_by(product_id=product.id).count()
    
    actual_reviews=Review.query.filter_by(product_id=product.id).limit(16).all()
    
    # Related Products
    related_products = Product.query.filter_by(category=product.category).order_by(func.random()).limit(4).all()
    
    return render_template('product.html', title=product.name, product=product, form=form,
                          pictures=pictures, specifications=specifications
                          , reviews=reviews, rating=rating, one_rating_count=one_rating_count,
                          rating_count=rating_count, actual_reviews=actual_reviews,
                          related_products=related_products)



@products.route('/brands/<string:brand_name>', methods=['GET', 'POST'])
def brand(brand_name):
    
    # Retrieve filters from request parameters
    categories = request.args.getlist('category')
    price_min = request.args.get('price_min', type=float)
    price_max = request.args.get('price_max', type=float)
    
    # Sorting parameters
    sort_by = request.args.get('sort_by', 'price_asc')  # Default sort option
    per_page = request.args.get('per_page', 24, type=int)  # Default per page option
    
    # Define default sort_criteria to avoid NoneType error
    sort_criteria = Product.price.asc()
    
    if sort_by == 'price_desc':
        sort_criteria = Product.price.desc()
    elif sort_by == 'avg_rating':
        sort_criteria = func.avg(Review.rating).desc()
    elif sort_by == 'latest':
        sort_criteria = Product.id.desc()
    

# Query products
    query = Product.query.filter(Product.brand == brand_name)
    
    if categories:
        query = query.filter(Product.category.in_(categories))
    if price_min is not None:
        query = query.filter(Product.price >= price_min)
    if price_max is not None:
        query = query.filter(Product.price <= price_max)

    query = query.order_by(sort_criteria)


    # Pagination logic
    page = request.args.get('page', 1, type=int)
    products = query.paginate(page=page, per_page=per_page, error_out=False)



    # Calculate the count of products in each category for the given brand
    category_counts = db.session.query(Product.category, func.count(Product.id)).filter_by(brand=brand_name).group_by(Product.category).all()
    category_counts_dict = {category: count for category, count in category_counts}
    
    # Total number of products
    total_products_by_brand = query.count()



    return render_template('brand_store.html', products=products, brand_name=brand_name,
                           category_counts=category_counts_dict, total_products=total_products_by_brand,
                           sort_by=sort_by, price_min=price_min, price_max=price_max,
                           per_page=per_page)




@products.route('/category/<string:category_name>')
def category(category_name):
    brands=request.args.getlist('brand')
    price_max=request.args.get('price_max', type=float)
    price_min=request.args.get('price_min', type=float)
    per_page=request.args.get('per_page', 24, type=int)
    sort_by=request.args.get('sort_by', 'price_asc')
    
    
    sort_criteria=Product.price.asc()
    
    if sort_by=='avg_rating':
        sort_criteria=Product.rating.desc()
    elif sort_by=='price_desc':
        sort_criteria=Product.price.desc()
    elif sort_by=='latest':
        sort_criteria=Product.id.desc()
        
    query=Product.query.filter(Product.category==category_name)
    
    if brands:
        query=query.filter(Product.brand.in_(brands))
    if price_max is not None:
        query=query.filter(Product.price <= price_max)
    if price_min is not None:
        query=query.filter(Product.price >= price_min)
        
    query=query.order_by(sort_criteria)
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    products = query.paginate(page=page, per_page=per_page, error_out=False)
    
    
    # Calculate the count of products for each brand for the given category
    brand_counts = db.session.query(Product.brand, func.count(Product.id)).filter_by(category=category_name).group_by(Product.brand).all()
    brand_counts_dict = {brand: count for brand, count in brand_counts}

    # Total number of products
    total_products_by_category = query.count()
    
    return  render_template('category_store.html', products=products, category_name=category_name,
                            brand_counts=brand_counts_dict, total_products=total_products_by_category,
                            sort_by=sort_by, price_min=price_min, price_max=price_max,
                            per_page=per_page)
    
    
@products.route('/search')
def search():
    query = request.args.get('query', '')
    category = request.args.get('category', '')
    sort_by = request.args.get('sort_by', 'latest')
    per_page = request.args.get('per_page', 24, type=int)
    page = request.args.get('page', 1, type=int)
    brands = request.args.getlist('brand')
    price_min = request.args.get('price_min', '')
    price_max = request.args.get('price_max', '')


    # Base query for products
    products_query = Product.query.filter(Product.name.ilike(f'%{query}%') | Product.description.ilike(f'%{query}%'))

    # Apply category filter
    if category:
        products_query = products_query.filter(Product.category == category)


    # Apply price filters
    if price_min:
        products_query = products_query.filter(Product.price >= float(price_min))
    if price_max:
        products_query = products_query.filter(Product.price <= float(price_max))


    # Apply sorting
    if sort_by == 'price_asc':
        products_query = products_query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        products_query = products_query.order_by(Product.price.desc())
    elif sort_by == 'avg_rating':
        products_query = products_query.order_by(Product.rating.desc())
    elif sort_by == 'latest':
        products_query = products_query.order_by(Product.created_at.desc())
        
    products_for_count=products_query
    
    # Apply brand filters
    if brands:
        products_query = products_query.filter(Product.brand.in_(brands))

    products = products_query.paginate(page=page, per_page=per_page, error_out=False)

    # Aggregate brand counts for the filtered search results
    # brand_counts={}
    # for product in products:
    #     brand_counts[product.brand] +=1
    
    brand_counts = Counter(product.brand for product in products_for_count)
    print(brand_counts)

    return  render_template('search.html',
                            products=products,
                            query=query,
                            brand_counts=brand_counts,
                            sort_by=sort_by,
                            per_page=per_page,
                            total_products=products.total,
                            category=category,
                            price_min=price_min,
                            price_max=price_max)



@products.route('/shop/<int:product_id>/update', methods=['GET','POST'])
@login_required
def product_update(product_id):
    if current_user.role!='admin':
        abort(403)
    form = UpdateProductForm()
    # product=Product.query.filter_by(id=5).first()
    product=Product.query.filter_by(id=product_id).first()
    if form.validate_on_submit():
        product.name=form.name.data
        product.description=form.description.data
        product.price=form.price.data
        product.price_before=form.price_before.data
        product.stock=form.stock.data
        product.category=form.category.data
        product.brand=form.brand.data
        product.color=form.color.data
        product.size=form.size.data
        product.weight=form.weight.data
        product.camera=form.camera.data
        product.screen=form.screen.data
        product.ram=form.ram.data
        product.cpu=form.cpu.data
        product.gpu=form.gpu.data
        product.os=form.os.data
        product.storage=form.storage.data
        product.battery=form.battery.data
        product.note=form.note.data
        product.created_at=datetime.utcnow()
        
        db.session.add(product)
        db.session.commit()
        
        flash('The Product has been Updated Successfully!', 'success')
        return redirect(url_for('products.product', product_id=product.id))
    elif request.method == 'GET':
        form.name.data=product.name
        form.description.data=product.description
        form.price.data=product.price
        form.price_before.data=product.price_before
        form.stock.data=product.stock
        form.category.data=product.category
        form.brand.data=product.brand
        form.color.data=product.color
        form.size.data=product.size
        form.weight.data=product.weight
        form.camera.data=product.camera
        form.screen.data=product.screen
        form.ram.data=product.ram
        form.cpu.data=product.cpu
        form.gpu.data=product.gpu
        form.os.data=product.os
        form.storage.data=product.storage
        form.battery.data=product.battery
        form.note.data=product.note
    return render_template('product_update.html', title='add a product', form=form)

