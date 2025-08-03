# 🚀 Démarrage Rapide

## Installation Locale

1. **Cloner le projet**
```bash
git clone <votre-repo-url>
cd audit-cabinet-dentaire
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Lancer l'application**
```bash
streamlit run streamlit_app.py
```

## Déploiement Streamlit Cloud

1. Connectez votre repository GitHub à Streamlit Cloud
2. Configurez le chemin vers `streamlit_app.py`
3. Ajoutez les variables d'environnement si nécessaire

## Structure des Données

Le fichier `data/patients_mis_a_jour.xlsx` doit contenir les colonnes :
- patientid
- type_de_soin_normalisé
- montant_total_chf
- date_du_soin
- sexe
- type_de_patient
- nom_de_la_clinique
- nom_complet_praticien

## Support

Pour toute question, ouvrez une issue sur GitHub.
