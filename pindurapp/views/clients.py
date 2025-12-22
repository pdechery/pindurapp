from sqlalchemy.sql.expression import func

from flask import (
  Blueprint,
  abort,
  request
)
from flask.json import jsonify
from flask.views import MethodView

from pydantic import BaseModel, ValidationError

from pindurapp import db
from pindurapp.models import Client, Bar, Bills

class B(BaseModel):
  bar: int
  bill: float 

class C(BaseModel):
  name: str
  bills: list[B]

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
    try:
      C.model_validate_json(request.get_data())
    except ValidationError as e:
      abort(500, e)
    
    client = Client()
    data = request.json
    if not data["name"]:
      abort(404, description="Client name is required")
    client.name = data["name"]
    if data["bills"]:
      for bill in data["bills"]:
        bar = db.get_or_404(Bar, bill["bar"], description="Bar id didn't found any bar on db.")
        bill = Bills(bill=bill["bill"])
        bill.bar_id = bar.id
        client.bills.append(bill)
    try:
      db.session.add(client)
      db.session.commit()
      return "Client added succesfully"
    except Exception as exp:
      abort(500, exp)
  
  def patch(self, id):
    client = db.get_or_404(Client, id)
    data = request.json
    for bill in data["bills"]:
        bar = db.get_or_404(Bar, bill["bar"], description="Bar id didn't found any bar on db.")
        bill = Bills(bill=bill["bill"])
        bill.bar_id = bar.id
        client.bars.append(bill)
    try:
      db.session.add(client)
      db.session.commit()
      return "The Bills were added succesfully"
    except Exception as exp:
      abort(500, exp)

  def delete(self, id):
    try:
      q = db.select(Client).filter_by(id=id)
      r = db.session.execute(q).scalar_one()
      db.session.delete(r)
      db.session.commit()
      return "The Client were removed succesfully"
    except Exception as exp:
      pass


client_views.add_url_rule('/clients', 'clients_endpoint_root', view_func=ClientAPI.as_view('client_api'))
client_views.add_url_rule('/clients/<int:id>', 'clients_endpoint', view_func=ClientAPI.as_view('client_api'))
client_views.add_url_rule("/clients/sum", "clients_endpoint_sum", view_func=clients_sum)

