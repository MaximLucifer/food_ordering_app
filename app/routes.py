import os
import secrets
from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, MenuItem, Order, OrderItem
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, MenuItemForm, OrderForm
from app.decorators import role_required

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
    menu_items = MenuItem.query.all()
    return render_template('home.html', menu_items=menu_items)

@main.route('/about')
def about():
    return render_template('about.html')

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
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            menu_item = MenuItem(name=form.name.data, price=form.price.data, description=form.description.data, image_file=picture_file)
        else:
            menu_item = MenuItem(name=form.name.data, price=form.price.data, description=form.description.data)
        db.session.add(menu_item)
        db.session.commit()
        flash('Menu item has been added/updated!', 'success')
        return redirect(url_for('admin.manage_menu'))
    items = MenuItem.query.all()
    return render_template('manage_menu.html', title='Manage Menu', form=form, items=items)

@admin.route('/admin', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def administrator():
    menu_items = MenuItem.query.all()
    orders = Order.query.all()
    users = User.query.all()
    form = MenuItemForm()
    return render_template('admin.html', title='Admin Panel', menu_items=menu_items, orders=orders, users=users, form=form)


@admin.route("/admin/add_menu_item", methods=['GET', 'POST'])
@login_required
@role_required('admin')
def admin_add_menu_item():
    form = MenuItemForm()
    if form.validate_on_submit():
        picture_file = save_picture(form.picture.data)
        menu_item = MenuItem(name=form.name.data, price=form.price.data, description=form.description.data, image_file=picture_file)
        db.session.add(menu_item)
        db.session.commit()
        flash('Menu item has been added!', 'success')
        return redirect(url_for('admin.administrator'))
    flash('Form not validated', 'danger')
    return redirect(url_for('admin.administrator'))

@admin.route("/admin/<int:item_id>/delete", methods=['POST'])
@login_required
@role_required('admin')
def admin_delete_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Menu item has been deleted!', 'success')
    return redirect(url_for('admin.administrator'))

@admin.route('/admin/update_order_status/<int:order_id>', methods=['POST'])
@login_required
@role_required('admin')
def admin_update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    order.status = new_status
    db.session.commit()
    flash('Order status has been updated!', 'success')
    return redirect(url_for('admin.administrator'))

@admin.route("/manage_orders")
@login_required
@role_required('admin')
def manage_orders():
    orders = Order.query.all()
    return render_template('manage_orders.html', title='Manage Orders', orders=orders)

@admin.route('/admin/update_user_role/<int:user_id>', methods=['POST'])
@login_required
@role_required('admin')
def admin_update_user_role(user_id):
    user = User.query.get_or_404(user_id)
    new_role = request.form.get('role')
    user.role = new_role
    db.session.commit()
    flash('User role has been updated!', 'success')
    return redirect(url_for('admin.administrator'))

@main.route("/order/<int:item_id>", methods=['GET', 'POST'])
@login_required
def order(item_id):
    item = MenuItem.query.get_or_404(item_id)
    form = OrderForm()
    if form.validate_on_submit():
        order_item = OrderItem(quantity=form.quantity.data, menu_item_id=item.id, order_id=current_user.id)
        order = Order(total=item.price * form.quantity.data, user_id=current_user.id, items=[order_item])
        db.session.add(order_item)
        db.session.add(order)
        db.session.commit()
        flash('Your order has been placed!', 'success')
        return redirect(url_for('main.home'))
    return render_template('order.html', title='Order', item=item, form=form)

