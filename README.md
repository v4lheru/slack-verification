# Slack Verification Service

A simple Flask application designed specifically for handling Slack events API verification.

## Features

- Responds to Slack challenge requests for URL verification
- Handles Slack OAuth redirects
- Processes Slack interactive components
- Minimal and lightweight

## Deployment

### Railway Deployment

1. Create a new project on [Railway](https://railway.app/)
2. Connect this GitHub repository
3. Railway will automatically detect the Dockerfile and deploy the application

### Local Development

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python app.py
   ```

## Slack Configuration

1. Go to the [Slack API Dashboard](https://api.slack.com/apps) and select your app
2. Under "Event Subscriptions", enable events and add your deployment URL + `/slack/events` as the request URL
3. Under "OAuth & Permissions", add your deployment URL + `/slack/oauth_redirect` as a redirect URL
4. Under "Interactivity & Shortcuts", enable interactivity and add your deployment URL + `/slack/interactive` as the request URL

## License

MIT
