import os

from sqlalchemy.sql.expression import func

from flask import (
  Blueprint,
  abort,
  request,
  redirect,
  url_for,
  send_from_directory
)
from flask.json import jsonify
from flask.views import MethodView
from werkzeug.utils import secure_filename

from pydantic import BaseModel, ValidationError

from pindurapp import db, app
from pindurapp.models import Client, Bar, Bills

from datetime import datetime

class BarModel(BaseModel):
  id: int
  bill: float

class ClientModel(BaseModel):
  name: str
  picture: str
  bars: list[BarModel]
  date_add: str

client_views = Blueprint('client_views', __name__, url_prefix='/api')

@client_views.get('/clients/sum')
def clients_sum():
  q = db.select(Client.name, func.sum(Bills.bill)).join(Client.bills).join(Bills.bar).group_by(Client.name)
  sums = db.session.execute(q)
  res = []
  for s in sums:
    res.append({'name':s[0], 'bill':s[1]})
  response = jsonify(res)
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response

@client_views.post('/clients/upload')
def client_upload():
  pic = request.files['picture']
  # Needs validation
  pic.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(pic.filename)))
  headers = {"Access-Control-Allow-Origin": "*"}
  return secure_filename(pic.filename), 200, headers

@client_views.route('/clients/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

class ClientAPI(MethodView):
  def get(self, id: int = 0):
    '''
    Get single or all clients
    '''
    if not id:
      clients = db.session.execute(db.select(Client)).scalars()
      res = []
      for c in clients:
        client_data = {'name': c.name, 'picture': c.picture, 'date_add': c.created_at, 'bars': []}
        for bill in c.bills:
          client_data['bars'].append({'name': bill.bar.name, 'bill': bill.bill})
        res.append(client_data)
      
      response = jsonify(res)
      response.headers.add("Access-Control-Allow-Origin", "*")
      return response
    
    try:
      client = db.session.execute(db.select(Client).filter_by(id=id)).scalar_one()
      res = {'name': client.name, 'bars': []}
      for bill in client.bills:
        res['bars'].append({
          'name':bill.bar.name,
          'bill':bill.bill
          })
      return res
    
    except:
      abort(404)

  def options(self):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "3600",
    }

    return "", 204, headers


  def post(self):
    '''
    Insert a new Client
    '''
    try:
      ClientModel.model_validate_json(request.get_data())
    except ValidationError as e:
      abort(500, e)

    client = Client()
    
    data = request.json
    
    if not data["name"]:
      abort(404, description="Client name is required")
    
    # add name
    client.name = data["name"]
    
    if data.get("bars"):
      # adding bills (needs existing Bar id)
      for bar in data["bars"]:
        bar = db.get_or_404(Bar, bar["id"], description="Bar id didn't found any bar on db.")
        bill = Bills(bill=bar["bill"])
        bill.bar_id = bar.id
        client.bills.append(bill)
    
    try:
      db.session.add(client)
      db.session.commit()
      headers = {"Access-Control-Allow-Origin": "*"}
      return "Client Added Successfully", 200, headers
    
    except Exception as exp:
      abort(500, exp)


  def patch(self, id):
    '''
    Add new Bill for existing Client
    '''
    client = db.get_or_404(Client, id)
    
    data = request.json
    
    for bill in data["bills"]:
        bar = db.get_or_404(Bar, bill["bar"], description="Bar id didn't found any bar on db.")
        bill = Bills(bill=bill["bill"])
        bill.bar_id = bar.id
        client.bills.append(bill)
    
    try:
      db.session.add(client)
      db.session.commit()
      return "The Bills were added succesfully"
    
    except Exception as exp:
      abort(500, exp)


  def delete(self, id):
    '''
    Delete a single client
    '''
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
