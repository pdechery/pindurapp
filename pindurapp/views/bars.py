from flask import (
  Blueprint,
  abort
)
from flask.views import MethodView


from pindurapp import db
from pindurapp.models import Bar

bar_views = Blueprint('bar_views', __name__, url_prefix='/api')

class BarsAPI(MethodView):
  def __init__(self):
    pass

  def get(self, id: int = None):
    if not id:
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
    try:
      bar = db.session.execute(db.select(Bar).filter_by(id=id)).scalar_one()
      res = {'nome': bar.name, 'clients': []}
      for c in bar.clients:
        res['clients'].append({
          'name':c.clients.name,
          'bill':c.bill
          })
        return res 
    except:
      abort(404) 

  def post(self):
    return "This is Client POST function"


bar_views.add_url_rule('/bars', 'bars_all', view_func=BarsAPI.as_view('bars_api'))
bar_views.add_url_rule('/bars/<int:id>', 'bars_single', view_func=BarsAPI.as_view('bars_api'))

