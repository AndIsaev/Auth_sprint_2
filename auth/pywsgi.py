import os

from gevent import monkey

monkey.patch_all()

from dotenv import load_dotenv
from gevent.pywsgi import WSGIServer

from app import app, create_app

load_dotenv()

FLASK_PORT: int = int(os.getenv("FLASK_PORT"))

http_server = WSGIServer(("", FLASK_PORT), create_app(app))
http_server.serve_forever()
