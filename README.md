# GreenLife Wellness Center - using flask

-   make a folder called GreenLife
-   make flask install using - `pip install flask`
-   create a virtual environment using `python -m venv venv`
-   activate the virtual environment and activate using this
-   `. venv/bin/activate` using linux and mac
-   `. venv/scripts/activate` using windows
-   use flask app run when we use `flask run` - `export FLASK_APP=greenlife.py`
-   make flask form install using - `pip install flask-wtf`
-   `from greenlife import db` for import the database
-   `db.create_all()` - for to create db
-   `from greenlife import User, Service, Appointment, Message, Query` - for to add db classes
-   `db.drop_all()` to drop all the tables
