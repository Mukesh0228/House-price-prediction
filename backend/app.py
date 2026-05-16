from flask import Flask, render_template, send_from_directory
from flask_login import LoginManager
import os
import sys

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import ML utilities
from ml_model.utils import load_saved_artifacts

# Import local modules
from backend.config import Config
from backend.models import db
from backend.routes.main import main_bp
from backend.routes.auth import auth_bp
from backend.routes.properties import properties_bp
from backend.routes.analytics import analytics_bp
from backend.routes.api import api_bp
from backend.routes.admin import admin_bp

def create_app():
    app = Flask(__name__,
                template_folder='../frontend',
                static_folder='../frontend/static')

    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(properties_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Login manager user loader
    @login_manager.user_loader
    def load_user(user_id):
        from backend.models import User
        return User.query.get(int(user_id))

    # Favicon route
    @app.route('/favicon.ico')
    def favicon():
        """Return a simple favicon or 204 No Content."""
        return '', 204

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500

    return app

# Initialize Database
def create_tables(app):
    """Create database tables."""
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    app = create_app()

    # Load ML artifacts
    try:
        load_saved_artifacts()
        print("ML artifacts loaded successfully.")
    except Exception as e:
        print(f"Warning: Could not load ML artifacts: {e}")

    # Create tables
    create_tables(app)

    # Run app
    app.run(debug=True, host='0.0.0.0', port=5000)