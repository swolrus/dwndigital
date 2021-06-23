from flask import Blueprint, url_for, request, redirect, render_template, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.users.forms import LoginForm, RegisterForm
from app.payments.forms import SetItemForm
from app.payments.models import Item
from app.users.models import User

users_routes = Blueprint('users', __name__, url_prefix='/users')

@users_routes.route("/createitem", methods=['GET', 'POST'])
@login_required
def create_item():
    form = SetItemForm()
    name = form.name.data
    price = form.price.data
    displayname = form.displayname.data
    description = form.description.data

    if form.validate_on_submit():
        Item(name=name, price=price, displayname=displayname, description=description).save()
        return render_template("newitem.html", item=item)

    return render_template('form.html', title='Create Item', form=form)

@users_routes.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm(next=request.args.get('next'))
    email = form.email.data
    password = form.password.data
    
    if form.validate_on_submit():
        user = User.objects(email=email).first()

        if user and user.check_password(password):

            if login_user(user, remember=True):
                user.update_activity()

                #handle optionally redirecting to the next URL safely
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('users.profile')
                return redirect(next_page)

            else:
                flash('This account is not active','error')

        else: 
            flash('Login or password is incorrect','error')

    return render_template('form.html', title='Sign In', form=form)

@users_routes.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegisterForm()
    email = form.email.data
    password = form.password.data
    repeatpassword = form.repeatpassword.data
    
    if form.validate_on_submit():
        user = User.objects(email=email).first()
        if not user:
            user = User(email=email).set_password(password).save()

        return redirect(url_for('users.login'))

    else:
        return render_template('form.html', form=form)

@users_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users_routes.route("/profile")
def profile():
    return "<p>" + current_user.email + "</p>"