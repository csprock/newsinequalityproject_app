from flask import Blueprint

bp = Blueprint('blog', __name__, template_folder=None, static_folder=None)

from app.blog import routes