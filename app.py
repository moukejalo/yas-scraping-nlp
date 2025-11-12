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

# Titre principal
st.markdown('<p class="main-header">📊 Analyse de Sentiments - Opérateur Yas</p>', unsafe_allow_html=True)
st.markdown("### Analyse des 30 derniers posts LinkedIn")

# Sidebar pour les options
with st.sidebar:
    st.image("yas-senegal.jpeg", use_container_width=True)
    st.markdown("---")
    
    st.subheader("⚙️ Configuration")
    
    data_source = st.radio(
        "Source de données:",
        ["Données de démonstration", "Importer un fichier CSV"]
    )
    
    uploaded_file = None
    if data_source == "Importer un fichier CSV":
        uploaded_file = st.file_uploader("Choisir un fichier CSV", type=['csv'])
        st.info("Format attendu: date, topic, comment")
    
    st.markdown("---")
    st.subheader("📅 Période")
    date_range = st.slider("Nombre de jours", 7, 90, 30)
    
    st.markdown("---")
    st.markdown("### 📖 Guide d'utilisation")
    with st.expander("Comment utiliser cette app?"):
        st.markdown("""
        1. **Données**: Utilisez les données de démo ou importez votre CSV
        2. **Analyse**: Consultez les statistiques et graphiques
        3. **Recommandations**: Suivez les actions prioritaires
        4. **Export**: Téléchargez le rapport complet
        """)

# Chargement des données
if data_source == "Données de démonstration":
    df = generate_mock_data(date_range)
    st.info("ℹ️ Vous utilisez des données simulées. Pour analyser vos vraies données LinkedIn, importez un fichier CSV.")
else:
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            # Analyse de sentiment si pas déjà présent
            if 'sentiment' not in df.columns:
                with st.spinner("Analyse des sentiments en cours..."):
                    results = df['comment'].apply(lambda x: pd.Series(analyze_sentiment(x)))
                    df['sentiment'] = results[0]
                    df['score'] = results[1]
            st.success(f"✅ {len(df)} posts importés et analysés")
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement du fichier: {e}")
            st.stop()
    else:
        st.warning("⚠️ Veuillez importer un fichier CSV")
        st.stop()

# Calcul des statistiques
total_posts = len(df)
positif_count = len(df[df['sentiment'] == 'positif'])
negatif_count = len(df[df['sentiment'] == 'négatif'])
neutre_count = len(df[df['sentiment'] == 'neutre'])

positif_pct = (positif_count / total_posts * 100) if total_posts > 0 else 0
negatif_pct = (negatif_count / total_posts * 100) if total_posts > 0 else 0
neutre_pct = (neutre_count / total_posts * 100) if total_posts > 0 else 0

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

# Graphiques
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Distribution des Sentiments")
    
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
    st.subheader("📈 Évolution dans le Temps")
    
    df_time = df.groupby(['date', 'sentiment']).size().reset_index(name='count')
    
    fig_line = px.line(
        df_time, 
        x='date', 
        y='count', 
        color='sentiment',
        color_discrete_map={'positif': '#10b981', 'négatif': '#ef4444', 'neutre': '#94a3b8'},
        markers=True
    )
    
    fig_line.update_layout(
        height=400,
        xaxis_title="Date",
        yaxis_title="Nombre de posts",
        margin=dict(t=20, b=20, l=20, r=20),
        legend=dict(title="Sentiment")
    )
    
    st.plotly_chart(fig_line, use_container_width=True)

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
problematic_topics = topic_analysis[topic_analysis['score'] < 0].sort_values('score')

if len(problematic_topics) > 0:
    for topic in problematic_topics.index[:3]:  # Top 3 problèmes
        score = problematic_topics.loc[topic, 'score']
        priority = "🔴 HAUTE" if score < -30 else "🟡 MOYENNE"
        
        st.markdown(f"### {priority} - {topic}")
        st.markdown(f"**Score de sentiment:** {score:.1f}%")
        
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

filter_sentiment = st.multiselect(
    "Filtrer par sentiment:",
    options=['positif', 'négatif', 'neutre'],
    default=['positif', 'négatif', 'neutre']
)

filter_topic = st.multiselect(
    "Filtrer par sujet:",
    options=df['topic'].unique().tolist(),
    default=df['topic'].unique().tolist()
)

df_filtered = df[
    (df['sentiment'].isin(filter_sentiment)) & 
    (df['topic'].isin(filter_topic))
].sort_values('date', ascending=False)

# Affichage avec couleurs
def color_sentiment(val):
    colors = {'positif': 'background-color: #218050', 
              'négatif': 'background-color: #9c2222', 
              'neutre': 'background-color: #8c9dad'}
    return colors.get(val, '')

st.dataframe(
    df_filtered[['date', 'topic', 'sentiment', 'comment', 'engagement']]
    .style.applymap(color_sentiment, subset=['sentiment']),
    use_container_width=True,
    height=400
)

# Export des résultats
st.markdown("---")
st.subheader("📥 Export des Résultats")

col1, col2 = st.columns(2)

with col1:
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📊 Télécharger les données (CSV)",
        data=csv,
        file_name=f"yas_sentiment_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with col2:
    # Créer un rapport texte
    report = f"""
RAPPORT D'ANALYSE DE SENTIMENTS - YAS
Date: {datetime.now().strftime('%d/%m/%Y')}
Période analysée: {date_range} jours

STATISTIQUES GLOBALES:
- Total de posts analysés: {total_posts}
- Sentiments positifs: {positif_pct:.1f}% ({positif_count} posts)
- Sentiments négatifs: {negatif_pct:.1f}% ({negatif_count} posts)
- Sentiments neutres: {neutre_pct:.1f}% ({neutre_count} posts)

SUJETS PROBLÉMATIQUES:
"""
    
    for i, topic in enumerate(problematic_topics.index[:3], 1):
        score = problematic_topics.loc[topic, 'score']
        report += f"\n{i}. {topic} (Score: {score:.1f}%)\n"
        recs = get_recommendations(topic, score)
        for action in recs['actions']:
            report += f"   - {action}\n"
    
    st.download_button(
        label="📄 Télécharger le rapport (TXT)",
        data=report,
        file_name=f"rapport_yas_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain"
    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 20px;'>
    <p>🔒 Données confidentielles - Usage interne uniquement</p>
    <p style='font-size: 0.9em;'>Développé pour l'analyse de sentiments LinkedIn de Yas</p>
</div>
""", unsafe_allow_html=True)