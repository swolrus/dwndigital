from flask import current_app as app
from flask import Blueprint, url_for, request, redirect, render_template, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os
from app.common.util import allowed_file, toJSON
from app.admin.forms import LoginForm, RegisterForm
from app.payments.forms import SetItemForm, DeleteItemForm
from app.admin.models import User
from app.payments.models import Item
from app.payments import errors

admin_routes = Blueprint('admin', __name__, url_prefix='/admin')

@admin_routes.route("/createitem", methods=['GET', 'POST'])
@login_required
def create_item():
    form = SetItemForm()
    ref = form.ref.data
    name = form.name.data
    active = form.active.data
    price = form.price.data
    description = form.description.data

    if form.validate_on_submit():
        file = request.files['img']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash('Please use a valid image format')
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            relpath = os.path.join(app.config['UPLOAD_STATIC_FOLDER'], filename)
            abspath = os.path.join(app.root_path, 'static', relpath)

            file.save(abspath)
            
            item = Item(ref=ref, name=name, active=active, description=description, price=price, img=relpath).save()
            return render_template('admin/newitem.html', item=item)

    return render_template('form.html', title='Create Item', form=form)

@admin_routes.route("/delitem", methods=['GET', 'POST'])
@login_required
def delete_item():
    form = DeleteItemForm()
    form.name.choices = [(item.pk, item.name) for item in Item.objects().all()]
    pk = form.name.data

    if form.validate_on_submit():
        if form.delete.data == True:
            item = Item.objects().get(pk=pk)
            form.name.choices.remove((item.pk, item.name))
            flash("Deleted item: " + item.name)
            item.delete()
        elif form.activate.data == True:
            item = Item.objects().get(pk=pk)
            form.name.choices.remove((item.pk, item.name))
            flash("Ativated item: " + item.name)
            item.active = True
            item.save()
        elif form.deactivate.data == True:
            item = Item.objects().get(pk=pk)
            form.name.choices.remove((item.pk, item.name))
            flash("Deactivated item: " + item.name)
            item.active = False
            item.save()

    
    if len(form.name.choices) == 0:
        form.name.choices=['No Items Exist!']

    return render_template('form.html', title='Delete Item', form=form)

@admin_routes.route("/", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.home'))

    form = LoginForm(next=request.args.get('next'))
    email = form.email.data
    remember_me = form.remember_me.data
    password = form.password.data
    
    if form.validate_on_submit():
        user = User.objects(email=email).first() or False

        if user and user.check_password(password):

            if login_user(user, remember=remember_me):
                user.update_activity()

                #handle optionally redirecting to the next URL safely
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('admin.home')
                return redirect(next_page)

            else:
                flash('This account is not active','error')

        else: 
            flash('Login or password is incorrect','error')

    return render_template('form.html', title='Sign In', form=form)

@admin_routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    email = form.email.data
    password = form.password.data
    repeatpassword = form.repeatpassword.data
    
    if form.validate_on_submit():
        user = User.objects(email=email).first() or False
        if not user:
            user = User(email=email).set_password(password)
            user.save()

        return redirect(url_for('admin.login'))

    else:
        return render_template('form.html', form=form)

@admin_routes.route('/logout')
@login_required
def logout():
    flash('successfully logged out ' + current_user.email)
    logout_user()
    return redirect(url_for('admin.login'))

@admin_routes.route("/home")
def home():
    return render_template('admin/home.html')