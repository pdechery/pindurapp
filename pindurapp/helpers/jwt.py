from functools import wraps
from flask import request, current_app
from jose.exceptions import JWTError
from jose import jwt

def generate_jwt(payload):
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm=current_app.config['ALGORITHM'])
    return token


def verify_jwt(token):
    try:
      header, payload, signature = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=[current_app.config['ALGORITHM']])
      return payload
    except JWTError as e:
      return None


def token(func):
  @wraps(func)
  def wrapper(*args):
    authorization = request.headers.get('Authorization')
    if not authorization:
      return "Header not present", 422
    token = authorization.split(' ')[1]
    if not token:
      return "Token is missing", 422
    payload = verify_jwt(token)
    if not payload:
      return "Token is invalid", 422
    res = func(*args)
    return res
  return wrapper