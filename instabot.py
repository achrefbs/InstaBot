#!venv/bin/python3
from app import app, db
import os
from flaskwebgui import FlaskUI
ui = FlaskUI(app)
if __name__ == '__main__':

    if not os.path.exists('db.sqlite'):
        db.create_all()
    ui.run()
