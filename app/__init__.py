from flask import Flask, g, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Flask extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()

def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Default Configuration
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(app.instance_path, 'portfolio.db')),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        MAIL_SERVER=os.getenv('MAIL_SERVER', 'smtp.gmail.com'),
        MAIL_PORT=int(os.getenv('MAIL_PORT', 587)),
        MAIL_USE_TLS=True,
        MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
    )

    # Override config if provided
    if config:
        app.config.update(config)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    mail.init_app(app)
    migrate.init_app(app, db)
    
    # User loader callback
    @login_manager.user_loader
    def load_user(id):
        try:
            from .models import User
            return User.query.get(int(id))
        except Exception as e:
            print(f"Error loading user: {e}")
            return None
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # Register context processor
    @app.context_processor
    def inject_globals():
        try:
            from .models import About
            about = About.query.first()
        except Exception:
            about = None
        return {
            'year': datetime.now().year,
            'g': {'about': about}
        }
    
    with app.app_context():
        # Import routes
        try:
            from .routes.main import bp as main_bp
            from .routes.auth import bp as auth_bp
            from .routes.admin import bp as admin_bp
            
            # Register blueprints
            app.register_blueprint(main_bp)
            app.register_blueprint(auth_bp)
            app.register_blueprint(admin_bp)
            
            # Create database tables
            db.create_all()
            
        except Exception as e:
            print(f"Error during app initialization: {e}")
            raise
    
    return app 