import os
import logging
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET") or "barter-hub-secret-key-for-development-2024"
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

# Initialize the app with the extension
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # type: ignore
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

@app.context_processor
def inject_language():
    def get_user_language():
        accept_language = request.headers.get('Accept-Language', '')
        # Check if request is from outside Indonesia or explicitly requests English
        if 'en' in accept_language.lower() and 'id' not in accept_language.lower():
            # Additional check for common non-Indonesian locales
            non_id_locales = ['en-us', 'en-gb', 'en-au', 'en-ca', 'zh-cn', 'ja-jp', 'ko-kr', 'es-es', 'fr-fr', 'de-de']
            for locale in non_id_locales:
                if locale in accept_language.lower():
                    return 'en'
        return 'id'
    
    return dict(user_language=get_user_language)

# Create upload directory if it doesn't exist
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

with app.app_context():
    # Import models to ensure tables are created
    import models  # noqa: F401
    db.create_all()
    
    # Initialize default categories
    from models import Category
    if Category.query.count() == 0:
        default_categories = [
            'Elektronik', 'Pakaian & Aksesoris', 'Rumah & Taman', 
            'Olahraga & Outdoor', 'Buku & Media', 'Mainan & Permainan',
            'Otomotif', 'Kesehatan & Kecantikan', 'Koleksi', 'Lainnya'
        ]
        
        for cat_name in default_categories:
            category = Category(name=cat_name)  # type: ignore
            db.session.add(category)
        
        db.session.commit()
        logging.info("Default categories created")
    
    logging.info("Database tables created")
