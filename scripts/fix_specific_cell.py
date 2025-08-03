#!/usr/bin/env python3
import json
import os

def fix_specific_cell():
    # Charger le notebook
    notebook_files = [f for f in os.listdir('.') if f.endswith('.ipynb')]
    notebook_file = notebook_files[0]
    
    with open(notebook_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"🔍 Recherche de la cellule problématique...")
    
    # Parcourir toutes les cellules pour trouver celle qui pose problème
    for i, cell in enumerate(data['cells']):
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source'])
            if 'df["date_du_soin"]' in source or 'df["Date"]' in source:
                print(f"📝 Cellule {i+1} trouvée avec problème de date")
                print(f"   Contenu actuel : {source[:200]}...")
                
                # Corriger cette cellule spécifiquement
                new_source = []
                for line in cell['source']:
                    # Remplacer les références de colonnes de date
                    new_line = line.replace('df["Date"]', 'df["date_du_soin"]')
                    new_line = new_line.replace('df["date_du_soin"]', 'df["date_du_soin"]')
                    new_source.append(new_line)
                
                cell['source'] = new_source
                print(f"   ✅ Cellule {i+1} corrigée")
    
    # Sauvegarder le notebook corrigé
    with open(notebook_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("✅ Corrections terminées")

if __name__ == "__main__":
    fix_specific_cell() 