"""
Configuration avancée pour le scraper LinkedIn
"""

import os
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ScraperConfig:
    """Configuration du scraper LinkedIn"""
    
    # Identifiants LinkedIn
    email: str = ""
    password: str = ""
    
    # Configuration de l'entreprise
    company_name: str = "Yas Guinée"
    company_url: str = ""  # URL directe si connue
    
    # Paramètres d'extraction
    max_posts: int = 30
    num_scrolls: int = 6
    
    # Délais (en secondes)
    min_delay: float = 2.0
    max_delay: float = 5.0
    scroll_delay: float = 3.0
    
    # Options du navigateur
    headless: bool = False
    window_size: str = "1920,1080"
    disable_images: bool = False  # Pour accélérer le chargement
    
    # Timeouts
    page_load_timeout: int = 30
    element_wait_timeout: int = 20
    
    # Sélecteurs CSS (peuvent changer si LinkedIn modifie son HTML)
    selectors: Dict[str, str] = None
    
    # Options de sauvegarde
    output_dir: str = "data"
    output_format: str = "csv"  # csv, json, excel
    
    # Proxy (optionnel)
    use_proxy: bool = False
    proxy_host: str = ""
    proxy_port: int = 0
    
    # Logging
    log_level: str = "INFO"  # DEBUG, INFO, WARNING, ERROR
    save_screenshots: bool = True
    screenshot_dir: str = "screenshots"
    
    def __post_init__(self):
        """Initialisation des valeurs par défaut"""
        if self.selectors is None:
            self.selectors = {
                # Sélecteurs pour la page de connexion
                'login_email': 'input#username',
                'login_password': 'input#password',
                'login_button': 'button[type="submit"]',
                
                # Sélecteurs pour la recherche
                'search_result': '.entity-result__title-text a',
                
                # Sélecteurs pour les posts
                'post_container': '.feed-shared-update-v2',
                'post_text': '.feed-shared-update-v2__description, .feed-shared-text',
                'post_date': '.feed-shared-actor__sub-description',
                'post_reactions': '.social-details-social-counts__reactions-count',
                'post_comments': '.social-details-social-counts__comments',
                
                # Boutons et actions
                'see_more_button': 'button.feed-shared-inline-show-more-text__see-more-less-toggle',
            }
        
        # Créer les dossiers si nécessaires
        os.makedirs(self.output_dir, exist_ok=True)
        if self.save_screenshots:
            os.makedirs(self.screenshot_dir, exist_ok=True)
    
    @classmethod
    def from_env(cls):
        """Charge la configuration depuis les variables d'environnement"""
        return cls(
            email=os.getenv('LINKEDIN_EMAIL', ''),
            password=os.getenv('LINKEDIN_PASSWORD', ''),
            company_name=os.getenv('COMPANY_NAME', 'Yas Guinée'),
            max_posts=int(os.getenv('MAX_POSTS', '30')),
            headless=os.getenv('HEADLESS', 'False').lower() == 'true',
        )
    
    def validate(self) -> List[str]:
        """Valide la configuration et retourne une liste d'erreurs"""
        errors = []
        
        if not self.email:
            errors.append("Email LinkedIn manquant")
        
        if not self.password:
            errors.append("Mot de passe LinkedIn manquant")
        
        if not self.company_name and not self.company_url:
            errors.append("Nom ou URL de l'entreprise manquant")
        
        if self.max_posts < 1 or self.max_posts > 100:
            errors.append("max_posts doit être entre 1 et 100")
        
        if self.use_proxy and (not self.proxy_host or self.proxy_port <= 0):
            errors.append("Configuration proxy invalide")
        
        return errors


