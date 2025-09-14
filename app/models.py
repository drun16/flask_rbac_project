# app/models.py

from app import db, login_manager, bcrypt
from flask_login import UserMixin

# The user_loader callback is used to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Association table for the many-to-many relationship between users and roles
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    """
    User model for storing user details.
    Inherits from UserMixin to get default implementations for Flask-Login.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    # Define the many-to-many relationship to Role
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def has_role(self, role_name):
        """Checks if a user has a specific role."""
        for role in self.roles:
            if role.name == role_name:
                return True
        return False

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Role(db.Model):
    """
    Role model for user roles (e.g., Admin, User).
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"Role('{self.name}')"