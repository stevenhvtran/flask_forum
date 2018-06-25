# flask_forum

A forum, backend created in Flask, Python and a frontend created with JS/HTML/CSS

How to run tests:
From directory for flask_forum run in command line:
pytest tests/ --cov forum_app/

How to run the development Flask server in Windows 10 command line:
set FLASK_APP=forum_app
set FLASK_ENV=development
set FLASK_CONFIG=%PATH-TO-CONFIG-FILE%
flask run
