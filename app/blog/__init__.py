from flask import Blueprint

bp = Blueprint('blog', __name__, template_folder='app/static/blog')

from app.blog import routes