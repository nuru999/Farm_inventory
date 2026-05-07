from flask import Blueprint

inventory_bp = Blueprint('inventory', __name__, url_prefix='/api')
pages_bp = Blueprint('pages', __name__)
