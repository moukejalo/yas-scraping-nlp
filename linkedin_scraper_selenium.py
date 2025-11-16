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
from bs4 import BeautifulSoup
import re



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

        # chrome_options.add_argument("--headless=new")        # Required for server
        # chrome_options.add_argument("--no-sandbox")          # Required for EC2
        chrome_options.add_argument("--disable-dev-shm-usage") # Fixes shared memory issue
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")

        # Add these to your Chrome options
        chrome_options.add_argument('--memory-pressure-off')
        chrome_options.add_argument('--max_old_space_size=4096')  # Increase memory limit

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
        all_mcomments = []
        comments_data = []
        
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
                        # comment_texte = self.extract_comments_from_post(post, self.driver)
                        # print(comment_texte)

                    except (NoSuchElementException, ValueError):
                        comments_count = 0
                    
                    # Analyser le sentiment
                    # sentiment, score = self.analyze_sentiment(post_text)
                    topic = self.classify_topic(post_text)

                    # Extraire les commentaires du post
                    print(f"   📝 Extraction des commentaires du post {idx+1}...")
                    post_comments = self.extract_comments_from_post(post)
                    print("comments of a post : ", post_comments)

                    score_total = 0
                    for comment in post_comments:

                        sentiment, score = self.pipeline_nlp(post_text)
                        comment_row = {
                            'date': post_date,
                            'comment': comment,
                            'sentiment': sentiment,
                            'score': score,
                            'topic': topic,
                            'post_id': idx,
                            'post_text': post_text[:20],
                        }
                        score_total += score
                        comments_data.append(comment_row)

                    post_score = score_total / len(post_comments)
                    post_sentiment = self.classifier_sentiment(post_score)
                    
                    post_data = {
                        'date': post_date,
                        'topic': topic,
                        'sentiment': post_sentiment,
                        'score': post_score,
                        'reactions': reactions_count,
                        'comments': len(post_comments),
                        'engagement': reactions_count + comments_count
                    }

                    all_mcomments.append(post_comments)
                    # print(new_posts)
                    
                    posts_data.append(post_data)
                    print(f"   ✅ Post {idx+1}/{min(len(posts), max_posts)} extrait - {topic} ({sentiment})")
                    
                except Exception as e:
                    print(f"   ⚠️ Erreur extraction post {idx+1}: {e}")
                    continue
            
            print(f"✅ {len(posts_data)} posts extraits avec succès!")
            print("all_mcomments")
            # print(all_mcomments)

            print("posts_data :", posts_data)
            print("comments_data :", comments_data)
            # return posts_data
            return posts_data, comments_data
            
        except Exception as e:
            print(f"❌ Erreur lors de l'extraction: {e}")
            return posts_data, comments_data
    
    def extract_comments_from_post1(self, post_element, driver):
        """Cliquer sur le bouton commentaire et récupérer les commentaires"""
        comments = []
        
        try:
            # Trouver le bouton de commentaires
            comment_button_selectors = [
                "button[aria-label*='comment']",
                "//button[contains(., 'comment')]",
                ".social-details-social-counts__comments-button"
            ]
            
            comment_button = None
            for selector in comment_button_selectors:
                try:
                    if selector.startswith("//"):
                        comment_button = post_element.find_element(By.XPATH, selector)
                    else:
                        comment_button = post_element.find_element(By.CSS_SELECTOR, selector)
                    
                    if comment_button.is_displayed():
                        print(f"✅ Bouton trouvé avec: {selector}")
                        break
                    else:
                        comment_button = None
                except Exception:
                    continue
            
            if comment_button:
                # Scroll et clic
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", comment_button)
                time.sleep(2)
                
                button_text = comment_button.text.strip()
                print(f"📝 Bouton texte: '{button_text}'")
                
                # Clic JavaScript
                driver.execute_script("arguments[0].click();", comment_button)
                print("🖱️ Clic JavaScript réussi")
                
                # Attendre que la modale des commentaires s'ouvre
                print("🔄 Attente du chargement des commentaires...")
                time.sleep(5)
                
                # MAIN CORRECTION: Attendre spécifiquement la modale des commentaires
                wait = WebDriverWait(driver, 10)
                
                # Essayer de trouver la modale des commentaires
                modal_selectors = [
                    ".comments-overlay",
                    ".scaffold-finite-scroll__content", 
                    ".comments-comments-list__container",
                    ".artdeco-modal__content"
                ]
                
                modal_element = None
                for selector in modal_selectors:
                    try:
                        modal_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                        print(f"✅ Modale trouvée avec: {selector}")
                        break
                    except:
                        continue
                
                if modal_element:
                    # Scroll dans la modale pour charger tous les commentaires
                    print("📜 Défilement dans la modale...")
                    for i in range(3):
                        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal_element)
                        time.sleep(2)
                    
                    # Attendre un peu plus pour le chargement
                    time.sleep(3)
                    
                    # MAIN FIX: Rechercher les commentaires dans toute la page une fois la modale ouverte
                    comment_selectors = [
                        "span.coments-comment-item_main-content",  # Votre sélecteur exact
                        ".comments-comment-item",
                        ".feed-shared-comment__content",
                        ".comment__content",
                        "[data-test-id='comment']",
                        ".update-components-text"  # Le contenu texte des commentaires
                    ]
                    
                    all_comments_found = []
                    for selector in comment_selectors:
                        try:
                            comment_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                            if comment_elements:
                                print(f"✅ {len(comment_elements)} éléments trouvés avec: {selector}")
                                
                                for comment_element in comment_elements:
                                    try:
                                        text = comment_element.text.strip()
                                        if text and len(text) < 100:  # Filtrer les textes courts
                                            # Éviter les doublons
                                            if text not in all_comments_found:
                                                all_comments_found.append(text)
                                                print(f"💬 Commentaire: {text[:80]}...")
                                    except Exception as e:
                                        continue
                        except Exception:
                            continue
                    
                    comments = all_comments_found
                    
                    # Alternative avec BeautifulSoup sur le HTML de la modale
                    # if not comments:
                    #     print("🔄 Essai avec BeautifulSoup sur le HTML complet...")
                    #     soup = BeautifulSoup(driver.page_source, "html.parser")
                        
                    #     # Essayer plusieurs sélecteurs
                    #     comment_texts = []
                        
                    #     # Sélecteur exact de votre HTML
                    #     comment_spans = soup.find_all("span", class_="coments-comment-item_main-content")
                    #     for span in comment_spans:
                    #         text = span.get_text(separator=" ", strip=True)
                    #         if text and len(text) > 10:
                    #             comment_texts.append(text)
                        
                    #     # Autres sélecteurs possibles
                    #     if not comment_texts:
                    #         comment_divs = soup.find_all("div", class_="update-components-text")
                    #         for div in comment_divs:
                    #             text = div.get_text(separator=" ", strip=True)
                    #             if text and len(text) > 10:
                    #                 comment_texts.append(text)
                        
                    #     # Filtrer les doublons
                    #     comments = list(dict.fromkeys(comment_texts))
                        
                    #     for comment in comments:
                    #         print(f"💬 Commentaire BS: {comment[:80]}...")
                
                else:
                    print("❌ Modale des commentaires non trouvée")
                    
                # Fermer la modale
                self.close_modal(driver)
                
            else:
                print("❌ Aucun bouton de commentaires trouvé dans ce post")
                
        except Exception as e:
            print(f"❌ Erreur générale: {e}")
            import traceback
            traceback.print_exc()
            # Essayer de fermer la modale en cas d'erreur
            try:
                self.close_modal(driver)
            except:
                pass
        
        return comments
    
    def extract_comments_from_post(self, post_element):
        comments_data = []
        
        try:
            # Chercher le bouton "Commentaire" dans la barre d'actions
            try:
                # Essayer plusieurs sélecteurs pour le bouton commentaire
                comment_button_selectors = [
                    "button.comment-button",
                    "button[aria-label*='omment']",
                    ".feed-shared-social-action-bar__action-button--comment",
                    "button.social-actions-button--comment"
                ]
                
                comments_button = None
                for selector in comment_button_selectors:
                    try:
                        comments_button = post_element.find_element(By.CSS_SELECTOR, selector)
                        break
                    except NoSuchElementException:
                        continue
                
                if not comments_button:
                    print("      Pas de bouton commentaires trouvé")
                    return comments_data
                
                # Scroll et clic avec JavaScript pour éviter l'interception
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", comments_button)
                self.random_delay(0.5, 1)
                
                # Utiliser JavaScript pour cliquer (évite les interceptions)
                self.driver.execute_script("arguments[0].click();", comments_button)
                self.random_delay(1.5, 2.5)
                
            except Exception as e:
                print(f"      Erreur lors du clic sur commentaires: {e}")
                return comments_data
            
            # Cliquer sur "Afficher plus de commentaires" si disponible
            max_attempts = 5
            for attempt in range(max_attempts):
                try:
                    show_more_selectors = [
                        "button.comments-comments-list__show-more-button",
                        "button[aria-label*='more comment']",
                        ".artdeco-button--tertiary.comments-comments-list__show-more-button"
                    ]
                    
                    show_more = None
                    for selector in show_more_selectors:
                        try:
                            show_more = self.driver.find_element(By.CSS_SELECTOR, selector)
                            if show_more and show_more.is_displayed():
                                break
                        except NoSuchElementException:
                            continue
                    
                    if show_more and show_more.is_displayed():
                        # Clic avec JavaScript
                        self.driver.execute_script("arguments[0].click();", show_more)
                        self.random_delay(1, 1.5)
                    else:
                        break
                        
                except Exception as e:
                    print(f"      Fin du chargement des commentaires")
                    break
            
            # Extraire tous les commentaires
            self.random_delay(1, 1.5)
            
            # Chercher les commentaires avec plusieurs sélecteurs possibles
            comment_selectors = [
                ".comments-comment-item",
                "article.comments-comment-item",
                ".comments-comment-entity"
            ]
            
            comment_elements = []
            for selector in comment_selectors:
                try:
                    comment_elements = post_element.find_elements(By.CSS_SELECTOR, selector)
                    if comment_elements:
                        break
                except NoSuchElementException:
                    continue
            
            print(f"      {len(comment_elements)} commentaires trouvés")
            
            for idx, comment_elem in enumerate(comment_elements):
                try:
                    # # Nom de l'auteur du commentaire
                    # try:
                    #     author = comment_elem.find_element(By.CSS_SELECTOR, 
                    #         ".comments-post-meta__name-text, .comments-comment-meta__name").text.strip()
                    # except NoSuchElementException:
                    #     author = "Anonyme"
                    
                    # # Titre/Position de l'auteur
                    # try:
                    #     author_title = comment_elem.find_element(By.CSS_SELECTOR, 
                    #         ".comments-comment-meta__headline, .comments-post-meta__headline").text.strip()
                    # except NoSuchElementException:
                    #     author_title = ""
                    
                    # Texte du commentaire
                    try:
                        comment_text = comment_elem.find_element(By.CSS_SELECTOR, 
                            ".comments-comment-item__main-content, .comments-comment-item-content-body__text").text.strip()
                    except NoSuchElementException:
                        comment_text = ""
                    
                    # # Date du commentaire
                    # try:
                    #     comment_date = comment_elem.find_element(By.CSS_SELECTOR, 
                    #         ".comments-comment-meta__timestamp, .feed-shared-actor__sub-description").text.strip()
                    #     parsed_date = self.parse_linkedin_date(comment_date)
                    # except NoSuchElementException:
                    #     parsed_date = datetime.now().strftime('%Y-%m-%d')
                    
                    # # Nombre de réactions sur le commentaire
                    # try:
                    #     reactions_elem = comment_elem.find_element(By.CSS_SELECTOR, 
                    #         ".comments-comment-social-bar__reactions-count")
                    #     reactions = int(''.join(filter(str.isdigit, reactions_elem.text)))
                    # except (NoSuchElementException, ValueError):
                    #     reactions = 0
                    
                    # Analyser le sentiment du commentaire
                    # sentiment, score = self.analyze_sentiment(comment_text)
                    
                    # comment_data = {
                    #     'author': author,
                    #     'author_title': author_title,
                    #     'comment_text': comment_text,
                    #     'date': parsed_date,
                    #     'reactions': reactions,
                    #     'sentiment': sentiment,
                    #     'sentiment_score': score
                    # }

                    # comment_data = {
                    #     # 'post_id': post_element.get_attribute('id'),
                    #     'comment_text': comment_text,
                    #     'date': parsed_date,
                    # }


                    
                    # comments_data.append(comment_data)
                    comments_data.append(comment_text)
                    
                except Exception as e:
                    print(f"      ⚠️ Erreur extraction commentaire {idx+1}: {e}")
                    continue
            
            return comments_data
            
        except Exception as e:
            print(f"      ❌ Erreur lors de l'extraction des commentaires: {e}")
            return comments_data

    def close_modal(sell, driver):
        """Fermer la modale des commentaires"""
        try:
            # Méthode 1: Bouton de fermeture explicite
            close_selectors = [
                "button[aria-label='Fermer']",
                "button[aria-label='Close']",
                ".artdeco-modal__dismiss",
                "button.artdeco-button--circle",
                "button[data-test-modal-close-btn]"
            ]
            
            for selector in close_selectors:
                try:
                    close_btn = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    driver.execute_script("arguments[0].click();", close_btn)
                    print("✅ Modale fermée avec bouton")
                    time.sleep(2)
                    return
                except:
                    continue
            
            # Méthode 2: Cliquer sur l'overlay/backdrop
            try:
                overlay = driver.find_element(By.CSS_SELECTOR, ".artdeco-modal-overlay")
                driver.execute_script("arguments[0].click();", overlay)
                print("✅ Modale fermée via overlay")
                time.sleep(2)
                return
            except:
                pass
                
            # Méthode 3: Échap
            from selenium.webdriver.common.keys import Keys
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.ESCAPE)
            print("✅ Modale fermée avec Échap")
            time.sleep(2)
            
        except Exception as e:
            print(f"⚠️ Erreur lors de la fermeture: {e}")

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
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            return polarity

        except:
            return 'neutre', 0.0
    
    def pipeline_nlp(self, text):
        # pretaitement
        text = self.nettoyer_texte(text)

        # Analyse de sentiment
        polarite = self.analyze_sentiment(text)

        # Classification de sentiment
        sentiment = self.classifier_sentiment(polarite)

        # Retourner le sentiment et la polarité
        return sentiment, polarite
        
    def nettoyer_texte(self,texte):
        """Fonction de nettoyage du texte"""
        # Convertir en minuscules
        texte = texte.lower()
        # Retirer les URLs
        texte = re.sub(r'http\S+|www\S+|https\S+', '', texte)
        # Retirer les mentions (@username)
        texte = re.sub(r'@\w+', '', texte)
        # Retirer les hashtags
        texte = re.sub(r'#\w+', '', texte)
        # Retirer les caractères spéciaux excessifs
        texte = re.sub(r'[^\w\s!?.,]', '', texte)
        # Supprimer les espaces multiples
        texte = re.sub(r'\s+', ' ', texte).strip()
        return texte
    
    def classifier_sentiment(self, polarite):
        """Classifie le sentiment basé sur la polarité"""
        if polarite > 0.1:
            return 'positif'
        elif polarite < -0.1:
            return 'négatif'
        else:
            return 'neutre'
    

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
        save_dir = "prod-data"
        os.makedirs(save_dir, exist_ok=True)  # ensures folder exists, even if deleted later


        # if not filename:
        filename = f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

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
    # Usage
    email = get_secret("LINKEDIN_EMAIL")
    password = get_secret("LINKEDIN_PASSWORD")
    company_name = get_secret("COMPANY_NAME")
    max_posts = int(get_secret("MAX_POSTS", 30))
    
    # max_posts = 5
    headless = False
    
    print(email)
    print("🚀 Démarrage du scraper...")
    print()
    
    scraper = None
    
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
        posts_data, comments_data = scraper.extract_posts(max_posts=max_posts)
        
        if posts_data:
            # Sauvegarder les données
            filename = scraper.save_to_csv(posts_data, "linkedin_yas_posts")
            time.sleep(2 )
            filename2 = scraper.save_to_csv(comments_data, "linkedin_yas_comments")
            
            # Afficher un résumé
            print()
            print("=" * 70)
            print("📊 RÉSUMÉ DE L'EXTRACTION")
            print("=" * 70)
            
            df_posts_data = pd.DataFrame(posts_data)
            df_comments_data = pd.DataFrame(comments_data)
            
            print(f"✅ Total de posts extraits: {len(posts_data)}")
            print(f"📅 Période: {df_posts_data['date'].min()} à {df_posts_data['date'].max()}")
            print()
            print("📈 Distribution des sentiments:")
            sentiment_counts = df_posts_data['sentiment'].value_counts()
            for sentiment, count in sentiment_counts.items():
                pct = (count / len(df_posts_data)) * 100
                print(f"   {sentiment.capitalize()}: {count} ({pct:.1f}%)")
            print()
            print("🎯 Sujets les plus mentionnés:")
            topic_counts = df_posts_data['topic'].value_counts().head(5)
            for topic, count in topic_counts.items():
                print(f"   {topic}: {count} mentions")
            print()
            print(f"💾 Fichier sauvegardé: {filename}")
            print()
            print("🎉 Extraction terminée avec succès!")
            print()
            print("📌 Prochaine étape: Importez ce fichier CSV dans l'application Streamlit")
            print("   pour visualiser l'analyse complète.")

            return df_posts_data, df_comments_data
            
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