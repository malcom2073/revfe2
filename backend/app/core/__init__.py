from flask import Flask
#import db
app = Flask(__name__)
username="postgres"
password="postgres"
hostname="localhost"
port="5432"
databasename="test_db"
SUCCESS_STR = "SUCCESS"
FAIL_STR = "FAILURE"
STATUS_KEY = "STATUS"
ERROR_KEY = "ERROR"
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://" + username + ":" + password + "@" + hostname + ":" + port + "/" + databasename
SQLALCHEMY_MAIN_URI = "postgresql+psycopg2://" + username + ":" + password + "@" + hostname + ":" + port
@app.route("/")
def index():
    return "<p>Hello there!</p>"

