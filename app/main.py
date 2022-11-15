from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import Lauggage
from . import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/admin')
def admin():
    luggages = Lauggage.query.all()
    return render_template('admin.html', luggages=luggages)


# @main.route('/admin')
# def view_luggages():
#     luggages = Lauggage.query.all()
#     return render_template('admin.html', luggages=luggages)


@main.route('/luggage')
def luggage():
    return render_template('luggage.html')


@main.route('/luggage', methods=['POST'])
def add_luggage():
    name = request.form.get('name')
    email = request.form.get('email')
    description = request.form.get('description')

    new_luggage = Lauggage(email=email, name=name, description=description)

    db.session.add(new_luggage)
    db.session.commit()

    return redirect(url_for('main.admin'))
