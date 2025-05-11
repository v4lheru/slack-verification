from flask import Flask, request, jsonify, Response
import os
import logging
import requests
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Get the main application URL from environment variable
MAIN_APP_URL = os.environ.get('MAIN_APP_URL', 'https://slack-supabase-production.up.railway.app')

@app.route('/', methods=['GET'])
def health_check():
    logger.info("Health check endpoint called")
    return jsonify({"status": "ok"})

@app.route('/slack/events', methods=['POST'])
def slack_events():
    logger.info("Slack events endpoint called")
    
    # Log the request headers
    logger.info(f"Headers: {request.headers}")
    
    try:
        # Get the raw request body
        raw_body = request.get_data()
        
        # Try to parse as JSON
        try:
            data = json.loads(raw_body)
            logger.info(f"Request data: {data}")
            
            # Check for challenge
            if data and "challenge" in data:
                challenge = data["challenge"]
                logger.info(f"Responding to Slack challenge: {challenge}")
                return jsonify({"challenge": challenge})
        except json.JSONDecodeError:
            logger.warning("Could not parse request body as JSON")
        
        # For non-challenge events, forward to the main application
        logger.info(f"Forwarding non-challenge event to {MAIN_APP_URL}/slack/events")
        
        # Forward the request to the main application
        try:
            response = requests.post(
                f"{MAIN_APP_URL}/slack/events",
                headers={key: value for key, value in request.headers if key != 'Host'},
                data=raw_body,
                timeout=10
            )
            
            # Return the response from the main application
            logger.info(f"Received response from main application: {response.status_code}")
            return Response(
                response.content,
                status=response.status_code,
                content_type=response.headers.get('Content-Type', 'application/json')
            )
        except requests.RequestException as e:
            logger.error(f"Error forwarding request to main application: {e}")
            # If forwarding fails, just return OK to Slack
            return jsonify({"status": "ok"})
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/slack/oauth_redirect', methods=['GET'])
def slack_oauth_redirect():
    logger.info("Slack OAuth redirect endpoint called")
    
    # Forward to the main application
    try:
        response = requests.get(
            f"{MAIN_APP_URL}/slack/oauth_redirect",
            params=request.args,
            headers={key: value for key, value in request.headers if key != 'Host'},
            timeout=10
        )
        
        # Return the response from the main application
        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers.get('Content-Type', 'application/json')
        )
    except requests.RequestException as e:
        logger.error(f"Error forwarding request to main application: {e}")
        return jsonify({"status": "Authentication successful"})

@app.route('/slack/interactive', methods=['POST'])
def slack_interactive():
    logger.info("Slack interactive endpoint called")
    
    # Forward to the main application
    try:
        response = requests.post(
            f"{MAIN_APP_URL}/slack/interactive",
            headers={key: value for key, value in request.headers if key != 'Host'},
            data=request.get_data(),
            timeout=10
        )
        
        # Return the response from the main application
        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers.get('Content-Type', 'application/json')
        )
    except requests.RequestException as e:
        logger.error(f"Error forwarding request to main application: {e}")
        return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
