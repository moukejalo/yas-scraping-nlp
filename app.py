"""
Application Streamlit - Analyse de Sentiments LinkedIn
Opérateur Yas
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from textblob import TextBlob
import re
import os
import glob 
from linkedin_scraper_selenium import main as main_scrapping

# Configuration de la page
st.set_page_config(
    page_title="Analyse Sentiments Yas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .recommendation-box {
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Fonction pour générer des données de démonstration
@st.cache_data
def generate_mock_data(n_posts=30):
    """Génère des données simulées pour la démonstration"""
    topics = ['Réseau', 'Service Client', 'Prix', 'Internet', 'Couverture', 'Offres', 'Application']
    
    data = []
    for i in range(n_posts):
        date = datetime.now() - timedelta(days=i)
        topic = np.random.choice(topics)
        
        # Génération du sentiment avec distribution réaliste
        sentiment_rand = np.random.random()
        if sentiment_rand < 0.40:
            sentiment = 'positif'
            score = np.random.uniform(0.6, 1.0)
        elif sentiment_rand < 0.75:
            sentiment = 'négatif'
            score = np.random.uniform(0.0, 0.4)
        else:
            sentiment = 'neutre'
            score = np.random.uniform(0.4, 0.6)
        
        # Génération de commentaires simulés
        comments = {
            'positif': [
                f"Excellent service {topic.lower()} chez Yas!",
                f"Très satisfait du {topic.lower()}, je recommande vivement.",
                f"Le {topic.lower()} de Yas s'est vraiment amélioré!",
                f"Bravo à Yas pour son {topic.lower()}!",
                f"Impressionné par le {topic.lower()}"
            ],
            'négatif': [
                f"Déçu par le {topic.lower()} de Yas...",
                f"Problèmes récurrents avec le {topic.lower()}",
                f"Le {topic.lower()} laisse vraiment à désirer",
                f"Insatisfait du {topic.lower()}, besoin d'amélioration",
                f"Franchement, le {topic.lower()} est décevant"
            ],
            'neutre': [
                f"{topic} correct chez Yas, rien d'exceptionnel",
                f"Service {topic.lower()} standard, sans plus",
                f"Expérience moyenne avec le {topic.lower()}"
            ]
        }
        
        comment = np.random.choice(comments[sentiment])
        
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'topic': topic,
            'sentiment': sentiment,
            'score': score,
            'comment': comment,
            'engagement': np.random.randint(10, 500)
        })
    
    return pd.DataFrame(data)

# Fonction d'analyse de sentiment (pour données réelles)
def analyze_sentiment(text):
    """Analyse le sentiment d'un texte"""
    try:
        blob = TextBlob(str(text))
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            return 'positif', polarity
        elif polarity < -0.1:
            return 'négatif', polarity
        else:
            return 'neutre', polarity
    except:
        return 'neutre', 0.0

