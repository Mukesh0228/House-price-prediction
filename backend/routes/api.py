from flask import Blueprint, jsonify, request
from ml_model.utils import get_location_names, get_estimated_price
from backend.models import db, PropertyRequest, Property
from flask_login import current_user

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/get_location_names', methods=['GET'])
def api_get_location_names():
    """API endpoint for location names."""
    try:
        locations = get_location_names()
        return jsonify({'locations': locations})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/predict_home_price', methods=['POST'])
def api_predict_home_price():
    """API endpoint for price prediction."""
    try:
        data = request.get_json()
        location = data['location']
        sqft = float(data['sqft'])
        bhk = int(data['bhk'])
        bath = int(data['bath'])

        estimated_price = get_estimated_price(location, sqft, bhk, bath)
        return jsonify({'estimated_price': estimated_price})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/request_property', methods=['POST'])
def api_request_property():
    """API endpoint for property purchase requests."""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'property_id']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400

        # Check if property exists
        property = Property.query.get(data['property_id'])
        if not property:
            return jsonify({'error': 'Property not found'}), 404

        # Create property request
        property_request = PropertyRequest(
            property_id=data['property_id'],
            user_id=current_user.id if current_user.is_authenticated else None,
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            budget=float(data.get('budget', 0)) if data.get('budget') else None,
            visit_date=data.get('visit_date'),
            message=data.get('message', '')
        )

        db.session.add(property_request)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Property request submitted successfully',
            'request_id': property_request.id
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500