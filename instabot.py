#!venv/bin/python3
from app import app, db
import os

if __name__ == '__main__':

    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(debug=True)