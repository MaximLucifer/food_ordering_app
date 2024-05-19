import os
import secrets
from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, MenuItem, Order, OrderItem
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, MenuItemForm, OrderForm

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
admin = Blueprint('admin', __name__)

def save_picture_acc(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/acc_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

def delete_picture_acc(picture_filename):
    picture_path = os.path.join(current_app.root_path, 'static/acc_pics', picture_filename)
    if os.path.exists(picture_path):
        os.remove(picture_path)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/menu_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

def delete_picture(picture_filename):
    picture_path = os.path.join(current_app.root_path, 'static/menu_pics', picture_filename)
    if os.path.exists(picture_path):
        os.remove(picture_path)

@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')

@main.route("/menu")
def menu():
    items = MenuItem.query.all()
    return render_template('menu.html', items=items)

@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.picture.data:  # Проверка, был ли загружен файл
            picture_file = save_picture_acc(form.picture.data)  # Функция для сохранения файла на сервере
            current_user.image_file = picture_file  # Обновление поля с путем к файлу аватарки в базе данных
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

@admin.route("/manage_menu", methods=['GET', 'POST'])
@login_required
def manage_menu():
    form = MenuItemForm()
    if form.validate_on_submit():
        print("Form validated")  # Debugging information
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            menu_item = MenuItem(
                name=form.name.data, 
                price=form.price.data, 
                description=form.description.data, 
                image_file=picture_file
            )
            print(f"Picture file saved: {picture_file}")  # Debugging information
        else:
            menu_item = MenuItem(
                name=form.name.data, 
                price=form.price.data, 
                description=form.description.data
            )
            print("No picture file provided")  # Debugging information

        db.session.add(menu_item)
        db.session.commit()
        print("Menu item added to the database")  # Debugging information
        flash('Menu item has been added/updated!', 'success')
        return redirect(url_for('admin.manage_menu'))
    else:
        print("Form not validated")  # Debugging information

    items = MenuItem.query.all()
    return render_template('manage_menu.html', title='Manage Menu', form=form, items=items)

@admin.route("/menu_item/<int:item_id>/delete", methods=['POST'])
@login_required
def delete_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    if item.image_file != 'default.jpg':
        delete_picture(item.image_file)
    db.session.delete(item)
    db.session.commit()
    flash('Menu item has been deleted!', 'success')
    return redirect(url_for('admin.manage_menu'))

@main.route("/order/<int:item_id>", methods=['GET', 'POST'])
@login_required
def order(item_id):
    item = MenuItem.query.get_or_404(item_id)
    form = OrderForm()
    if form.validate_on_submit():
        order_item = OrderItem(quantity=form.quantity.data, menu_item_id=item.id)
        order = Order(customer=current_user, total=item.price * form.quantity.data, items=[order_item])
        db.session.add(order)
        db.session.commit()
        flash('Your order has been placed!', 'success')
        return redirect(url_for('main.home'))
    return render_template('order.html', title='Order', item=item, form=form)

@admin.route("/manage_orders")
@login_required
def manage_orders():
    orders = Order.query.all()
    return render_template('manage_orders.html', title='Manage Orders', orders=orders)