# Fonction pour les recommandations
def get_recommendations(topic, sentiment_score):
    """Génère des recommandations basées sur l'analyse"""
    recommendations = {
        'Service Client': {
            'actions': [
                '🎓 Former les agents sur la gestion des réclamations complexes',
                '⏱️ Réduire le temps d\'attente moyen à moins de 3 minutes',
                '🤖 Implémenter un chatbot IA pour les questions fréquentes',
                '📞 Augmenter les effectifs aux heures de pointe'
            ],
            'kpi': 'Temps de réponse moyen et taux de satisfaction'
        },
        'Réseau': {
            'actions': [
                '📡 Investir dans l\'infrastructure 4G/5G dans les zones identifiées',
                '🗺️ Étendre la couverture dans les zones rurales prioritaires',
                '📊 Publier des rapports de couverture transparents',
                '🔧 Optimiser les antennes existantes pour améliorer la qualité'
            ],
            'kpi': 'Taux de couverture et débit moyen'
        },
        'Prix': {
            'actions': [
                '💰 Revoir la structure tarifaire pour plus de compétitivité',
                '🎁 Lancer des offres promotionnelles ciblées',
                '📝 Améliorer la transparence des tarifs et frais',
                '🔄 Proposer des formules flexibles sans engagement'
            ],
            'kpi': 'Part de marché et taux de churn'
        },
        'Internet': {
            'actions': [
                '🚀 Augmenter les débits disponibles de 20% minimum',
                '⚡ Optimiser la stabilité des connexions',
                '📦 Proposer des forfaits data plus généreux',
                '🌐 Améliorer la latence pour le gaming et streaming'
            ],
            'kpi': 'Débit moyen et taux de satisfaction internet'
        },
        'Couverture': {
            'actions': [
                '🏗️ Installer 50 nouvelles antennes dans les 6 prochains mois',
                '🏢 Optimiser la couverture indoor dans les bâtiments',
                '🗺️ Publier une carte de couverture interactive en temps réel',
                '📱 Tester et améliorer la couverture dans les transports'
            ],
            'kpi': 'Pourcentage de couverture nationale'
        },
        'Application': {
            'actions': [
                '🐛 Corriger les bugs signalés dans les 48h',
                '🎨 Refonte de l\'interface utilisateur (UX/UI)',
                '⚙️ Ajouter plus de fonctionnalités self-service',
                '📲 Optimiser les performances et réduire la consommation'
            ],
            'kpi': 'Note App Store/Play Store et taux d\'utilisation'
        },
        'Offres': {
            'actions': [
                '📋 Diversifier le catalogue avec 5 nouvelles offres',
                '✅ Simplifier les conditions contractuelles',
                '🎯 Créer des offres personnalisées basées sur l\'usage',
                '🔄 Faciliter les changements d\'offres en ligne'
            ],
            'kpi': 'Taux de conversion et satisfaction offres'
        }
    }
    
    return recommendations.get(topic, {
        'actions': ['Analyser en détail les retours clients', 'Mettre en place un plan d\'action'],
        'kpi': 'Satisfaction client'
    })

def extract_timestamp_post(filename):
    # Example: linkedin_yas_posts_20251111_160420.csv
    base = os.path.basename(filename)
    ts_str = base.replace("data/linkedin_yas_posts_", "").replace(".csv", "")
    return datetime.strptime(ts_str, "%Y%m%d_%H%M%S")

def extract_timestamp_comment(filename):
    # Example: linkedin_yas_posts_20251111_160420.csv
    base = os.path.basename(filename)
    ts_str = base.replace("data/linkedin_yas_comments_", "").replace(".csv", "")
    return datetime.strptime(ts_str, "%Y%m%d_%H%M%S")

def get_latest_file(folder_path, file_type):
    """
    file_type: "comments" or "posts"
    folder_path: directory where CSV files are stored
    """

    prefix = f"linkedin_yas_{file_type}_"

    # Get all matching files
    files = [
        f for f in os.listdir(folder_path)
        if f.startswith(prefix) and f.endswith(".csv")
    ]

    if not files:
        return None  # no file found

    # Extract timestamps and find the newest file
    def extract_datetime(filename):
        # Example: linkedin_yas_posts_20251114_145830.csv
        timestamp = filename.replace(prefix, "").replace(".csv", "")
        return datetime.strptime(timestamp, "%Y%m%d_%H%M%S")

    latest_file = max(files, key=lambda f: extract_datetime(f))

    return os.path.join(folder_path, latest_file)

# Titre principal
st.markdown('<p class="main-header">📊 Analyse de Sentiments - Opérateur Yas</p>', unsafe_allow_html=True)
st.markdown("### Analyse des 30 derniers posts LinkedIn")

