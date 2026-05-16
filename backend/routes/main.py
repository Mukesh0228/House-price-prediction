from flask import Blueprint, render_template
from flask_login import login_required, current_user
from backend.models import Property

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Home page with property listings and prediction form."""
    properties = Property.query.order_by(Property.created_at.desc()).limit(6).all()
    return render_template('index.html', properties=properties)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard."""
    user_properties = Property.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', properties=user_properties)