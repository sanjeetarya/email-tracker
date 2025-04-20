from flask import Flask, send_file

app = Flask(__name__)

@app.route('/track/<email_id>')
def track(email_id):
    print(f"Tracking opened email: {email_id}")
    return send_file("pixel.png", mimetype='image/png')

@app.route('/')
def home():
    return "Tracking Pixel Server is Running!"
