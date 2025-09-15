# seed.py

from app import create_app, db
from app.models import Role, User

def seed_data():
    """Seeds the database with initial roles and an admin user."""
    app = create_app()
    with app.app_context():
        # --- Create Roles if they don't exist ---
        if not Role.query.filter_by(name='Admin').first():
            print("Creating Admin role...")
            db.session.add(Role(name='Admin'))
        
        if not Role.query.filter_by(name='User').first():
            print("Creating User role...")
            db.session.add(Role(name='User'))

        # --- Create Admin User if it doesn't exist ---
        # IMPORTANT: Change the email and password to your own secure credentials
        admin_email = 'admin@example.com'
        admin_password = 'a-very-strong-production-password'

        if not User.query.filter_by(email=admin_email).first():
            print(f"Creating admin user ({admin_email})...")
            admin_user = User(username='admin', email=admin_email)
            admin_user.set_password(admin_password)
            admin_role = Role.query.filter_by(name='Admin').first()
            if admin_role:
                admin_user.roles.append(admin_role)
            db.session.add(admin_user)

        db.session.commit()
        print("Database seeding complete.")

if __name__ == '__main__':
    seed_data()