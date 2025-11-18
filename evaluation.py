from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import warnings
warnings.filterwarnings("ignore")

textes_test = [
    "cette plateforme est nulle",
    "j'adore ce produit, il est fantastique!",
    "This platform is terrible",
    "I love this product, it's amazing!",
    "Le service client est très décevant",
    "The customer service is excellent"
]

model_name = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

classifier = pipeline(
    "sentiment-analysis",
    model=model,
    tokenizer=tokenizer
)

for texte in textes_test:

    print(f"Texte: {texte}")
            
    resultat = classifier(texte)[0]

    # Convertir en polarité
    label_map = {'negative': -1, 'neutral': 0, 'positive': 1}
    polarite = label_map.get(resultat['label'].lower(), 0) * resultat['score']


    print(f"Label: {resultat['label']}")
    print(f"Score: {resultat['score']:.3f}")
    print(f"Polarité: {polarite:.3f}\n")