from app import db, app  # Import both 'db' and 'app' from your Flask app

# Create an application context
with app.app_context():
    db.create_all()  # Create all tables
