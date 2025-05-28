from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
AWS_ACCESS_KEY = "ADSOIFNEOHFHW"
@app.route("/search")
def search():
    user_input = request.args.get("username")
    # Vulnerable: Directly embedding user input into raw SQL
    result = db.session.execute(f"SELECT * FROM users WHERE username = '{user_input}'")
    return str(result.fetchall())
