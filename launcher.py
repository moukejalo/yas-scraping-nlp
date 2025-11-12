#!/usr/bin/env python3
"""
Script de lancement simplifié pour le scraper LinkedIn
"""

import sys
import os
from pathlib import Path

# Couleurs pour le terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header():
    """Affiche le header de l'application"""
    print(f"{Colors.CYAN}")
    print("=" * 70)
    print("   _____ _____  _____        _____  _____ _____  ")
    print("  / ____|  __ \\|  __ \\  /\\  |  __ \\|  __ \\___  \\ ")
    print(" | (___ | |  | | |__) |/  \\ | |__) | |__) | / /  ")
    print("  \\___ \\| |  | |  _  // /\\ \\|  ___/|  ___/ / /   ")
    print("  ____) | |__| | | \\ / ____ \\ |    | |    / /    ")
    print(" |_____/|_____/|_|  \\_/_/   \\_\\_|    |_|   /_/     ")
    print()
    print("        LinkedIn Scraper - Analyse Sentiments Yas")
    print("=" * 70)
    print(f"{Colors.ENDC}")
    print()

def print_warning():
    """Affiche l'avertissement légal"""
    print(f"{Colors.WARNING}{Colors.BOLD}")
    print("⚠️  AVERTISSEMENT IMPORTANT ⚠️")
    print(f"{Colors.ENDC}{Colors.WARNING}")
    print()
    print("Le scraping de LinkedIn peut violer leurs conditions d'utilisation.")
    print("Votre compte LinkedIn pourrait être:")
    print("  • Temporairement suspendu")
    print("  • Définitivement banni")
    print("  • Soumis à des restrictions")
    print()
    print("Ce script est fourni à des fins ÉDUCATIVES uniquement.")
    print(f"{Colors.ENDC}")
    print()
    print(f"{Colors.GREEN}Alternatives recommandées:{Colors.ENDC}")
    print("  1. API officielle LinkedIn (légal, stable, supporté)")
    print("  2. Export manuel des données (100% sûr)")
    print("  3. Services tiers autorisés (Zapier, Phantombuster)")
    print()

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    print(f"{Colors.BLUE}🔍 Vérification des dépendances...{Colors.ENDC}")
    
    required_packages = {
        'selenium': 'selenium',
        'pandas': 'pandas',
        'textblob': 'textblob',
    }
    
    missing = []
    
    for package, import_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing.append(package)
    
    if missing:
        print()
        print(f"{Colors.FAIL}❌ Packages manquants: {', '.join(missing)}{Colors.ENDC}")
        print()
        print(f"{Colors.CYAN}Installation:{Colors.ENDC}")
        print(f"  pip install {' '.join(missing)}")
        return False
    
    print()
    print(f"{Colors.GREEN}✅ Toutes les dépendances sont installées{Colors.ENDC}")
    return True

def get_user_input(prompt, default=None):
    """Demande une entrée utilisateur avec valeur par défaut"""
    if default:
        prompt = f"{prompt} [{default}]"
    
    value = input(f"  {prompt}: ").strip()
    return value if value else default

def show_menu():
    """Affiche le menu principal"""
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                    MENU PRINCIPAL                          ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")
    print()
    print("  1. 🚀 Lancer le scraper (Configuration manuelle)")
    print("  2. ⚡ Quick Test (5 posts)")
    print("  3. 📊 Monitoring Quotidien (15 posts)")
    print("  4. 📈 Rapport Hebdomadaire (30 posts)")
    print("  5. 🔬 Analyse Complète (50-100 posts)")
    print("  6. ⚙️  Configuration Avancée")
    print("  7. 📚 Documentation et Aide")
    print("  8. ❌ Quitter")
    print()

