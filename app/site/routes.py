from flask import Blueprint, render_template, redirect, url_for, flash
from models import User, db, Estimate
from flask_login import current_user

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
@site.route('/home')
def home():
    return render_template('index.html')

@site.route('/profile')
def profile():
    return render_template('profile.html')
