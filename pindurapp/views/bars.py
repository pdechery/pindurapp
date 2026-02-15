from flask import (
  Blueprint,
  abort,
  request
)
from flask.views import MethodView

from pydantic import BaseModel, ValidationError

from pindurapp import db
from pindurapp.models import Bar, Client, Bills

class C(BaseModel):
  client: int
  bill: float 

class B(BaseModel):
  name: str
  clients: list[C]

bar_views = Blueprint('bar_views', __name__, url_prefix='/api')

class BarsAPI(MethodView):
  def get(self, id: int = None):
    if not id:
      bars = db.session.execute(db.select(Bar).order_by(Bar.name)).scalars()
      res = []
      for b in bars:
        bar = {'nome': b.name, 'bills': []}
        for bill in b.bills:
          bar['bills'].append({
            'bill':bill.bill,
            'client':bill.client.name
            })
          res.append(bar)
      return res
    try:
      bar = db.session.execute(db.select(Bar).filter_by(id=id)).scalar_one()
      res = {'nome': bar.name, 'bills': []}
      for bill in bar.bills:
        res['bills'].append({
          'bill':bill.bill,
          'client':bill.client.name
          })
      return res
    except:
      abort(404, description="No Bar was found.") 

  def post(self):
    try:
      B.model_validate_json(request.get_data())
    except ValidationError as e:
      abort(500, e)

    bar = Bar()
    data = request.json
    if not data["name"]:
      abort(404, description="Bar name is required")
    bar.name = data["name"]
    if data["clients"]:
      for cl in data["clients"]:
        client = db.get_or_404(Client, cl["client"], description="Client id didn't found any client on db.")
        bill = Bills(bill=cl["bill"])
        bill.client_id = client.id
        bar.bills.append(bill)
    try:
      db.session.add(bar)
      db.session.commit()
      return "Bar added succesfully"
    except Exception as exp:
      abort(500, exp)
  
  def patch(self, id):
    bar = db.get_or_404(Bar, id)
    data = request.json
    for cl in data["clients"]:
      client = db.get_or_404(Client, cl["client"], description="Client id didn't found any client on db.")
      bill = Bills(bill=cl["bill"])
      bill.client_id = client.id
      bar.bills.append(bill)
    try:
      db.session.add(bar)
      db.session.commit()
      return "Bar updated succesfully"
    except Exception as exp:
      abort(500, exp)

  def delete(self, id):
    try:
      q = db.select(Bar).filter_by(id=id)
      r = db.session.execute(q).scalar_one()
      db.session.delete(r)
      db.session.commit()
      return "The Bar were removed succesfully"
    except Exception as exp:
      abort(500, exp)


bar_views.add_url_rule('/bars', 'bars_all', view_func=BarsAPI.as_view('bars_api'))
bar_views.add_url_rule('/bars/<int:id>', 'bars_single', view_func=BarsAPI.as_view('bars_api'))

