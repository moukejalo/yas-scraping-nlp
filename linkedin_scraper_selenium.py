"""
LinkedIn Scraper avec Selenium - Opérateur Yas
ATTENTION: Ce script est fourni à des fins éducatives uniquement.
Le scraping de LinkedIn peut violer leurs conditions d'utilisation.

Utilisez à vos propres risques et assurez-vous d'avoir les autorisations nécessaires.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from datetime import datetime
import json
import os
from textblob import TextBlob
import random
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import streamlit as st



class LinkedInScraper:
    """
    Scraper LinkedIn pour extraire les posts d'une entreprise
    """
    
    def __init__(self, email, password, headless=False):

        if not email or not password:
            print("❌ Identifiants LinkedIn manquants.")
            print("💡 Configurez les variables d'environnement LINKEDIN_EMAIL et LINKEDIN_PASSWORD")
            return
        
        self.email = email
        self.password = password

        company_posts_url = "https://www.linkedin.com/company/promobilesn/posts/"

        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        # """
        # Initialise le scraper
        
        # Args:
        #     email: Email LinkedIn
        #     password: Mot de passe LinkedIn
        #     headless: Exécuter sans interface graphique
        # """
        # self.email = email
        # self.password = password
        
        # # Configuration du navigateur Chrome
        # chrome_options = Options()
        
        # # if headless:
        # #     chrome_options.add_argument("--headless")
        
        # # # Options pour éviter la détection
        # # chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # # chrome_options.add_experimental_option('useAutomationExtension', False)
        # # chrome_options.add_argument("--disable-gpu")
        # # chrome_options.add_argument("--no-sandbox")
        # # chrome_options.add_argument("--disable-dev-shm-usage")
        # # chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # # self.driver = webdriver.Chrome(options=chrome_options)

        # chrome_options = Options()
        # chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # self.wait = WebDriverWait(self.driver, 20)
        
        print("✅ Navigateur initialisé")
    
    def random_delay(self, min_seconds=2, max_seconds=5):
        """Ajoute un délai aléatoire pour simuler un comportement humain"""
        time.sleep(random.uniform(min_seconds, max_seconds))
    
    def login(self):
        self.driver.get("https://www.linkedin.com/login")
        wait = WebDriverWait(self.driver, 20)

        email_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
        email_input.send_keys(self.email)

        pwd_input = self.driver.find_element(By.ID, "password")
        pwd_input.send_keys(self.password)
        pwd_input.submit()

        # # Vérifier si la connexion a réussi
        # if "feed" in self.driver.current_url or "mynetwork" in self.driver.current_url:
        #     print("✅ Connexion réussie!")
        #     return True
        # else:
        #     print("⚠️ Connexion échouée - Vérifiez vos identifiants")
        #     return False

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "nav")))
            return True
        except Exception:
            # print("⚠️ Vérifie le navigateur : LinkedIn peut demander un code 2FA.")
            # time.sleep(15)
            print("⚠️ Connexion échouée - Vérifiez vos identifiants")
            return False

    def loginO(self):
        """
        Connexion à LinkedIn
        """
        try:
            print("🔐 Connexion à LinkedIn...")
            self.driver.get("https://www.linkedin.com/login")
            self.random_delay(2, 4)
            
            # Saisie de l'email
            email_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_input.send_keys(self.email)
            self.random_delay(1, 2)
            
            # Saisie du mot de passe
            password_input = self.driver.find_element(By.ID, "password")
            password_input.send_keys(self.password)
            self.random_delay(1, 2)
            
            # Clic sur le bouton de connexion
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            print("⏳ Attente de la connexion...")
            self.random_delay(5, 7)
            
            # Vérifier si la connexion a réussi
            if "feed" in self.driver.current_url or "mynetwork" in self.driver.current_url:
                print("✅ Connexion réussie!")
                return True
            else:
                print("⚠️ Connexion échouée - Vérifiez vos identifiants")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors de la connexion: {e}")
            return False
    
    def navigate_to_company_page(self, company_name):
        """
        Navigue vers la page d'une entreprise
        
        Args:
            company_name: Nom de l'entreprise (ex: "Yas Guinée")
        """
        try:
            print(f"🔍 Recherche de l'entreprise: {company_name}")
            
            # # Recherche de l'entreprise
            # search_url = f"https://www.linkedin.com/search/results/companies/?keywords={company_name}"
            # self.driver.get(search_url)
            # self.random_delay(3, 5)
            
            # # Cliquer sur le premier résultat
            # first_result = self.wait.until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, ".entity-result__title-text a"))
            # )
            # company_url = first_result.get_attribute("href")
            company_url = f"https://www.linkedin.com/company/{company_name}"
            
            
            # Aller sur la page de l'entreprise
            self.driver.get(company_url)
            self.random_delay(3, 5)
            
            # Aller sur l'onglet Posts
            posts_url = company_url.rstrip('/') + "/posts/"
            print(f"🔍 Navigation vers la page de l'entreprise post: {posts_url}")
            self.driver.get(posts_url)
            self.random_delay(3, 5)
            
            print(f"✅ Page de l'entreprise chargée: {posts_url}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la navigation: {e}")
            return False
    
    def scroll_to_load_posts(self, num_scrolls=5):
        """
        Fait défiler la page pour charger plus de posts
        
        Args:
            num_scrolls: Nombre de fois à défiler
        """
        print(f"📜 Chargement des posts (scrolling {num_scrolls} fois)...")
        
        for i in range(num_scrolls):
            # Scroll vers le bas
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.random_delay(2, 4)
            print(f"   Scroll {i+1}/{num_scrolls} effectué")
        
        # Remonter en haut
        self.driver.execute_script("window.scrollTo(0, 0);")
        self.random_delay(2, 3)
    
    def extract_posts(self, max_posts=30):
        """
        Extrait les posts de l'entreprise
        
        Args:
            max_posts: Nombre maximum de posts à extraire
            
        Returns:
            Liste de dictionnaires contenant les données des posts
        """
        posts_data = []
        
        try:
            print(f"📊 Extraction de {max_posts} posts maximum...")
            
            # Trouver tous les conteneurs de posts
            posts = self.driver.find_elements(By.CSS_SELECTOR, ".feed-shared-update-v2")
            
            print(f"   {len(posts)} posts trouvés sur la page")
            
            for idx, post in enumerate(posts[:max_posts]):
                try:
                    # Scroll jusqu'au post pour le rendre visible
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", post)
                    self.random_delay(0.5, 1)
                    
                    # Extraire le texte du post
                    try:
                        text_element = post.find_element(By.CSS_SELECTOR, ".feed-shared-update-v2__description, .feed-shared-text")
                        post_text = text_element.text.strip()
                    except NoSuchElementException:
                        post_text = ""
                    
                    # Extraire la date (approximative)
                    try:
                        date_element = post.find_element(By.CSS_SELECTOR, ".feed-shared-actor__sub-description")
                        date_text = date_element.text.strip()
                        post_date = self.parse_linkedin_date(date_text)
                    except NoSuchElementException:
                        post_date = datetime.now().strftime('%Y-%m-%d')
                    
                    # Extraire les statistiques d'engagement
                    try:
                        reactions = post.find_element(By.CSS_SELECTOR, ".social-details-social-counts__reactions-count")
                        reactions_count = int(''.join(filter(str.isdigit, reactions.text)))
                    except (NoSuchElementException, ValueError):
                        reactions_count = 0
                    
                    try:
                        comments = post.find_element(By.CSS_SELECTOR, ".social-details-social-counts__comments")
                        comments_count = int(''.join(filter(str.isdigit, comments.text)))
                    except (NoSuchElementException, ValueError):
                        comments_count = 0
                    
                    # Analyser le sentiment
                    sentiment, score = self.analyze_sentiment(post_text)
                    topic = self.classify_topic(post_text)
                    
                    post_data = {
                        'date': post_date,
                        'topic': topic,
                        'comment': post_text,
                        'sentiment': sentiment,
                        'score': score,
                        'reactions': reactions_count,
                        'comments': comments_count,
                        'engagement': reactions_count + comments_count
                    }
                    
                    posts_data.append(post_data)
                    print(f"   ✅ Post {idx+1}/{min(len(posts), max_posts)} extrait - {topic} ({sentiment})")
                    
                except Exception as e:
                    print(f"   ⚠️ Erreur extraction post {idx+1}: {e}")
                    continue
            
            print(f"✅ {len(posts_data)} posts extraits avec succès!")
            return posts_data
            
        except Exception as e:
            print(f"❌ Erreur lors de l'extraction: {e}")
            return posts_data
    
    def parse_linkedin_date(self, date_text):
        """
        Parse le texte de date LinkedIn (ex: "il y a 2 jours")
        
        Args:
            date_text: Texte de la date LinkedIn
            
        Returns:
            Date au format YYYY-MM-DD
        """
        from datetime import timedelta
        
        date_text = date_text.lower()
        today = datetime.now()
        
        if "minute" in date_text or "min" in date_text:
            return today.strftime('%Y-%m-%d')
        elif "heure" in date_text or "hour" in date_text:
            return today.strftime('%Y-%m-%d')
        elif "jour" in date_text or "day" in date_text:
            days = int(''.join(filter(str.isdigit, date_text)))
            date = today - timedelta(days=days)
            return date.strftime('%Y-%m-%d')
        elif "semaine" in date_text or "week" in date_text:
            weeks = int(''.join(filter(str.isdigit, date_text)))
            date = today - timedelta(weeks=weeks)
            return date.strftime('%Y-%m-%d')
        elif "mois" in date_text or "month" in date_text:
            months = int(''.join(filter(str.isdigit, date_text)))
            date = today - timedelta(days=months*30)
            return date.strftime('%Y-%m-%d')
        else:
            return today.strftime('%Y-%m-%d')
    
    def analyze_sentiment(self, text):
        """
        Analyse le sentiment d'un texte
        
        Args:
            text: Texte à analyser
            
        Returns:
            Tuple (sentiment, score)
        """
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                return 'positif', polarity
            elif polarity < -0.1:
                return 'négatif', polarity
            else:
                return 'neutre', polarity
        except:
            return 'neutre', 0.0
    
    def classify_topic(self, text):
        """
        Classifie le sujet d'un post
        
        Args:
            text: Texte du post
            
        Returns:
            Catégorie du sujet
        """
        text_lower = text.lower()
        
        keywords = {
            'Réseau': ['réseau', '4g', '5g', 'connexion', 'signal', 'antenne'],
            'Service Client': ['service', 'client', 'support', 'aide', 'assistance', 'équipe'],
            'Prix': ['prix', 'tarif', 'coût', 'facture', 'promotion', 'offre', 'réduction'],
            'Internet': ['internet', 'data', 'débit', 'vitesse', 'téléchargement', 'navigation'],
            'Couverture': ['couverture', 'zone', 'rural', 'urbain', 'région', 'national'],
            'Application': ['app', 'application', 'mobile', 'interface', 'smartphone'],
            'Offres': ['forfait', 'package', 'abonnement', 'plan', 'souscription']
        }
        
        for topic, words in keywords.items():
            if any(word in text_lower for word in words):
                return topic
        
        return 'Autre'
    
    def save_to_csv(self, posts_data, filename=None):
        """
        Sauvegarde les données dans un fichier CSV
        
        Args:
            posts_data: Liste des posts
            filename: Nom du fichier (optionnel)
        """

        # Define the save directory
        save_dir = "data"
        os.makedirs(save_dir, exist_ok=True)  # ensures folder exists, even if deleted later


        if not filename:
            filename = f"linkedin_yas_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        # Full path inside 'data' folder
        filepath = os.path.join(save_dir, filename)
        
        df = pd.DataFrame(posts_data)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f"💾 Données sauvegardées dans: {filepath}")
        return filepath
    
    def close(self):
        """Ferme le navigateur"""
        self.driver.quit()
        print("🔒 Navigateur fermé")


