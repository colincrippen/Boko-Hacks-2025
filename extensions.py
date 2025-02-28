from flask_sqlalchemy import SQLAlchemy
from flask_mailman import Mail
from flask_migrate import Migrate

db = SQLAlchemy()
mail = Mail()
migrate = Migrate()