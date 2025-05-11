# Slack Verification Proxy

A Flask application that handles Slack events API verification and proxies other requests to your main application.

## Features

- Responds to Slack challenge requests for URL verification
- Proxies non-verification requests to your main application
- Handles Slack OAuth redirects
- Processes Slack interactive components
- Minimal and lightweight

## How It Works

This service acts as a proxy between Slack and your main application:

1. When Slack sends a verification challenge, this service responds directly with the challenge value
2. For all other requests (events, OAuth, interactive components), it forwards them to your main application
3. This ensures that your main application still receives all the events and can process them normally

## Deployment

### Railway Deployment

1. Create a new project on [Railway](https://railway.app/)
2. Connect this GitHub repository
3. Set the `MAIN_APP_URL` environment variable to your main application's URL (e.g., `https://slack-supabase-production.up.railway.app`)
4. Railway will automatically detect the Dockerfile and deploy the application

### Local Development

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set the `MAIN_APP_URL` environment variable:
   ```
   export MAIN_APP_URL=https://your-main-app-url.com
   ```
4. Run the application:
   ```
   python app.py
   ```

## Slack Configuration

1. Go to the [Slack API Dashboard](https://api.slack.com/apps) and select your app
2. Under "Event Subscriptions", enable events and add your verification proxy URL + `/slack/events` as the request URL
3. Under "OAuth & Permissions", add your verification proxy URL + `/slack/oauth_redirect` as a redirect URL
4. Under "Interactivity & Shortcuts", enable interactivity and add your verification proxy URL + `/slack/interactive` as the request URL

## License

MIT
