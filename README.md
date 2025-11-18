# 🤖 LinkedIn Scraper avec Selenium - Analyse de Sentiments Yas

## 📋 Vue d'ensemble

Solution complète pour extraire et analyser les sentiments des posts LinkedIn de l'opérateur Yas. Cette solution utilise Selenium pour automatiser la collecte de données et fournit une analyse détaillée des sentiments clients.

## Environement

1.  Paltform de scraping des donnees
    Cronjob programme toutes les 2 heures
    Connexion LinkedIn
    Navigation page entreprise
    Extraction des commentaire des 30 posts
    Analyse des sentiments
    Sauvegarde des résultat
    Transfert des données vers l’application

2.  VISUALISATION
    Depot Github https://github.com/moukejalo/yas-scraping-nlp
    Deployment de l’app sur Streamlit https://yas-scraping-nlp-group5.streamlit.app/
    Dashboard des sentiments par poste
    Categorization des postes
    Graphe et courbe des données



## Architecture du Projet
1. SCRAPER LINKEDIN (Selenium)
   - Authentification sécurisée
   - Extraction données temps réel

2. ANALYSE SENTIMENTS
   - Pipeline Transformer (XLM Roberta)
   - Classification automatique
   - Score de polarité

3. DASHBOARD STREAMLIT
   - Visualisation interactive
   - Recommandations intelligentes


## ORGANISATION :
    yas-scraping-nlp/
    ├── app.py (Dashboard Streamlit)
    ├── linkedin_scraper_selenium.py
    ├── requirements.txt
    ├── prod-data/
    ├── run_backend.sh/
    └── secrets ou .env

## run_backend.sh
    #!/bin/bash

    # Exit on error
    set -e

    # Change to project directory
    cd /Users/mdiallo/mprojects/etudes/DIT/nlp/yas-sentiment-analysis

    # Activate virtual environment
    source nplenv/bin/activate

    # Run the scraper
    python linkedin_scraper_selenium.py

    # Git operations
    git add .
    git commit -m "adding created files"
    git push origin master

    echo "Script completed successfully!"

## Fichier .env
    # email LinkedIn
    LINKEDIN_EMAIL=**************@**********

    # mot de passe LinkedIn
    LINKEDIN_PASSWORD=********************

    # nom de l'entreprise à analyser
    COMPANY_NAME=yas-senegal

    # nombre maximum de posts à extraire
    MAX_POSTS=30

    # production data files
    PROD_DATA = 'prod-data'

## Ficher requirements
    selenium
    webdriver-manager
    pandas
    numpy
    textblob
    textblob-fr
    streamlit
    plotly  
    openpyxl
    python-dotenv
    beautifulsoup4
    transformers 
    torch
    langdetect
    tiktoken
    sentencepiece
    protobuf

    pip install -r requirements.txt

## configurer le script run_backend pour s'executer toutes les 2 heures
0 */2 * * * /Users/mdiallo/mprojects/etudes/DIT/nlp/yas-sentiment-analysis/run_backend.sh

## lancer le scraping manuellement
    # Activate virtual environment
    source nplenv/bin/activate

    # Run the scraper
    python linkedin_scraper_selenium.py