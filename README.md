# flask_forum

A forum, backend created in Flask, Python and a frontend created with JS/HTML/CSS

How to run tests:
From directory for flask_forum run in command line:
pytest tests/ --cov forum_app/

Configuration file for Flask should have:
SQLALCHEMY_DATABASE_URI=%URL-FOR-PSQL%
SECRET_KEY=%RANDOMLY-GENERATED-KEY%
SQLALCHEMY_TRACK_MODIFICATIONS=False

How to run the development Flask server in Windows 10 command line:
set FLASK_APP=forum_app
set FLASK_ENV=development
set FLASK_CONFIG=%PATH-TO-CONFIG-FILE%
flask run
