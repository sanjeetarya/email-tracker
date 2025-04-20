from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route('/track/<email_id>')
def track(email_id):
    print(f"Tracking opened email: {email_id}")
    return send_file("pixel.png", mimetype='image/png')

@app.route('/')
def home():
    return "Tracking Pixel Server is Running!"

# ✅ This is important for Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
