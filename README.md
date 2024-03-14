# Orchestration of web application for music recommendation, University of Colorado Boulder

Team Members: Ashwin Umadi

Executing the code
To run the code, you need to build 3 docker files available in /backend, /core & /worker folder.

Then run all the commands in deploy.sh

Make sure to first have Database pod & Database service up and running before running the backend YAML file.

Load Testing
To run the Load testing file, below is the command:

locust -f load_test.py

Before running this test make sure to create a username and password account from the website and use those credentials in the load_test.py file.

Unit test
Go to /backend folder

Now run:

python manage.py test api
