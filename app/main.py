from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import Lauggage
from . import db

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    luggages = Lauggage.query.all()
    return render_template('index.html', luggages=luggages)


@main.route('/new-luggage')
@login_required
def luggage():
    return render_template('luggage.html')


@main.route('/new-luggage', methods=['POST'])
@login_required
def add_luggage():
    name = request.form.get('name')
    email = request.form.get('email')
    description = request.form.get('description')

    new_luggage = Lauggage(email=email, name=name, description=description)

    db.session.add(new_luggage)
    db.session.commit()

    return redirect(url_for('main.index'))


@main.route('/luggage/<id>')
@login_required
def view_luggage(id):
    return render_template('show_luggage.html', id=id)
