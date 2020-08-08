from flask import Flask

Flask(__name__, static_url_path='/static', static_folder='app')
app = Flask (__name__)
app.config.from_object('config')
from app import views
