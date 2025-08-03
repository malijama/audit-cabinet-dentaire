#!/usr/bin/env python3
import json
import os

def fix_date_column():
    # Charger le notebook
    notebook_files = [f for f in os.listdir('.') if f.endswith('.ipynb')]
    notebook_file = notebook_files[0]
    
    with open(notebook_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Mapping complet des colonnes
    column_mapping = {
        'Patient': 'patientid',
        'Type De Soin Normalisé': 'type_de_soin_normalisé',
        'Montant (CHF)': 'montant_total_chf',
        'Date': 'date_du_soin',
        'Sexe': 'sexe',
        'Type De Patient': 'type_de_patient',
        'Ville': 'nom_de_la_clinique',
        'Praticien': 'nom_complet_praticien',
        'Année': 'Annee',
        'Mois': 'Mois',
        'Année-Mois': 'Année-Mois',
        'date_du_soin': 'date_du_soin',  # Garder le même nom
        'Annee': 'Annee',
        'Mois': 'Mois'
    }
    
    corrections_count = 0
    
    # Parcourir toutes les cellules
    for cell in data['cells']:
        if cell['cell_type'] == 'code':
            # Remplacer les noms de colonnes dans chaque ligne
            new_source = []
            for line in cell['source']:
                new_line = line
                for old_name, new_name in column_mapping.items():
                    if old_name in new_line:
                        new_line = new_line.replace(old_name, new_name)
                        corrections_count += 1
                new_source.append(new_line)
            cell['source'] = new_source
    
    # Sauvegarder le notebook corrigé
    with open(notebook_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ {corrections_count} corrections effectuées")
    print("📋 Colonnes mappées :")
    for old_name, new_name in column_mapping.items():
        print(f"   {old_name} → {new_name}")

if __name__ == "__main__":
    fix_date_column() 