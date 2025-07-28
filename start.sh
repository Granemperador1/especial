#!/bin/bash
echo "Starting MindSchool application..."

# Set environment variables if not set
export FLASK_ENV=${FLASK_ENV:-production}
export SECRET_KEY=${SECRET_KEY:-default-secret-key-change-in-production}

# Start the application
exec gunicorn --bind 0.0.0.0:$PORT wsgi:app 