from flask import Flask

import config

app = Flask(__name__)
app.config.from_object(config.Config)

from app import admin_views
from app import client_views
from app import staff_views


