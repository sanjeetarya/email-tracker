# from flask import Flask, send_file
import os

# app = Flask(__name__)

# @app.route('/track/<email_id>')
# def track(email_id):
#     print(f"Tracking opened email: {email_id}")
#     return send_file("pixel.png", mimetype='image/png')

# @app.route('/')
# def home():
#     return "Tracking Pixel Server is Running!"/

from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
CORS(app)

# Setup SQLite DB
DATABASE_URL = "sqlite:///tracking.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

class Tracking(Base):
    __tablename__ = 'tracking'
    email_id = Column(String, primary_key=True)
    status = Column(String, default="not opened")
    click_count = Column(Integer, default=0)

Base.metadata.create_all(engine)

# Pixel route for tracking email open
@app.route("/track/<email_id>")
def track_email(email_id):
    # Track email open and increment click count
    entry = session.query(Tracking).filter_by(email_id=email_id).first()
    if entry:
        entry.status = "opened"
        entry.click_count += 1
    else:
        entry = Tracking(email_id=email_id, status="opened", click_count=1)
        session.add(entry)
    session.commit()

    # Return a 1x1 transparent image
    return send_file("pixel.png", mimetype='image/png')

@app.route("/status/<email_id>")
def get_status(email_id):
    entry = session.query(Tracking).filter_by(email_id=email_id).first()
    if entry:
        return jsonify({
            "email_id": entry.email_id,
            "status": entry.status,
            "click_count": entry.click_count
        }), 200
    else:
        return jsonify({"error": "Not found"}), 404



# ✅ This is important for Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
