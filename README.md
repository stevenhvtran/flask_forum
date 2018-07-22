# Flask Forum

A forum API backend created in Flask. ReactJS front-end can be found [here](https://github.com/stevenhvtran/react_forum)

## How to run tests

Run ```pytest tests/ --cov forum_app/``` in command line from flask_forum directory to run tests.

## How to run the development Flask server in Windows 10:
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


## How to use Flask Forum API

The base API URL is https://flask-forum-api.herokuapp.com/api
All requests should be made to an endpoint of this base URL
Examples are written for the requests module in Python, use .json() to see the JSON response

### Endpoints:
/posts  
Methods: GET  
Use a GET request to get a list of all the posts created
eg. requests.get(url=base_url + '/posts')

/register  
Methods: POST  
Use a POST request with JSON to create a new user
JSON format: {'username': username, 'password': password}
eg. requests.post(url=base_url + '/register', json={'username': 'user123', 'password': 'pw123'}

/post/\<int:post_id>  
Methods: GET, PUT, DELETE  
Use a GET request to get information about the specific post
eg. requests.get(url=base_url + '/post/1')  
Use a PUT request to edit the post with the corresponding post id. Only works if Post was created by same user
JSON format: {'title': new_title, 'body': new_body}
eg. requests.put(url=base_url + '/post/1', json={'title': 'new title', 'body': 'new body'}, auth=('user123', 'pw123')}  
Use a DELETE request to delete the psot with the corresponding post id. Only works if Post was created by same user
eg. requests.delete(url=base_url + '/post/1', auth=('user123', 'pw123')}
