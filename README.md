# 🤖 LinkedIn Scraper avec Selenium - Analyse de Sentiments Yas

## 📋 Vue d'ensemble

Solution complète pour extraire et analyser les sentiments des posts LinkedIn de l'opérateur Yas. Cette solution utilise Selenium pour automatiser la collecte de données et fournit une analyse détaillée des sentiments clients.

### ⚠️ Avertissement Légal

**Le scraping de LinkedIn viole leurs conditions d'utilisation.**  
Utilisez cette solution uniquement:
- À des fins éducatives
- Dans un environnement de test
- Avec l'autorisation explicite de LinkedIn

**Nous recommandons fortement l'utilisation de l'API officielle LinkedIn pour un usage en production.**

---

## 🎯 Fonctionnalités

### ✨ Extraction Automatisée
- ✅ Connexion automatique à LinkedIn
- ✅ Navigation vers la page entreprise
- ✅ Scrolling intelligent pour charger les posts
- ✅ Extraction du texte complet des posts
- ✅ Récupération des statistiques (likes, commentaires)
- ✅ Extraction des dates de publication

### 🧠 Analyse Intelligente
- 📊 Analyse de sentiments (positif/négatif/neutre)
- 🎯 Classification automatique par sujet
- 📈 Calcul de scores de sentiment
- 💾 Export en CSV compatible Streamlit

### 🛡️ Sécurité et Discrétion
- 🎭 User-Agent personnalisé
- ⏱️ Délais aléatoires (simulation humaine)
- 🔒 Support proxy
- 📸 Capture d'écran pour débogage
- 🚫 Désactivation des indicateurs d'automatisation

---

## 📦 Structure du Projet

```
yas-linkedin-scraper/
│
├── linkedin_scraper_selenium.py  # Script principal
├── config.py                     # Configuration avancée
├── launcher.py                   # Interface de lancement
├── app.py                        # Application Streamlit
│
├── requirements_selenium.txt     # Dépendances Python
├── .env.example                  # Template variables d'environnement
├── .gitignore                    # Fichiers à ignorer
│
├── data/                         # Données extraites (CSV)
├── screenshots/                  # Captures d'écran
├── logs/                         # Fichiers de log
│
└── docs/
    ├── Guide_Utilisation_Selenium.md
    └── API_Alternative.md
```

---

## 🚀 Installation Rapide

### Prérequis

- Python 3.8+
- Google Chrome
- Compte LinkedIn actif

### Installation en 3 étapes

```bash
# 1. Cloner ou créer le dossier projet
mkdir yas-linkedin-scraper
cd yas-linkedin-scraper

# 2. Installer les dépendances
pip install -r requirements_selenium.txt

# 3. Télécharger les données TextBlob
python -m textblob.download_corpora
```

### Vérification de l'installation

```bash
python launcher.py
```

Si tout est correctement installé, vous verrez le menu principal.

---

## 💻 Utilisation

### Méthode 1: Interface Interactive (Recommandé)

```bash
python launcher.py
```

**Menu disponible:**
1. Configuration manuelle
2. Quick Test (5 posts)
3. Monitoring quotidien (15 posts)
4. Rapport hebdomadaire (30 posts)
5. Analyse complète (50-100 posts)

### Méthode 2: Script Direct

```bash
python linkedin_scraper_selenium.py
```

Le script vous demandera:
- Email LinkedIn
- Mot de passe
- Nom de l'entreprise
- Nombre de posts à extraire

### Méthode 3: Configuration Programmatique

```python
from linkedin_scraper_selenium import LinkedInScraper
from config import ScraperConfig, ConfigPresets

# Utiliser une configuration prédéfinie
config = ConfigPresets.weekly_report()
config.email = "votre.email@example.com"
config.password = "votre_mot_de_passe"

# Ou créer une configuration personnalisée
config = ScraperConfig(
    email="votre.email@example.com",
    password="votre_mot_de_passe",
    company_name="Yas Guinée",
    max_posts=30,
    headless=True
)

# Lancer le scraper
scraper = LinkedInScraper(config.email, config.password, config.headless)
scraper.login()
scraper.navigate_to_company_page(config.company_name)
scraper.scroll_to_load_posts(num_scrolls=6)
posts = scraper.extract_posts(max_posts=config.max_posts)
scraper.save_to_csv(posts)
scraper.close()
```

---

## ⚙️ Configuration

### Variables d'Environnement

Créez un fichier `.env`:

