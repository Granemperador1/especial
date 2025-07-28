#!/bin/bash
echo "Building MindSchool application..."

# Install Python dependencies
pip install -r requirements.txt

# Create database if it doesn't exist
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Database initialized successfully')
"

echo "Build completed successfully!" 