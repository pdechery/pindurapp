import datetime
from sqlalchemy.sql.expression import func

from flask import (
  Blueprint,
  abort
)
from flask.json import jsonify


from pindurapp import db
from pindurapp.models import Client, Bar, Bills
from pindurapp.helpers.jwt import generate_jwt, verify_jwt, token

jwt_views = Blueprint('views', __name__, url_prefix='/api')

@jwt_views.route('/get-token')
def get_token():
  token = generate_jwt({
    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
    'iat': datetime.datetime.utcnow(),
    'sub': 'eu',
  })
  return token