```env
# Identifiants LinkedIn
LINKEDIN_EMAIL=votre.email@example.com
LINKEDIN_PASSWORD=VotreMotDePasse123

# Configuration
COMPANY_NAME=Yas Guinée
MAX_POSTS=30
HEADLESS=False

# Proxy (optionnel)
USE_PROXY=False
PROXY_HOST=
PROXY_PORT=
```

### Configurations Prédéfinies

```python
from config import ConfigPresets

# Test rapide (5 posts, 1 minute)
config = ConfigPresets.quick_test()

# Monitoring quotidien (15 posts, 3 minutes)
config = ConfigPresets.daily_monitoring()

# Rapport hebdomadaire (30 posts, 5-7 minutes)
config = ConfigPresets.weekly_report()

# Analyse complète (100 posts, 15-20 minutes)
config = ConfigPresets.full_analysis()

# Mode furtif (délais longs)
config = ConfigPresets.stealth_mode()
```

---

## 📊 Format des Données Extraites

### Fichier CSV Généré

```csv
date,topic,comment,sentiment,score,reactions,comments,engagement
2024-11-10,Réseau,"Excellent réseau 5G!",positif,0.85,245,12,257
2024-11-09,Prix,"Tarifs trop élevés",négatif,-0.65,89,34,123
2024-11-08,Service Client,"Équipe réactive",positif,0.72,156,8,164
```

### Colonnes

| Colonne | Description | Type |
|---------|-------------|------|
| `date` | Date de publication | YYYY-MM-DD |
| `topic` | Sujet classifié | String |
| `comment` | Texte du post | String |
| `sentiment` | Sentiment détecté | positif/négatif/neutre |
| `score` | Score de polarité | Float (-1 à 1) |
| `reactions` | Nombre de likes | Integer |
| `comments` | Nombre de commentaires | Integer |
| `engagement` | Total interactions | Integer |

---

## 🎯 Classification des Sujets

### Sujets Détectés Automatiquement

| Sujet | Mots-Clés |
|-------|-----------|
| **Réseau** | réseau, 4G, 5G, connexion, signal, antenne |
| **Service Client** | service, client, support, aide, assistance |
| **Prix** | prix, tarif, coût, facture, promotion |
| **Internet** | internet, data, débit, vitesse, navigation |
| **Couverture** | couverture, zone, rural, urbain, région |
| **Application** | app, application, mobile, interface |
| **Offres** | forfait, package, abonnement, plan |

### Personnalisation

Modifiez `config.py` pour ajouter vos propres sujets:

```python
from config import KeywordConfig

keywords = KeywordConfig()
keywords.add_topic('5G', ['5g', 'cinquième génération', '5ème'])
keywords.add_keywords('Service Client', ['répondeur', 'attente'])
```

---

## 📈 Intégration avec Streamlit

### Étape 1: Extraire les données

```bash
python linkedin_scraper_selenium.py
# Fichier généré: linkedin_yas_posts_20241110_143022.csv
```

### Étape 2: Lancer Streamlit

```bash
streamlit run app.py
```

### Étape 3: Importer les données

1. Dans la sidebar, sélectionner "Importer un fichier CSV"
2. Choisir le fichier CSV généré
3. Visualiser l'analyse complète

### Résultats dans Streamlit

- 📊 Distribution des sentiments (graphique camembert)
- 📈 Évolution temporelle
- 🎯 Analyse par sujet
- 💡 Recommandations automatiques
- 📥 Export rapport PDF/CSV

---

## 🛠️ Résolution de Problèmes

### Problème: "ChromeDriver not found"

**Solution:**
```bash
pip install --upgrade webdriver-manager
```

### Problème: "Login failed"

**Causes:**
- Identifiants incorrects
- 2FA activé sur le compte
- LinkedIn a détecté une activité suspecte

**Solutions:**
1. Vérifier email/mot de passe
2. Désactiver temporairement 2FA
3. Se connecter manuellement d'abord
4. Utiliser mode non-headless pour voir l'erreur

### Problème: "No posts found"

**Solutions:**
1. Vérifier le nom exact de l'entreprise
2. Augmenter `num_scrolls` dans la config
3. Vérifier manuellement que la page existe
4. Attendre quelques heures (rate limiting)

### Problème: "TimeoutException"

**Solution:**
```python
config.element_wait_timeout = 30  # Augmenter à 30s
config.page_load_timeout = 60     # Augmenter à 60s
```

### Problème: Compte Restreint

**Si LinkedIn détecte le scraping:**
- ⏸️ Arrêter immédiatement
- ⏳ Attendre 24-48h
- 📧 Contacter support LinkedIn si nécessaire
- ✅ Passer à l'API officielle

