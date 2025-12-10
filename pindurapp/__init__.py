from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('pindurapp.settings.DefaultSettings')
app.config.from_pyfile('instance_settings.py')

db = SQLAlchemy(app)

from pindurapp.views.clients import client_views
from pindurapp.views.bars import bar_views
app.register_blueprint(client_views)
app.register_blueprint(bar_views)

@app.errorhandler(HTTPException)
def handle_bad_request(e):
    return jsonify(error=str(e)), e.code

@app.cli.command("gcp")
def gcp():
  from pindurapp.helpers.gcp import view_users
  view_users()

@app.cli.command("create-db")
def create_db():
  db.create_all()

@app.cli.command("drop-db")
def drop_db():
  db.drop_all()

@app.cli.command("seed")
def seed():
  from pindurapp.helpers.command import seed_db
  seed_db()

@app.route("/")
def home():
    return render_template("index.html")