# Helper to read config values flexibly
def get_secret(key, default=None):
    if key in os.environ:
        return os.environ[key]
    elif key in st.secrets:
        return st.secrets[key]
    else:
        return default        
    # # 1. Check Streamlit secrets (deployment)
    # if key in st.secrets:
    #     return st.secrets[key]
    # # 2. Fallback to OS environment variables (local dev)
    # elif key in os.environ:
    #     return os.environ[key]
    # # 3. Optional default
    # return default

def main():

    # Try to import dotenv for local environment (safe even if not installed in cloud)
    try:
        from dotenv import load_dotenv
        load_dotenv()  # loads .env if it exists
    except ImportError:
        pass

    """
    # Fonction principale
    # """
    # print("=" * 70)
    # print("🚀 LINKEDIN SCRAPER - OPÉRATEUR YAS")
    # print("=" * 70)
    # print()
    # print("⚠️  AVERTISSEMENT:")
    # print("Le scraping de LinkedIn peut violer leurs conditions d'utilisation.")
    # print("Utilisez ce script à vos propres risques.")
    # print("Il est recommandé d'utiliser l'API officielle LinkedIn.")
    # print()
    # print("=" * 70)
    # print()
    
    # Demander confirmation
    # confirmation = input("Voulez-vous continuer? (oui/non): ").lower()
    # if confirmation not in ['oui', 'yes', 'o', 'y']:
    #     print("❌ Opération annulée")
    #     return
    
    # print()
    # print("📝 Configuration du scraper...")
    # print()
    
    # Demander les identifiants
    # email = input("Email LinkedIn: ").strip()
    # Usage
    email = get_secret("LINKEDIN_EMAIL")
    password = get_secret("LINKEDIN_PASSWORD")
    # password = input("Mot de passe LinkedIn: ").strip()
    # company_name = input("Nom de l'entreprise (ex: Yas Guinée): ").strip() or "Yas"
    company_name = get_secret("COMPANY_NAME")
    
    # Options
    # max_posts = int(input("Nombre de posts à extraire (défaut: 30): ").strip() or "30")
    # headless = input("Mode sans interface graphique? (oui/non, défaut: non): ").lower() in ['oui', 'yes', 'o', 'y']
    max_posts = 30
    headless = False
    
    print(email)
    print("🚀 Démarrage du scraper...")
    print()
    
    scraper = None
    # return "ok"
    
    try:

        

        # Initialiser le scraper
        scraper = LinkedInScraper(email, password, headless=headless)
        
        # Se connecter
        if not scraper.login():
            print("❌ Impossible de se connecter. Vérifiez vos identifiants.")
            return
        
        # Naviguer vers la page de l'entreprise
        if not scraper.navigate_to_company_page(company_name):
            print("❌ Impossible de trouver la page de l'entreprise")
            return
        
        # Charger plus de posts
        scraper.scroll_to_load_posts(num_scrolls=int(max_posts / 5))
        
        # Extraire les posts
        posts_data = scraper.extract_posts(max_posts=max_posts)
        
        if posts_data:
            # Sauvegarder les données
            filename = scraper.save_to_csv(posts_data)
            
            # Afficher un résumé
            print()
            print("=" * 70)
            print("📊 RÉSUMÉ DE L'EXTRACTION")
            print("=" * 70)
            
            df = pd.DataFrame(posts_data)
            
            print(f"✅ Total de posts extraits: {len(posts_data)}")
            print(f"📅 Période: {df['date'].min()} à {df['date'].max()}")
            print()
            print("📈 Distribution des sentiments:")
            sentiment_counts = df['sentiment'].value_counts()
            for sentiment, count in sentiment_counts.items():
                pct = (count / len(df)) * 100
                print(f"   {sentiment.capitalize()}: {count} ({pct:.1f}%)")
            print()
            print("🎯 Sujets les plus mentionnés:")
            topic_counts = df['topic'].value_counts().head(5)
            for topic, count in topic_counts.items():
                print(f"   {topic}: {count} mentions")
            print()
            print(f"💾 Fichier sauvegardé: {filename}")
            print()
            print("🎉 Extraction terminée avec succès!")
            print()
            print("📌 Prochaine étape: Importez ce fichier CSV dans l'application Streamlit")
            print("   pour visualiser l'analyse complète.")
            
        else:
            print("⚠️ Aucun post n'a pu être extrait")
    
    except KeyboardInterrupt:
        print("\n⚠️ Extraction interrompue par l'utilisateur")
    
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if scraper:
            scraper.close()
        print()
        print("=" * 70)


if __name__ == "__main__":
    main()