# Sidebar pour les options
with st.sidebar:
    st.image("yas-senegal.jpeg", use_container_width=True)
    st.markdown("---")
    
    # st.subheader("⚙️ Configuration")
    
    # data_source = st.radio(
    #     "Source de données:",
    #     ["Données de démonstration", "Données scrapées"]
    # )
    data_source = st.radio(
        "Source de données:",
        ["Données scrapées"]
    )

    df_post = None
    df_comments = None
    
    uploaded_file = None
    uploaded_file = None
    if data_source == "Données scrapées":
        # get latest file
        folder = "data"
        latest_post_file = get_latest_file(folder, "posts")
        latest_comment_file = get_latest_file(folder, "comments")
        if latest_post_file and latest_comment_file:
            df_post = pd.read_csv(latest_post_file)
            df_comments = pd.read_csv(latest_comment_file)
        else:
            st.error("Aucun fichier trouvé.")

        # csv_files = glob.glob("linkedin_yas_posts_*.csv")
        # if not csv_files:
        #     st.error("Aucun fichier trouvé.")
        # else:
        #     # Extract the timestamp from each filename and sort
        #     uploaded_file = max(csv_files, key=extract_timestamp_post)
        #     df_post = pd.read_csv(uploaded_file)

        # # get latest file
        # csv_files = glob.glob("linkedin_yas_comments_*.csv")
        # if not csv_files:
        #     st.error("Aucun fichier trouvé.")
        # else:
        #     # Extract the timestamp from each filename and sort
        #     uploaded_file2 = max(csv_files, key=extract_timestamp_post)
        #     df_comments = pd.read_csv(uploaded_file2)

        # click on button start the scraper
        if st.button("Scraper LinkedIn"):
            st.write("Scrapping encours")
            df_post, df_comments = main_scrapping()
            st.write("Scrapping termine")
    


if df_post is not None:
# if True:
    try:
        df = df_post
        # st.write(df.head())
        # st.write(df_comments.head())
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du fichier: {e}")
        st.stop()
else:
    st.warning("⚠️ Cliquez sur le bouton 'Scraper LinkedIn' pour lancer le scrapping. Ensuite veuillez patienter")
    st.stop()

# Calcul des statistiques
total_posts = len(df)
positif_count = len(df[df['sentiment'] == 'positif'])
negatif_count = len(df[df['sentiment'] == 'négatif'])
neutre_count = len(df[df['sentiment'] == 'neutre'])

positif_pct = (positif_count / total_posts * 100) if total_posts > 0 else 0
negatif_pct = (negatif_count / total_posts * 100) if total_posts > 0 else 0
neutre_pct = (neutre_count / total_posts * 100) if total_posts > 0 else 0

# Calcul des statistiques des commentaires
total_comments = len(df_comments)
positif_comment_count = len(df_comments[df_comments['sentiment'] == 'positif'])
negatif_comment_count = len(df_comments[df_comments['sentiment'] == 'négatif'])
neutre_comment_count = len(df_comments[df_comments['sentiment'] == 'neutre'])

positif_comment_pct = (positif_comment_count / total_comments * 100) if total_comments > 0 else 0
negatif_comment_pct = (negatif_comment_count / total_comments * 100) if total_comments > 0 else 0
neutre_comment_pct = (neutre_comment_count / total_comments * 100) if total_comments > 0 else 0

# Métriques principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📝 Total Posts", total_posts)

with col2:
    st.metric("✅ Positif", f"{positif_pct:.1f}%", 
              delta=f"{positif_count} posts", 
              delta_color="normal")

with col3:
    st.metric("❌ Négatif", f"{negatif_pct:.1f}%", 
              delta=f"{negatif_count} posts", 
              delta_color="inverse")

with col4:
    st.metric("➖ Neutre", f"{neutre_pct:.1f}%", 
              delta=f"{neutre_count} posts", 
              delta_color="off")

st.markdown("---")


# # Métriques principales
# col1c, col2c, col3c, col4c = st.columns(4)

# with col1c:
#     st.metric("📝 Total Commentaires", total_comments)

# with col2c:
#     st.metric("✅ Positif", f"{positif_comment_pct:.1f}%", 
#               delta=f"{positif_comment_count} commentaires", 
#               delta_color="normal")

# with col3c:
#     st.metric("❌ Négatif", f"{negatif_pct:.1f}%", 
#               delta=f"{negatif_comment_count} commentaires", 
#               delta_color="inverse")

# with col4c:
#     st.metric("➖ Neutre", f"{neutre_comment_pct:.1f}%", 
#               delta=f"{neutre_comment_count} commentaires", 
#               delta_color="off")

