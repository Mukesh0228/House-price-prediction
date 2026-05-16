from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from backend.models import User, Property

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
def admin():
    """Admin panel."""
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.home'))

    users_count = User.query.count()
    properties_count = Property.query.count()
    recent_properties = Property.query.order_by(Property.created_at.desc()).limit(5).all()

    return render_template('admin.html',
                         users_count=users_count,
                         properties_count=properties_count,
                         recent_properties=recent_properties)