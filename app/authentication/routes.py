from forms import UserLoginForm, UserSignupForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, redirect, request, url_for, flash

from flask_login import login_user, logout_user, login_manager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserSignupForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data
            print(first_name, last_name, email, password)

            user = User(first_name, last_name, email, password=password)

            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account {email}', 'User-created')
            return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid form data: Please check your form.')
    return render_template('sign_up.html', form=form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash("You were successful in your login. Welcome to Tequila Heaven!", 'auth-success')
                return redirect(url_for('site.profile'))
            
            else:
                flash("Opps! Try again!", 'auth-failed')
    except:
        raise Exception('Invalid form data: Please check your form.')
    return render_template('sign_in.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))

