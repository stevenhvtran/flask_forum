# flask_forum

A forum API backend created in Flask. ReactJS front-end can be found [here](https://github.com/stevenhvtran/react_forum)

Run ```pytest tests/ --cov forum_app/``` in command line from flask_forum directory to run tests.

How to run the development Flask server in Windows 10:
1. Set the environment variables:
```
set FLASK_APP=forum_app
set FLASK_ENV=development
set DATABASE_URL=%DATABASE_URL%
set SECRET_KEY=%RANDOMLY_GENERATED_KEY%
```
2. Run the development server:
```
flask run
```