# st.markdown("---")



# Graphiques
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊  Sentiments des postes")
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Positif', 'Négatif', 'Neutre'],
        values=[positif_count, negatif_count, neutre_count],
        marker=dict(colors=['#10b981', '#ef4444', '#94a3b8']),
        hole=0.4,
        textinfo='label+percent',
        textfont=dict(size=14)
    )])
    
    fig_pie.update_layout(
        showlegend=True,
        height=400,
        margin=dict(t=20, b=20, l=20, r=20)
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)


with col2:
    st.subheader("📊  Sentiments detaille des commentaires")

    # Bar chart (Histogram style)
    fig_bar = go.Figure(data=[
        go.Bar(
            x=['Positif', 'Négatif', 'Neutre'],      # categories
            y=[positif_comment_count, negatif_comment_count, neutre_comment_count],   # values
            marker=dict(color=['#10b981', '#ef4444', '#94a3b8']),  # colors
            text=[positif_comment_count, negatif_comment_count, neutre_comment_count],
            textposition='auto'
        )
    ])

    fig_bar.update_layout(
        xaxis_title="Sentiments",
        yaxis_title="Nombre de commentaire",
        height=400,
        margin=dict(t=20, b=20, l=20, r=20)
    )

    st.plotly_chart(fig_bar, use_container_width=True)

# Analyse par sujet
st.subheader("🎯 Analyse par Sujet")

topic_analysis = df.groupby(['topic', 'sentiment']).size().unstack(fill_value=0)
topic_analysis['total'] = topic_analysis.sum(axis=1)
topic_analysis['score'] = ((topic_analysis.get('positif', 0) - topic_analysis.get('négatif', 0)) / topic_analysis['total'] * 100)
topic_analysis = topic_analysis.sort_values('score')

fig_bar = go.Figure()

if 'positif' in topic_analysis.columns:
    fig_bar.add_trace(go.Bar(name='Positif', x=topic_analysis.index, y=topic_analysis['positif'], marker_color='#10b981'))
if 'neutre' in topic_analysis.columns:
    fig_bar.add_trace(go.Bar(name='Neutre', x=topic_analysis.index, y=topic_analysis['neutre'], marker_color='#94a3b8'))
if 'négatif' in topic_analysis.columns:
    fig_bar.add_trace(go.Bar(name='Négatif', x=topic_analysis.index, y=topic_analysis['négatif'], marker_color='#ef4444'))

fig_bar.update_layout(
    barmode='stack',
    height=400,
    xaxis_title="Sujet",
    yaxis_title="Nombre de mentions",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_bar, use_container_width=True)

# Recommandations
st.markdown("---")
st.subheader("💡 Recommandations Prioritaires")

# Identifier les sujets problématiques
problematic_topics = topic_analysis[topic_analysis['score'] < 0.5].sort_values('score')
# st.write(problematic_topics)
# st.write("problematic_topics")

if len(problematic_topics) > 0:
    for topic in problematic_topics.index[:3]:  # Top 3 problèmes
        score = problematic_topics.loc[topic, 'score']
        priority = "🔴 HAUTE" if score < -30 else "🟡 MOYENNE"
        
        st.markdown(f"### {priority} - {topic}")
        # st.markdown(f"**Score de sentiment:** {score:.1f}%")
        
        recs = get_recommendations(topic, score)
        
        st.markdown("**Actions recommandées:**")
        for action in recs['actions']:
            st.markdown(f"- {action}")
        
        st.markdown(f"**KPI à suivre:** {recs['kpi']}")
        st.markdown("---")
else:
    st.success("🎉 Aucun point critique détecté ! Continuez sur cette lancée.")
    st.balloons()

# Détail des posts
st.subheader("📋 Détail des Posts")

st.write(df)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 20px;'>
    <p>🔒 Données confidentielles - Usage interne uniquement</p>
    <p style='font-size: 0.9em;'>Développé pour l'analyse de sentiments LinkedIn de Yas</p>
</div>
""", unsafe_allow_html=True)