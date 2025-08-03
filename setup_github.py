#!/usr/bin/env python3
import os
import shutil
import subprocess

def setup_github_project():
    print("🚀 Configuration du projet pour GitHub")
    print("=" * 50)
    
    # Créer les dossiers nécessaires
    folders = ['scripts', 'data', 'visualisations', 'docs', '.streamlit']
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"✅ Dossier créé : {folder}/")
    
    # Déplacer les scripts utilitaires
    script_files = [
        'analyze_notebook.py',
        'add_analysis_sections.py', 
        'fix_notebook_columns.py',
        'fix_specific_cell.py',
        'test_notebook_fix.py',
        'final_test.py',
        'check_columns.py',
        'verify_notebook.py'
    ]
    
    for script in script_files:
        if os.path.exists(script):
            shutil.move(script, f"scripts/{script}")
            print(f"📁 Script déplacé : {script} → scripts/{script}")
    
    # Déplacer les données
    data_files = ['patients_mis_a_jour.xlsx']
    for data_file in data_files:
        if os.path.exists(data_file):
            shutil.move(data_file, f"data/{data_file}")
            print(f"📊 Données déplacées : {data_file} → data/{data_file}")
    
    # Déplacer les visualisations
    viz_files = ['performance_soins.png']
    for viz_file in viz_files:
        if os.path.exists(viz_file):
            shutil.move(viz_file, f"visualisations/{viz_file}")
            print(f"📈 Visualisation déplacée : {viz_file} → visualisations/{viz_file}")
    
    # Créer un fichier de configuration Streamlit
    streamlit_config = """
[server]
headless = true
port = 8501
enableCORS = false

[browser]
gatherUsageStats = false
"""
    
    with open('.streamlit/config.toml', 'w') as f:
        f.write(streamlit_config)
    print("⚙️ Configuration Streamlit créée")
    
    # Créer un fichier de déploiement
    deploy_script = """#!/bin/bash
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
"""
    
    with open('deploy.sh', 'w') as f:
        f.write(deploy_script)
    os.chmod('deploy.sh', 0o755)
    print("📜 Script de déploiement créé : deploy.sh")
    
    # Créer un fichier de documentation rapide
    quick_start = """# 🚀 Démarrage Rapide

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
"""
    
    with open('QUICKSTART.md', 'w') as f:
        f.write(quick_start)
    print("📖 Guide de démarrage rapide créé : QUICKSTART.md")
    
    print("\n🎉 Configuration terminée !")
    print("\n📋 Prochaines étapes :")
    print("1. git init")
    print("2. git add .")
    print("3. git commit -m 'Initial commit'")
    print("4. Créer un repository sur GitHub")
    print("5. git remote add origin <votre-repo-url>")
    print("6. git push -u origin main")
    print("\n💡 Pour tester l'application :")
    print("   streamlit run streamlit_app.py")

if __name__ == "__main__":
    setup_github_project() 