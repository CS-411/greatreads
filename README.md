# greatreads
#How to Run Welcome Page
git clone project_url
git checkout welcome
git pull
cd flask_tutorial
#Then
For Windows cmd, use set instead of export:
> set FLASK_APP=flaskr
> set FLASK_ENV=development

For Windows PowerShell, use $env: instead of export:
> $env:FLASK_APP = "flaskr"
> $env:FLASK_ENV = "development"
#Then
flask init-db
#Then
flask run
#Open
http://127.0.0.1:5000/auth/welcome