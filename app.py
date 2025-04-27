import os
from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime


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
    unique_id = Column(String, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)
    user_agent = Column(String)  # New column to store user agent
    ip_address = Column(String)  # New column to store IP address

Base.metadata.create_all(engine)

# Pixel route for tracking email open
@app.route("/track/<unique_id>")
def track_email(unique_id):
    try:
        # Get the user agent and IP address from the request
        user_agent = request.headers.get('User-Agent', 'Unknown')
        if not user_agent:
            user_agent = 'Unknown'  # Default value if user agent is missing or invalid

        ip_address = request.remote_addr
        if not ip_address:
            ip_address = '0.0.0.0'  # Default value if IP address is missing or invalid

        # Add a new row with a timestamp, user agent, and IP address
        new_entry = Tracking(
            unique_id=unique_id,
            timestamp=datetime.now(),
            user_agent=user_agent,
            ip_address=ip_address
        )
        session.add(new_entry)
        session.commit()

        # Return a 1x1 transparent image
        return send_file("pixel.png", mimetype='image/png')
    except Exception as e:
        # Log the error and return a generic error response
        print(f"Error tracking email: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/status/<unique_id>")
def get_status(unique_id):
    # Fetch all rows for the given unique_id
    entries = session.query(Tracking).filter_by(unique_id=unique_id).all()
    if entries:
        # Return all rows as a list of dictionaries
        return jsonify([
            {
                "unique_id": entry.unique_id,
                "timestamp": entry.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "user_agent": entry.user_agent,  # Include user agent
                "ip_address": entry.ip_address  # Include IP address
            }
            for entry in entries
        ]), 200
    else:
        return jsonify({"error": "Not found"}), 404



# ✅ This is important for Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
