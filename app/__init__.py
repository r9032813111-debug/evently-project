from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    from app.models import User

    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "supersecretkey12345"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///evently.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = "app/static/uploads"

    db.init_app(app)
    login_manager.init_app(app)

    # Импорт blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.events import events_bp
    from app.routes.profile import profile_bp  # ← добавлено

    # Регистрация blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(events_bp, url_prefix="/events")
    app.register_blueprint(profile_bp)  # ← добавлено

    # Создание папки для загрузок
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    with app.app_context():
        db.create_all()

    return app
