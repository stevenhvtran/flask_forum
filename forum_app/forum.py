from flask import Blueprint
from flask.json import jsonify
from forum_app.models.auth import auth

bp = Blueprint(name='forum', import_name=__name__)


@bp.route('/')
@auth.login_required
def index():
    return jsonify({'message': f'Hello {auth.username()}'})
