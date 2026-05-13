from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.models import Event, Registration
from app.forms import EventForm, EventRegistrationForm
from app import db
from werkzeug.utils import secure_filename
import os

events_bp = Blueprint("events", __name__)


# Создание события
@events_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = EventForm()
    if form.validate_on_submit():
        image_filename = None
        if form.image.data and form.image.data.filename:
            image = form.image.data
            image_filename = secure_filename(image.filename)
            upload_path = os.path.join("app/static/uploads", image_filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            image.save(upload_path)

        event = Event(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            location=form.location.data,
            category=form.category.data,
            image=image_filename,
            user_id=current_user.id,
        )
        db.session.add(event)
        db.session.commit()
        flash("Событие успешно создано!", "success")
        return redirect(url_for("main.index"))

    return render_template("create_event.html", form=form)


# Страница события
@events_bp.route("/<int:event_id>")
def detail(event_id):
    event = Event.query.get_or_404(event_id)
    reg_form = EventRegistrationForm()
    registrations = Registration.query.filter_by(event_id=event_id).all()

    return render_template(
        "event_detail.html", event=event, reg_form=reg_form, registrations=registrations
    )


# Регистрация на событие
@events_bp.route("/<int:event_id>/register", methods=["POST"])
@login_required
def register(event_id):
    form = EventRegistrationForm()
    if form.validate_on_submit():
        registration = Registration(
            event_id=event_id,
            user_id=current_user.id,
            full_name=form.full_name.data,
            age=form.age.data,
        )
        db.session.add(registration)
        db.session.commit()
        flash("Вы успешно зарегистрировались на событие!", "success")
    else:
        flash("Пожалуйста, заполните все поля", "danger")
    return redirect(url_for("events.detail", event_id=event_id))


# Удаление события
@events_bp.route("/<int:event_id>/delete")
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        abort(403)

    db.session.delete(event)
    db.session.commit()
    flash("Событие успешно удалено", "success")
    return redirect(url_for("main.index"))  # ← теперь точно на главную
