# app/admin.py

from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for
from app import db
from app.models import User, Role
from wtforms import PasswordField 


class MyAdminIndexView(AdminIndexView):
    """
    Custom AdminIndexView to enforce role-based access.
    """
    def is_accessible(self):
        # Only allow users with the 'Admin' role to access the admin dashboard
        return current_user.is_authenticated and current_user.has_role('Admin')

    def inaccessible_callback(self, name, **kwargs):
        # Redirect non-admin users to the main dashboard
        return redirect(url_for('main.dashboard'))

class UserAdminView(ModelView):
    """
    Custom ModelView for the User model.
    """
    # Don't display the password hash in the list view
    column_exclude_list = ('password_hash',)

    #use a custom form that includes a passwordfield
    form_extra_fields = {
        'password': PasswordField('New Password')
    }
    # Don't allow password hash to be edited directly
    form_excluded_columns = ('password_hash',)

    def on_model_change(self, form, model, is_created):
        """
        This method is called when a model is created or updated.
        We use it to hash the password before saving it to the database.
        """
        if form.password.data:
            model.set_password(form.password.data)
    
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('Admin')
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.dashboard'))

# Initialize the Admin interface with the custom index view
admin = Admin(name='Admin Dashboard', template_mode='bootstrap3', index_view=MyAdminIndexView())

# Add views for your models to the admin interface
admin.add_view(UserAdminView(User, db.session))
admin.add_view(ModelView(Role, db.session))