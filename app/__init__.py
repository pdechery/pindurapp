from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('app.settings.DefaultSettings')
app.config.from_pyfile('instance_settings.py')

db = SQLAlchemy(app)

from app.views import views
app.register_blueprint(views)

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


