from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.api.validators import StartFlowSchema, ValidatePhoneNumberSchema, CompleteFlowSchema
from app.utils.exceptions import ProveAPIError, AuthenticationError
from app.services.prove_service import prove_service

api_bp = Blueprint('api', __name__)

@api_bp.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify({'error': 'Validation failed', 'messages': e.messages}), 400

@api_bp.errorhandler(ProveAPIError)
def handle_prove_error(e):
    return jsonify({'error': 'Prove API error', 'message': str(e)}), 500


@api_bp.errorhandler(AuthenticationError)
def handle_auth_error(e):
    return jsonify({'error': 'Authentication error', 'message': str(e)}), 401

@api_bp.route('/start', methods=['POST'])
def start_flow():
    """Start the Prove Flow"""
    schema = StartFlowSchema()

    try:
        data = schema.load(request.json)
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'messages': e.messages}), 400

    result = prove_service.start_flow(
        phone_number=data['phone_number'],
        flow_type=data['flow_type'],
        ssn=data['ssn']
    )

    return jsonify({
        'auth_token': result.get('authToken'),
        'correlation_id': result.get('correlationId'),
    })

@api_bp.route('/validate', methods=['POST'])
def validate_phone_number():
    """Validate the phone number"""
    schema = ValidatePhoneNumberSchema()

    try:
        data = schema.load(request.json)
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'messages': e.messages}), 400

    result = prove_service.validate_phone_number(
        correlation_id=data['correlation_id']
    )

    return jsonify({
        'result': result
    })

@api_bp.route('/complete', methods=['POST'])
def complete_flow():
    """Complete the Prove Flow"""
    schema = CompleteFlowSchema()

    try:
        data = schema.load(request.json)
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'messages': e.messages}), 400

    result = prove_service.complete_flow(
        correlation_id=data['correlation_id'],
        user_data=data.get('individual', {})
    )

    return jsonify({
        'result': result
    })