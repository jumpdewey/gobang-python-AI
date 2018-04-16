 
_BLACK = 1
_WHITE = 2
from chessboard import Chessboard
cb = Chessboard()

from flask import Flask, url_for
from config import Config
app = Flask(__name__)
app.config.from_object(Config)
from app import routes, errors