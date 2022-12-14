from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import Lauggage
from . import db
import africastalking
import os
import smtplib


main = Blueprint('main', __name__)

username = os.getenv('user_name', 'sandbox')
api_key = os.getenv('api_key', 'key')
phone = os.getenv('phone', 'phone')

africastalking.initialize(username, api_key)
sms = africastalking.SMS


@main.route('/')
@login_required
def index():
    luggages = Lauggage.query.all()
    return render_template('index.html', luggages=luggages)


@main.route('/luggage')
@login_required
def luggage():
    return render_template('luggage.html')


@main.route('/luggage', methods=['POST'])
@login_required
def add_luggage():
    name = request.form.get('name')
    email = request.form.get('email')
    description = request.form.get('description')

    new_luggage = Lauggage(email=email, name=name, description=description)

    db.session.add(new_luggage)
    db.session.commit()

    message = f"Dear {new_luggage.name} your luggage ID: 00{new_luggage.id} has been logged into our storage"
    server = smtplib.SMTP("smtp.google.com", 465)
    server.starttls()
    server.login(os.getenv("email"), os.getenv("password"))
    server.sendmail(os.getenv("email"), luggage.email, message)

    sms.send(f"Dear {new_luggage.name} your luggage ID: 00{new_luggage.id} has been logged into our storage", [f"{phone}"], callback=on_finish)
    return redirect(url_for('main.index'))


def on_finish(error, response):
    if error is not None:
        raise error
    print(response)


@main.route('/luggage/<id>')
@login_required
def view_luggage(id):
    luggage = Lauggage.query.filter_by(id=id).first_or_404()
    data = f"Luggage ID: {luggage.id} Owner: {luggage.name} Contact: {luggage.email}"
    return render_template('show_luggage.html', luggage=luggage, data=data)


@main.route('/logout/<id>')
@login_required
def logout(id):
    luggage = Lauggage.query.filter_by(id=id).first_or_404()

    message = f"Dear {luggage.name} your luggage ID: 00{luggage.id} has been logged out of our storage"
    server = smtplib.SMTP("smtp.google.com", 465)
    server.starttls()
    server.login(os.getenv("email"), os.getenv("password"))
    server.sendmail(os.getenv("email"), luggage.email, message)

    sms.send(f"Dear {luggage.name} your luggage ID: 00{luggage.id} has been logged out of our storage", [f"{phone}"], callback=on_finish)

    db.session.delete(luggage)
    db.session.commit()
    flash("Luggage logged out")

    return redirect(url_for('main.index'))
