#!/bin/bash

# Exit on error
set -e

# Change to project directory
cd /Users/mdiallo/mprojects/etudes/DIT/nlp/yas-sentiment-analysis

# Activate virtual environment
source nplenv/bin/activate

# Run the scraper
python linkedin_scraper_selenium.py

Git operations
git add .
git commit -m "adding created files"
git push origin master

echo "Script completed successfully!"
