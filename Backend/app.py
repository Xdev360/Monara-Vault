# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from scheduler import schedule_tweet, client
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Route to schedule a tweet
@app.route('/schedule', methods=['POST'])
def schedule():
    data = request.json
    tweet_text = data.get("text")
    schedule_time = data.get("time")
    
    if not tweet_text:
        return jsonify({"status": "error", "message": "Tweet text is required."}), 400

    try:
        # Parse the datetime string
        schedule_time = datetime.strptime(schedule_time, '%Y-%m-%dT%H:%M')
        schedule_tweet(tweet_text, schedule_time)
        return jsonify({"status": "success", "message": "Tweet scheduled successfully!"}), 200
    except ValueError as e:
        return jsonify({
            "status": "error", 
            "message": f"Invalid date/time format: {e}. Use 'YYYY-MM-DDTHH:MM'."
        }), 400

@app.route('/test-tweet', methods=['POST'])
def test_tweet():
    print("Test tweet endpoint hit!")  # Debug print
    try:
        data = request.get_json()
        tweet_text = data.get('text', "Test tweet from scheduler app")
        
        response = client.create_tweet(text=tweet_text)
        print(f"Tweet response: {response}")  # Debug print
        
        return jsonify({
            "status": "success", 
            "message": "Test tweet posted successfully!",
            "tweet_id": str(response.data['id'])
        }), 200
    except Exception as e:
        error_msg = f"Error in test tweet: {str(e)}"
        print(error_msg)  # Debug print
        return jsonify({
            "status": "error", 
            "message": error_msg
        }), 400

# Add a simple test route
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "pong"}), 200

if __name__ == '__main__':
    app.run(debug=True)