def run_scraper(config_type='manual'):
    """Lance le scraper avec la configuration choisie"""
    try:
        # Import dynamique pour éviter les erreurs si pas installé
        from linkedin_scraper_selenium import LinkedInScraper
        from config import ScraperConfig, ConfigPresets
        
        print()
        print(f"{Colors.CYAN}📝 Configuration du scraper...{Colors.ENDC}")
        print()
        
        # Choisir la configuration
        if config_type == 'manual':
            email = get_user_input("Email LinkedIn")
            password = get_user_input("Mot de passe", "********")
            company = get_user_input("Nom de l'entreprise", "Yas Guinée")
            max_posts = int(get_user_input("Nombre de posts", "30"))
            headless = get_user_input("Mode sans interface (oui/non)", "non").lower() in ['oui', 'yes', 'o', 'y']
            
            config = ScraperConfig(
                email=email,
                password=password,
                company_name=company,
                max_posts=max_posts,
                headless=headless
            )
        
        elif config_type == 'quick':
            config = ConfigPresets.quick_test()
            config.email = get_user_input("Email LinkedIn")
            config.password = get_user_input("Mot de passe")
            config.company_name = get_user_input("Nom de l'entreprise", "Yas Guinée")
        
        elif config_type == 'daily':
            config = ConfigPresets.daily_monitoring()
            config.email = get_user_input("Email LinkedIn")
            config.password = get_user_input("Mot de passe")
            config.company_name = get_user_input("Nom de l'entreprise", "Yas Guinée")
        
        elif config_type == 'weekly':
            config = ConfigPresets.weekly_report()
            config.email = get_user_input("Email LinkedIn")
            config.password = get_user_input("Mot de passe")
            config.company_name = get_user_input("Nom de l'entreprise", "Yas Guinée")
        
        elif config_type == 'full':
            config = ConfigPresets.full_analysis()
            config.email = get_user_input("Email LinkedIn")
            config.password = get_user_input("Mot de passe")
            config.company_name = get_user_input("Nom de l'entreprise", "Yas Guinée")
        
        # Valider la configuration
        errors = config.validate()
        if errors:
            print()
            print(f"{Colors.FAIL}❌ Erreurs de configuration:{Colors.ENDC}")
            for error in errors:
                print(f"  • {error}")
            return
        
        print()
        print(f"{Colors.GREEN}✅ Configuration validée{Colors.ENDC}")
        print()
        print(f"{Colors.BLUE}📋 Résumé:{Colors.ENDC}")
        print(f"  • Entreprise: {config.company_name}")
        print(f"  • Posts à extraire: {config.max_posts}")
        print(f"  • Mode headless: {'Oui' if config.headless else 'Non'}")
        print()
        
        # Confirmation finale
        confirm = input(f"{Colors.WARNING}Voulez-vous continuer? (oui/non): {Colors.ENDC}").lower()
        if confirm not in ['oui', 'yes', 'o', 'y']:
            print(f"{Colors.WARNING}❌ Opération annulée{Colors.ENDC}")
            return
        
        print()
        print(f"{Colors.GREEN}🚀 Démarrage du scraper...{Colors.ENDC}")
        print("=" * 70)
        print()
        
        # Initialiser et lancer le scraper
        scraper = LinkedInScraper(
            email=config.email,
            password=config.password,
            headless=config.headless
        )
        
        # Connexion
        if not scraper.login():
            print(f"{Colors.FAIL}❌ Échec de la connexion{Colors.ENDC}")
            return
        
        # Navigation
        if not scraper.navigate_to_company_page(config.company_name):
            print(f"{Colors.FAIL}❌ Impossible de trouver l'entreprise{Colors.ENDC}")
            scraper.close()
            return
        
        # Chargement des posts
        scraper.scroll_to_load_posts(num_scrolls=config.num_scrolls)
        
        # Extraction
        posts = scraper.extract_posts(max_posts=config.max_posts)
        
        if posts:
            # Sauvegarde
            filename = scraper.save_to_csv(posts)
            
            # Afficher le résumé
            print()
            print("=" * 70)
            print(f"{Colors.GREEN}{Colors.BOLD}✅ EXTRACTION RÉUSSIE{Colors.ENDC}")
            print("=" * 70)
            print()
            print(f"📊 {len(posts)} posts extraits")
            print(f"💾 Fichier sauvegardé: {filename}")
            print()
            print(f"{Colors.CYAN}📌 Prochaine étape:{Colors.ENDC}")
            print(f"  Importez {filename} dans l'application Streamlit pour")
            print(f"  visualiser l'analyse complète des sentiments.")
            print()
            print(f"{Colors.BLUE}Commande:{Colors.ENDC}")
            print(f"  streamlit run app.py")
        else:
            print(f"{Colors.FAIL}❌ Aucun post extrait{Colors.ENDC}")
        
        # Fermer le navigateur
        scraper.close()
        
    except KeyboardInterrupt:
        print()
        print(f"{Colors.WARNING}⚠️  Opération interrompue par l'utilisateur{Colors.ENDC}")
    
    except Exception as e:
        print()
        print(f"{Colors.FAIL}❌ Erreur: {e}{Colors.ENDC}")
        import traceback
        print()
        print("Détails de l'erreur:")
        traceback.print_exc()

