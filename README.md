# flask_forum

A forum API backend created in Flask

How to run tests:\
From directory for flask_forum run in command line:\
pytest tests/ --cov forum_app/

How to run the development Flask server in Windows 10:
1. Set the environment variables:\
set FLASK_APP=forum_app\
set FLASK_ENV=development\
set DATABASE_URL=%DATABASE_URL%\
set SECRET_KEY=%RANDOMLY_GENERATED_KEY%
2. Run the development server:\
flask run
