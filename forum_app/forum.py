from flask import Blueprint
from flask.json import jsonify

bp = Blueprint(name='forum', import_name=__name__)


@bp.route('/')
def index():
    return jsonify({'message': 'Hello World'})