def show_documentation():
    """Affiche la documentation"""
    print()
    print(f"{Colors.CYAN}{Colors.BOLD}📚 DOCUMENTATION{Colors.ENDC}")
    print("=" * 70)
    print()
    print("📖 Fichiers de documentation disponibles:")
    print("  • Guide_Utilisation_Selenium.md - Guide complet")
    print("  • README.md - Vue d'ensemble")
    print("  • config.py - Options de configuration")
    print()
    print("🌐 Ressources en ligne:")
    print("  • Selenium: https://selenium-python.readthedocs.io/")
    print("  • LinkedIn API: https://docs.microsoft.com/en-us/linkedin/")
    print("  • TextBlob: https://textblob.readthedocs.io/")
    print()
    print("❓ Besoin d'aide?")
    print("  • Consultez les fichiers de documentation")
    print("  • Vérifiez les issues sur GitHub")
    print("  • Contactez votre administrateur système")
    print()

def main():
    """Fonction principale"""
    # Afficher le header
    print_header()
    
    # Vérifier les dépendances
    if not check_dependencies():
        print()
        input("Appuyez sur Entrée pour quitter...")
        sys.exit(1)
    
    print()
    
    # Afficher l'avertissement
    print_warning()
    
    # Boucle principale
    while True:
        show_menu()
        
        choice = input(f"{Colors.BOLD}Votre choix (1-8): {Colors.ENDC}").strip()
        
        if choice == '1':
            run_scraper('manual')
        
        elif choice == '2':
            print()
            print(f"{Colors.CYAN}⚡ Quick Test - Configuration:{Colors.ENDC}")
            print("  • 5 posts")
            print("  • Mode headless")
            print("  • Rapide (délais courts)")
            run_scraper('quick')
        
        elif choice == '3':
            print()
            print(f"{Colors.CYAN}📊 Monitoring Quotidien - Configuration:{Colors.ENDC}")
            print("  • 15 posts récents")
            print("  • Mode headless")
            print("  • Optimal pour suivi quotidien")
            run_scraper('daily')
        
        elif choice == '4':
            print()
            print(f"{Colors.CYAN}📈 Rapport Hebdomadaire - Configuration:{Colors.ENDC}")
            print("  • 30 posts")
            print("  • Capture d'écran activée")
            print("  • Analyse complète")
            run_scraper('weekly')
        
        elif choice == '5':
            print()
            print(f"{Colors.CYAN}🔬 Analyse Complète - Configuration:{Colors.ENDC}")
            print("  • 50-100 posts")
            print("  • Mode visible (surveillance)")
            print("  • Analyse approfondie")
            print()
            print(f"{Colors.WARNING}⚠️  Cette opération peut prendre 15-30 minutes{Colors.ENDC}")
            run_scraper('full')
        
        elif choice == '6':
            print()
            print(f"{Colors.CYAN}⚙️  Configuration Avancée{Colors.ENDC}")
            print()
            print("Pour une configuration avancée, éditez directement config.py")
            print("ou utilisez les variables d'environnement (.env)")
            print()
        
        elif choice == '7':
            show_documentation()
        
        elif choice == '8':
            print()
            print(f"{Colors.GREEN}👋 Au revoir!{Colors.ENDC}")
            print()
            sys.exit(0)
        
        else:
            print()
            print(f"{Colors.FAIL}❌ Choix invalide. Essayez à nouveau.{Colors.ENDC}")
        
        print()
        input(f"{Colors.CYAN}Appuyez sur Entrée pour continuer...{Colors.ENDC}")
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print(f"{Colors.WARNING}⚠️  Programme interrompu{Colors.ENDC}")
        print()
        sys.exit(0)