from flask import Blueprint, send_from_directory

static_bp = Blueprint('static', __name__, static_folder='static')

@static_bp.route('/')
def index():
    """Serve the index.html file"""
    return send_from_directory(static_bp.static_folder, 'index.html')