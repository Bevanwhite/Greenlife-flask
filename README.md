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
-   `from greenlife.models import User, Service, Appointment, Message, Query` - for to add db classes
-   `db.drop_all()` to drop all the tables
-   `from greenlife.seeds import seed_data`
-   `seed_data()`
-   create virtual env using conda `conda create --name venv python=3.12`
-   activate it using `conda activate venv`
    from greenlife import db
    db.drop_all()
    db.create_all()
    from greenlife.seeds import seed_data
    seed_data()
    exit()
    make testpy