@dataclass
class KeywordConfig:
    """Configuration des mots-clés pour classification"""
    
    topics: Dict[str, List[str]] = None
    
    def __post_init__(self):
        """Initialisation des mots-clés par défaut"""
        if self.topics is None:
            self.topics = {
                'Réseau': [
                    'réseau', '4g', '5g', '3g', 'connexion', 'signal', 'antenne',
                    'couverture réseau', 'qualité signal', 'débit', 'latence'
                ],
                'Service Client': [
                    'service', 'client', 'support', 'aide', 'assistance', 'équipe',
                    'accueil', 'conseiller', 'agence', 'réclamation', 'plainte',
                    'satisfaction', 'service après-vente', 'sav', 'hotline'
                ],
                'Prix': [
                    'prix', 'tarif', 'coût', 'facture', 'promotion', 'offre',
                    'réduction', 'abordable', 'cher', 'économique', 'gratuit',
                    'payant', 'frais', 'montant', 'budget'
                ],
                'Internet': [
                    'internet', 'data', 'débit', 'vitesse', 'téléchargement',
                    'navigation', 'web', 'wifi', 'fibre', 'adsl', 'connexion internet',
                    'bande passante', 'streaming', 'download', 'upload'
                ],
                'Couverture': [
                    'couverture', 'zone', 'rural', 'urbain', 'région', 'national',
                    'disponibilité', 'accessibilité', 'étendue', 'territoire',
                    'village', 'ville', 'quartier', 'secteur'
                ],
                'Application': [
                    'app', 'application', 'mobile', 'interface', 'smartphone',
                    'appli', 'logiciel', 'plateforme', 'ux', 'ui', 'ergonomie',
                    'bug', 'crash', 'mise à jour', 'version'
                ],
                'Offres': [
                    'forfait', 'package', 'abonnement', 'plan', 'souscription',
                    'contrat', 'engagement', 'formule', 'option', 'bundle',
                    'pack', 'catalogue'
                ]
            }
    
    def add_topic(self, topic: str, keywords: List[str]):
        """Ajoute un nouveau sujet avec ses mots-clés"""
        self.topics[topic] = keywords
    
    def add_keywords(self, topic: str, keywords: List[str]):
        """Ajoute des mots-clés à un sujet existant"""
        if topic in self.topics:
            self.topics[topic].extend(keywords)
        else:
            self.topics[topic] = keywords
    
    def get_all_keywords(self) -> List[str]:
        """Retourne tous les mots-clés"""
        all_keywords = []
        for keywords in self.topics.values():
            all_keywords.extend(keywords)
        return all_keywords


# Configurations prédéfinies

class ConfigPresets:
    """Configurations prédéfinies pour différents scénarios"""
    
    @staticmethod
    def quick_test() -> ScraperConfig:
        """Configuration pour test rapide (5 posts)"""
        return ScraperConfig(
            max_posts=5,
            num_scrolls=1,
            min_delay=1.0,
            max_delay=2.0,
            headless=True
        )
    
    @staticmethod
    def daily_monitoring() -> ScraperConfig:
        """Configuration pour monitoring quotidien (10-15 posts récents)"""
        return ScraperConfig(
            max_posts=15,
            num_scrolls=3,
            min_delay=2.0,
            max_delay=4.0,
            headless=True,
            save_screenshots=False
        )
    
    @staticmethod
    def weekly_report() -> ScraperConfig:
        """Configuration pour rapport hebdomadaire (30 posts)"""
        return ScraperConfig(
            max_posts=30,
            num_scrolls=6,
            min_delay=2.0,
            max_delay=5.0,
            headless=True,
            save_screenshots=True
        )
    
    @staticmethod
    def full_analysis() -> ScraperConfig:
        """Configuration pour analyse complète (50-100 posts)"""
        return ScraperConfig(
            max_posts=100,
            num_scrolls=20,
            min_delay=3.0,
            max_delay=6.0,
            headless=False,  # Pour surveiller le processus
            save_screenshots=True,
            disable_images=True  # Accélérer le chargement
        )
    
    @staticmethod
    def stealth_mode() -> ScraperConfig:
        """Configuration discrète avec délais plus longs"""
        return ScraperConfig(
            max_posts=20,
            num_scrolls=4,
            min_delay=5.0,
            max_delay=10.0,
            scroll_delay=5.0,
            headless=True
        )


# Exemple d'utilisation
if __name__ == "__main__":
    # Configuration basique
    config = ScraperConfig(
        email="votre.email@example.com",
        password="votre_mot_de_passe",
        company_name="Yas Guinée"
    )
    
    # Validation
    errors = config.validate()
    if errors:
        print("Erreurs de configuration:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ Configuration valide")
    
    # Utiliser un preset
    quick_config = ConfigPresets.quick_test()
    quick_config.email = "votre.email@example.com"
    quick_config.password = "votre_mot_de_passe"
    
    print(f"\n📊 Configuration Quick Test:")
    print(f"   - Posts à extraire: {quick_config.max_posts}")
    print(f"   - Mode headless: {quick_config.headless}")
    print(f"   - Délai moyen: {(quick_config.min_delay + quick_config.max_delay) / 2}s")
    
    # Configuration des mots-clés
    keywords = KeywordConfig()
    keywords.add_keywords('Service Client', ['répondeur', 'attente'])
    
    print(f"\n🔑 Sujets configurés: {list(keywords.topics.keys())}")
    print(f"   Total mots-clés: {len(keywords.get_all_keywords())}")