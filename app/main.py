from flask import Blueprint, render_template
from . import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/admin')
def admin():
    return render_template('admin.html')
