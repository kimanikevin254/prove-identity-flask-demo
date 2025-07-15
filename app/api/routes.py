from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.api.validators import StartFlowSchema, ValidatePhoneNumberSchema, CompleteFlowSchema
from app.utils.exceptions import ProveAPIError, AuthenticationError

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
