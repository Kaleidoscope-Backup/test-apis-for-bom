from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.secret_key = "super_secret_key_123"  # 🔥 CRITICAL: Hardcoded secret
email = "admin@abc.com"
phone = "+1 555 123 4567"
ssn = "123-45-6789"
test_access_key_id="ASIAYB2REOVTCGBPVKKJ"

@app.route("/search")
def search():
    user_input = request.args.get("username")
    # Vulnerable: Directly embedding user input into raw SQL
    result = db.session.execute(f"SELECT * FROM users WHERE username = '{user_input}'")
    return str(result.fetchall())
