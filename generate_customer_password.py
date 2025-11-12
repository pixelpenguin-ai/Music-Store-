import random
import string
from app import app, db, customer  # import your Flask app, db, and customer model
from werkzeug.security import generate_password_hash

def generate_password(length=10):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

# Run inside the Flask application context
with app.app_context():
    all_customers = customer.query.all()
    
    for c in all_customers:
        new_password = generate_password()
        hashed_password = generate_password_hash(new_password)
        c.password_hash = hashed_password
        db.session.commit()
        print(f"{c.first_name} {c.last_name}: {new_password}")
