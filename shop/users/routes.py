from shop import bcrypt, db
from flask import render_template, redirect, flash, url_for, request, Blueprint
from shop.users.forms import RegisterationForm, LoginForm, UpdateInformationForm
from shop.models import User
from flask_login import login_user, current_user, logout_user, login_required




users=Blueprint('users', __name__)

@users.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password, phone=form.phone.data, address=form.address.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title = 'register', form=form)

@users.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title = 'login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


@users.route("/account/information", methods=['GET', 'POST'])
@login_required
def account_information():
    form = UpdateInformationForm()
    if form.validate_on_submit():
        current_user.username=form.username.data
        current_user.email=form.email.data
        current_user.address=form.address.data
        current_user.phone=form.phone.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    
    elif request.method == 'GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
        form.address.data=current_user.address
        form.phone.data=current_user.phone
    return render_template('account_information.html', title='Update Account Information', form=form)