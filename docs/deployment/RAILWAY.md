# Deploying CompITA Report Generator to Railway

This guide explains how to deploy the CompITA Report Generator to [Railway](https://railway.app/), a modern cloud platform that makes it easy to deploy web applications.

## Prerequisites

1. A [Railway](https://railway.app/) account
2. [Railway CLI](https://docs.railway.app/develop/cli) installed (optional, but recommended)
3. Git repository with your CompITA Report Generator code

## Configuration Files

The following files have been added to the project to support Railway deployment:

- `Procfile`: Tells Railway how to run the application
- `railway.json`: Railway-specific configuration
- `env.example`: Example environment variables (rename to `.env` for local testing)
- `runtime.txt`: Specifies the Python version

## Deployment Steps

### Option 1: Deploy via Railway Dashboard

1. Log in to your [Railway Dashboard](https://railway.app/dashboard)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your CompITA Report Generator repository
4. Railway will automatically detect the configuration and deploy your app
5. Once deployed, go to the "Settings" tab to configure environment variables

### Option 2: Deploy via Railway CLI

1. Install the Railway CLI:
   ```bash
   npm i -g @railway/cli
   ```

2. Log in to your Railway account:
   ```bash
   railway login
   ```

3. Initialize a new project:
   ```bash
   railway init
   ```

4. Deploy your application:
   ```bash
   railway up
   ```

5. Open your deployed application:
   ```bash
   railway open
   ```

## Environment Variables

Configure the following environment variables in your Railway project settings:

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Port for the application to listen on | Automatically set by Railway |
| `ASSETS_DIR` | Directory for storing assets | `assets` |
| `REPORTS_DIR` | Directory for storing reports | `reports` |
| `ENVIRONMENT` | Environment (`development` or `production`) | `production` |
| `DEBUG` | Enable debug mode | `false` |
| `ALLOWED_ORIGINS` | Comma-separated list of allowed origins for CORS | `*` |
| `ENABLE_PERSISTENCE` | Enable file persistence | `true` |

## Persistent Storage

Railway applications are ephemeral by default, meaning files written to the filesystem won't persist between deploys or restarts. To enable persistent storage:

1. In your Railway dashboard, go to your project
2. Click "New" → "Database" → "Volume"
3. Once created, attach it to your service
4. Set the mount path to `/data`
5. Update your environment variables:
   ```
   ASSETS_DIR=/data/assets
   REPORTS_DIR=/data/reports
   ```

## Custom Domain

To use a custom domain with your Railway deployment:

1. In your Railway dashboard, go to your project
2. Click on the "Settings" tab
3. Scroll down to "Domains"
4. Click "Generate Domain" or "Add Custom Domain"
5. Follow the instructions to set up DNS records if using a custom domain

## Monitoring and Logs

Railway provides built-in monitoring and logging:

1. In your Railway dashboard, go to your project
2. Click on the "Metrics" tab to view performance metrics
3. Click on the "Logs" tab to view application logs

## Troubleshooting

If you encounter issues with your Railway deployment:

1. Check the application logs in the Railway dashboard
2. Verify that all required environment variables are set correctly
3. Ensure the application works locally before deploying
4. Check that your `railway.json` and `Procfile` are correctly configured

### Connection Errors

If you encounter errors like `error sending request for url` when using the Railway CLI:

1. **Verify your authentication**:
   ```bash
   railway logout
   railway login
   ```

2. **Check your network connection** - ensure you have a stable internet connection and that no firewalls are blocking Railway's domains.

3. **Link your project properly**:
   ```bash
   railway link
   ```

4. **Try the web dashboard** instead of the CLI for deployment.

5. **Update the Railway CLI**:
   ```bash
   npm update -g @railway/cli
   ```

6. **Check Railway status** at [status.railway.app](https://status.railway.app) to see if there are any ongoing service issues.

For more help, refer to the [Railway documentation](https://docs.railway.app/) or contact Railway support.
