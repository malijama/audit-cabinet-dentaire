#!/bin/bash
# Script de déploiement pour Streamlit Cloud

echo "🚀 Déploiement de l'application Streamlit..."

# Vérifier que les données sont présentes
if [ ! -f "data/patients_mis_a_jour.xlsx" ]; then
    echo "❌ Fichier de données manquant : data/patients_mis_a_jour.xlsx"
    exit 1
fi

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run streamlit_app.py
