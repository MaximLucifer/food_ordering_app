from app import create_app, db
from app import models

app = create_app()

app.app_context().push()

def create_tables():
    print("Creating tables...")
    db.create_all()
    print("Tables created")
    