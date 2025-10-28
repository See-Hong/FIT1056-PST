import datetime as dt
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from app.models import User, db
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.appointments import appointment_bp
from routes.home import home_bp
from routes.profile import profile_bp
from routes.reports import report_bp
from routes.staff import staff_bp
from faker_tool import seed_all
# App setup
app = Flask(__name__)

# Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(report_bp)
app.register_blueprint(appointment_bp)
app.register_blueprint(home_bp)


app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)
app.config['PERMANENT_SESSION_LIFETIME'] = dt.timedelta(minutes=10)

# Databases
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db.init_app(app)

with app.app_context():
    db.create_all()
    # Faker for sample data
    # seed_all()



# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login_page"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

if __name__ == "__main__":
    app.run(debug=True)