---

## 📊 Performances et Limites

### Vitesse d'Extraction

| Configuration | Posts | Durée | Posts/min |
|---------------|-------|-------|-----------|
| Quick Test | 5 | 1 min | 5 |
| Daily | 15 | 3-4 min | 4 |
| Weekly | 30 | 6-8 min | 4 |
| Full | 100 | 20-30 min | 3-5 |

### Limites Recommandées

- ⏱️ **Fréquence**: Maximum 1 extraction/heure
- 📊 **Volume**: Maximum 100 posts/extraction
- 📅 **Quotidien**: Maximum 3 extractions/jour
- 🚫 **Ne pas**: Lancer 24/7

### Optimisations

```python
# Accélérer l'extraction
config.disable_images = True       # Ne pas charger les images
config.headless = True             # Mode sans interface
config.min_delay = 1.0            # Réduire les délais (risqué)
```

---

## 🔒 Sécurité

### Bonnes Pratiques

#### 1. Protection des Identifiants

❌ **À NE PAS FAIRE:**
```python
email = "mon.email@gmail.com"  # Codé en dur
```

✅ **À FAIRE:**
```python
from dotenv import load_dotenv
import os

load_dotenv()
email = os.getenv('LINKEDIN_EMAIL')
```

#### 2. Fichier .gitignore

```
.env
*.csv
data/
screenshots/
logs/
venv/
__pycache__/
```

#### 3. Utilisation de Proxy

```python
config = ScraperConfig()
config.use_proxy = True
config.proxy_host = "proxy.example.com"
config.proxy_port = 8080
```

---

## 🆘 Support

### Documentation

- 📚 Guide complet: `docs/Guide_Utilisation_Selenium.md`
- 🔌 API Alternative: `docs/API_Alternative.md`
- ⚙️ Configuration: `config.py`

### Communautés

- **Stack Overflow**: Tag `selenium` + `linkedin`
- **Reddit**: r/selenium, r/webscraping
- **GitHub**: Issues du projet

### Contact

Pour toute question:
1. Consultez d'abord la documentation
2. Vérifiez les issues GitHub
3. Contactez votre administrateur système

---

## ⚖️ Alternatives Légales

### 1. API Officielle LinkedIn (RECOMMANDÉ)

**Avantages:**
- ✅ 100% légal
- ✅ Stable et fiable
- ✅ Support officiel
- ✅ Pas de risque de ban

**Ressources:**
- https://www.linkedin.com/developers/
- https://docs.microsoft.com/en-us/linkedin/

### 2. Export Manuel

**Processus:**
1. LinkedIn Analytics
2. Exporter en CSV
3. Importer dans Streamlit

### 3. Services Tiers Autorisés

- **Zapier**: Automatisation légale
- **Phantombuster**: Service de scraping autorisé
- **Apify**: Plateforme d'extraction

---

## 📝 Changelog

### Version 1.0.0 (2024-11-10)

**Fonctionnalités initiales:**
- Extraction automatisée des posts LinkedIn
- Analyse de sentiments avec TextBlob
- Classification par sujet
- Export CSV
- Interface de lancement
- Configuration avancée
- Documentation complète

**À venir:**
- Support multi-entreprises
- Analyse des commentaires
- Dashboard temps réel
- API REST
- Notifications par email

---

## 📄 Licence

Ce projet est fourni à des fins **ÉDUCATIVES UNIQUEMENT**.

⚠️ **Disclaimer:**
- L'utilisation de ce code pour violer les CGU de LinkedIn est de votre responsabilité
- Les auteurs ne sont pas responsables des conséquences
- Utilisez à vos propres risques

**Recommandation:** Utilisez l'API officielle LinkedIn pour un usage en production.

---

## 🙏 Remerciements

- **Selenium**: Framework d'automatisation
- **TextBlob**: Analyse de sentiments
- **LinkedIn**: Plateforme sociale professionnelle
- **Streamlit**: Framework de visualisation

---

## ✅ Checklist de Déploiement

- [ ] Python 3.8+ installé
- [ ] Chrome installé
- [ ] Dépendances installées (`pip install -r requirements_selenium.txt`)
- [ ] TextBlob corpus téléchargé
- [ ] Fichier `.env` configuré
- [ ] Identifiants LinkedIn testés
- [ ] Premier test réussi (Quick Test)
- [ ] Documentation lue
- [ ] Streamlit fonctionnel

---

**🎉 Vous êtes prêt à utiliser le scraper LinkedIn avec Selenium !**

Pour démarrer: `python launcher.py`