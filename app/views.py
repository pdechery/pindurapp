import datetime
from sqlalchemy.sql.expression import func

from flask import (
  Blueprint,
  session, 
  abort
)
from flask.json import jsonify


from app import db
from app.models import Client, Bar, Bills
from app.helpers.jwt import generate_jwt, verify_jwt, token

views = Blueprint('views', __name__, url_prefix='/api')

@views.errorhandler(404)
def page_not_found(error):
  return "Not Found", 404


@views.route('/get-token')
def get_token():
  token = generate_jwt({
    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
    'iat': datetime.datetime.utcnow(),
    'sub': 'eu',
  })
  return token

    
@views.route("/clients/")
@views.route("/")
def clients_list():
  clients = db.session.scalars(db.select(Client).order_by(Client.name))
  res = []
  for c in clients:
    clt = {'nome':c.name, 'bars': []}
    for b in c.bars:      
      clt['bars'].append({
        'id': b.bars.id,
        'nome': b.bill,
        'bill': b.bars.name
      })
    res.append(clt)
  response = jsonify(res)
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response


@views.route("/clients/sum")
def clients_sum():
  q = db.select(Client.name, func.sum(Bills.bill)).join(Client.bars).join(Bills.bars).group_by(Client.name)
  sums = db.session.execute(q)
  res = []
  for s in sums:
    res.append({'name':s[0], 'bill':s[1]})
  response = jsonify(res)
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response


@views.route("/client/<int:client_id>") 
@token
def client_by_id(client_id):
  try:
    client = db.session.execute(db.select(Client).filter_by(id=client_id)).scalar_one()
  except:
    abort(404)
    res = {'nome': client.name, 'bars': []}
    for bar in client.bars:
      res['bars'].append({
        'name':bar.bars.name,
        'bill':bar.bill
        })
      return res


@views.route("/bars")
@token
def bars_list():
  bars = db.session.execute(db.select(Bar).order_by(Bar.name)).scalars()
  res = []
  for b in bars:
    bar = {'nome': b.name, 'clients': []}
    for c in b.clients:
      bar['clients'].append({
        'name':c.clients.name,
        'bill':c.bill
        })
      res.append(bar)
      return res


@views.route("/bar/<int:bar_id>")
@token
def bar_by_id(bar_id):
  try:
    bar = db.session.execute(db.select(Bar).filter_by(id=bar_id)).scalar_one()
  except:
    abort(404)
    res = {'nome': bar.name, 'clients': []}
    for c in bar.clients:
      res['clients'].append({
        'name':c.clients.name,
        'bill':c.bill
        })
      return res

