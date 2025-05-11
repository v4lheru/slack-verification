from flask import Flask, request, jsonify
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def health_check():
    logger.info("Health check endpoint called")
    return jsonify({"status": "ok"})

@app.route('/slack/events', methods=['POST'])
def slack_events():
    logger.info("Slack events endpoint called")
    
    # Log the request headers and body
    logger.info(f"Headers: {request.headers}")
    
    try:
        # Get the request data
        data = request.json
        logger.info(f"Request data: {data}")
        
        # Check for challenge
        if data and "challenge" in data:
            challenge = data["challenge"]
            logger.info(f"Responding to Slack challenge: {challenge}")
            return jsonify({"challenge": challenge})
        
        # For other events, just return OK
        logger.info("Non-challenge event received")
        return jsonify({"status": "ok"})
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/slack/oauth_redirect', methods=['GET'])
def slack_oauth_redirect():
    logger.info("Slack OAuth redirect endpoint called")
    return jsonify({"status": "Authentication successful"})

@app.route('/slack/interactive', methods=['POST'])
def slack_interactive():
    logger.info("Slack interactive endpoint called")
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
