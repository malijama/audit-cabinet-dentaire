#!/usr/bin/env python3
import json
import os
import glob

# Trouver le fichier notebook
notebook_files = glob.glob("*.ipynb")
print("Fichiers notebook trouvés:", notebook_files)

if notebook_files:
    notebook_file = notebook_files[0]
    print(f"Lecture du fichier: {notebook_file}")
    
    try:
        with open(notebook_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Nombre total de cellules: {len(data['cells'])}")
        
        # Analyser les premières cellules
        for i, cell in enumerate(data['cells'][:10]):
            cell_type = cell.get('cell_type', 'unknown')
            source = cell.get('source', [])
            if isinstance(source, list):
                source_text = ''.join(source)
            else:
                source_text = str(source)
            
            print(f"\nCellule {i+1} ({cell_type}):")
            print(f"Source: {source_text[:200]}...")
            
    except Exception as e:
        print(f"Erreur lors de la lecture: {e}")
else:
    print("Aucun fichier notebook trouvé") 