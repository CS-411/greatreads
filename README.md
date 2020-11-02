# greatreads
## How to Run Welcome Page
1. git clone project_url
1. git checkout welcome
1. git pull
1. cd flask_tutorial
## Setup flask environment
* For Windows cmd, use set instead of export:
  * set FLASK_APP=flaskr
  * set FLASK_ENV=development

* For Windows PowerShell, use $env: instead of export:
  * $env:FLASK_APP = "flaskr"
  * $env:FLASK_ENV = "development"
## Initialize the database
flask init-db
## Run the project
flask run
## Open localhost for welcome page
http://127.0.0.1:5000/auth/welcome
