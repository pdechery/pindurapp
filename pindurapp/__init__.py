from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('pindurapp.settings.DefaultSettings')
app.config.from_pyfile('instance_settings.py')

db = SQLAlchemy(app)

from pindurapp.views import views
app.register_blueprint(views)

@app.errorhandler(HTTPException)
def handle_bad_request(e):
    return jsonify(error=str(e)), e.code

@app.cli.command("gcp")
def gcp():
  from app.helpers.gcp import view_users
  view_users()

@app.cli.command("create-db")
def create_db():
  db.create_all()

@app.cli.command("seed")
def seed():
  from app.helpers.command import seed_db
  seed_db()

@app.route("/")
def home():
    return render_template("index.html")


