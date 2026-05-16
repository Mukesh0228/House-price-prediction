from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from backend.models import db, Property
from backend.forms import PropertyForm
from ml_model.utils import get_location_names

properties_bp = Blueprint('properties', __name__)

@properties_bp.route('/properties')
def properties():
    """Browse all properties."""
    page = request.args.get('page', 1, type=int)
    location = request.args.get('location')
    property_type = request.args.get('type')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)

    query = Property.query

    if location:
        query = query.filter(Property.location.ilike(f'%{location}%'))
    if property_type:
        query = query.filter_by(property_type=property_type)
    if min_price:
        query = query.filter(Property.price >= min_price)
    if max_price:
        query = query.filter(Property.price <= max_price)

    properties_list = query.paginate(page=page, per_page=12)
    return render_template('properties.html', properties=properties_list)

@properties_bp.route('/property/<int:id>')
def property_detail(id):
    """View detailed property information."""
    property = Property.query.get_or_404(id)
    return render_template('property_detail.html', property=property)

@properties_bp.route('/add_property', methods=['GET', 'POST'])
@login_required
def add_property():
    """Add new property listing."""
    form = PropertyForm()
    form.location.choices = [(loc, loc) for loc in get_location_names()]

    if form.validate_on_submit():
        property_obj = Property(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            location=form.location.data,
            area_sqft=form.area_sqft.data,
            bhk=form.bhk.data,
            bathrooms=form.bathrooms.data,
            property_type=form.property_type.data,
            user_id=current_user.id
        )

        # Handle file upload
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                from flask import current_app
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                property_obj.image_filename = filename

        db.session.add(property_obj)
        db.session.commit()
        flash('Property added successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('add_property.html', form=form)