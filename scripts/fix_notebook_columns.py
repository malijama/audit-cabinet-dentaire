#!/usr/bin/env python3
import json
import os

def fix_notebook_columns():
    # Charger le notebook
    notebook_files = [f for f in os.listdir('.') if f.endswith('.ipynb')]
    notebook_file = notebook_files[0]
    
    with open(notebook_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Mapping des anciens noms vers les nouveaux noms
    column_mapping = {
        'Patient': 'patientid',
        'Type De Soin Normalisé': 'type_de_soin_normalisé',
        'Montant (CHF)': 'montant_total_chf',
        'Date': 'date_du_soin',
        'Sexe': 'sexe',
        'Type De Patient': 'type_de_patient',
        'Ville': 'nom_de_la_clinique',  # Utiliser la clinique comme ville
        'Praticien': 'nom_complet_praticien',
        'Année': 'année',
        'Mois': 'mois',
        'Année-Mois': 'année_mois'
    }
    
    # Compter les corrections
    corrections_count = 0
    
    # Parcourir toutes les cellules de code
    for cell in data['cells']:
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source'])
            
            # Remplacer les noms de colonnes
            for old_name, new_name in column_mapping.items():
                if old_name in source:
                    # Remplacer dans le code source
                    cell['source'] = [line.replace(old_name, new_name) for line in cell['source']]
                    corrections_count += 1
    
    # Sauvegarder le notebook corrigé
    with open(notebook_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ {corrections_count} corrections de noms de colonnes effectuées")
    print("📋 Mapping des colonnes :")
    for old_name, new_name in column_mapping.items():
        print(f"   {old_name} → {new_name}")

if __name__ == "__main__":
    fix_notebook_columns() 