#!/bin/bash

# Configuration
REPO_DIR="/root/nm_test_bot"
SERVICE_NAME="bot" # Name used in systemctl

echo "🚀 Starting Automated Deployment..."

cd $REPO_DIR || exit

# 1. Pull latest code
echo "📥 Pulling latest code from GitHub..."
git pull origin main

# 2. Update dependencies
echo "📦 Updating dependencies..."
# Assumes virtualenv is at $REPO_DIR/venv
if [ -d "venv" ]; then
    source venv/bin/python -m pip install -r requirements.txt
else
    pip install -r requirements.txt
fi

# 3. Restart the bot service
echo "♻️ Restarting Bot Service..."
sudo systemctl restart $SERVICE_NAME

# 4. Success message
echo "✅ Deployment Successful!"
echo "Timestamp: $(date)"
