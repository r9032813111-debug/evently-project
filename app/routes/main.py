from flask import Blueprint, render_template
from app.models import Event
from datetime import datetime

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    # Показываем все события, отсортированные по дате (от новых к старым)
    all_events = Event.query.order_by(Event.date.desc()).all()

    return render_template("index.html", events=all_events)
