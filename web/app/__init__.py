from flask import Flask, render_template
#from flask_s3 import FlaskS3
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)

#s3 = FlaskS3(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

from app.main import bp as main_bp
from app.blog import bp as blog_bp
app.register_blueprint(main_bp)
app.register_blueprint(blog_bp)

from app import models
