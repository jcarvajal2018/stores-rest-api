from app import app
from db import db

db.init_app(app)
@app.before_first_request
def create_TABLES():
    db.create_all()
