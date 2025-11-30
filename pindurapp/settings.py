from dotenv import load_dotenv
import os

load_dotenv()

class DefaultSettings():
	SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI","No DB")