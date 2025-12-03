from sqlalchemy.sql.expression import func

from flask import (
  Blueprint,
  abort
)
from flask.json import jsonify
from flask.views import MethodView


from pindurapp import db
from pindurapp.models import Client, Bills

client_views = Blueprint('client_views', __name__, url_prefix='/api')

def clients_sum():
  q = db.select(Client.name, func.sum(Bills.bill)).join(Client.bars).join(Bills.bars).group_by(Client.name)
  sums = db.session.execute(q)
  res = []
  for s in sums:
    res.append({'name':s[0], 'bill':s[1]})
  response = jsonify(res)
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response

class ClientAPI(MethodView):
  def __init__(self):
    pass
  
  def get(self, id: int = None):
    if not id:
      clients = db.session.execute(db.select(Client.name))
      res = []
      for c in clients:
        res.append({'name':c[0]})
      response = jsonify(res)
      response.headers.add("Access-Control-Allow-Origin", "*")
      return response
    try:
      client = db.session.execute(db.select(Client).filter_by(id=id)).scalar_one()
      res = {'nome': client.name, 'bars': []}
      for bar in client.bars:
        res['bars'].append({
          'name':bar.bars.name,
          'bill':bar.bill
          })
        return res
    except:
      abort(404)

  def post(self):
    return "This is Client POST function"


client_views.add_url_rule('/clients', 'clients_endpoint_root', view_func=ClientAPI.as_view('client_api'))
client_views.add_url_rule('/clients/<int:id>', 'clients_endpoint', view_func=ClientAPI.as_view('client_api'))
client_views.add_url_rule("/clients/sum", "clients_endpoint_sum", view_func=clients_sum)

