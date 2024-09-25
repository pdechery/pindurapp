from app import db
from app.models import Client, Bar, Bills

def seed_db():
  db.session.execute(db.insert(Client),[
      {"name": "Zeca"},
      {"name": "Biriba"},
      {"name": "Carlim"},
      {"name": "Jones"},
      {"name": "Sr. Paulo"},
      {"name": "Mathias"},
      {"name": "Vira Copo"},
      {"name": "José Paulo"},
  ])
  db.session.execute(db.insert(Bar),[
      {"name": "Amarelinho do Cônego"},
      {"name": "Bar Biriba"},
      {"name": "Petiscaria do Chapéu"},
      {"name": "Amandoeira"},
      {"name": "Café Lazer"},
      {"name": "Bar dos Amigos"},
      {"name": "Bar da Elizete"},
      {"name": "Bom Bar"},
  ])
  db.session.execute(db.insert(Bills),[
      {"bill": 20.50, "client_id": 1, "bar_id": 1},
      {"bill": 50.90, "client_id": 1, "bar_id": 2},
      {"bill": 120, "client_id": 1, "bar_id": 3},
      {"bill": 5.5, "client_id": 1, "bar_id": 4},
      {"bill": 35.5, "client_id": 2, "bar_id": 1},
      {"bill": 24.20, "client_id": 2, "bar_id": 2},
      {"bill": 100, "client_id": 3, "bar_id": 1},
      {"bill": 50, "client_id": 4, "bar_id": 1},
  ])
  db.session.commit()