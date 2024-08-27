import os
from flask import Flask
from app.extensions import db, migrate
from app import models
import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    print("Database URL:", app.config['SQLALCHEMY_DATABASE_URI'])
    print("Secret Key:", app.config['SECRET_KEY'])
    print("Upload Folder:", app.config['UPLOAD_FOLDER'])

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app