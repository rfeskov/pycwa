from flask import Blueprint

bp = Blueprint('main', __name__, static_folder='static', static_url_path='/main/static')

from app.main import views