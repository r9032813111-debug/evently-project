from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Event, Registration
from werkzeug.security import generate_password_hash

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile")
@login_required
def profile():
    user_events = (
        Event.query.filter_by(user_id=current_user.id).order_by(Event.date.desc()).all()
    )
    registrations = Registration.query.filter_by(user_id=current_user.id).all()

    return render_template(
        "profile.html", user_events=user_events, registrations=registrations
    )


@profile_bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if username:
            current_user.username = username
        if email:
            current_user.email = email
        if password:
            current_user.password = generate_password_hash(password)

        db.session.commit()
        flash("Профиль успешно обновлён!", "success")
        return redirect(url_for("profile.profile"))

    return render_template("edit_profile.html")
