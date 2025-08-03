#!/usr/bin/env python3
import json
import os

def analyze_notebook():
    # Trouver le fichier notebook
    notebook_files = [f for f in os.listdir('.') if f.endswith('.ipynb')]
    if not notebook_files:
        print("Aucun fichier notebook trouvé")
        return
    
    notebook_file = notebook_files[0]
    print(f"Analyse du fichier: {notebook_file}")
    
    try:
        with open(notebook_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Nombre total de cellules: {len(data['cells'])}")
        print("\nStructure des cellules:")
        
        for i, cell in enumerate(data['cells']):
            cell_type = cell.get('cell_type', 'unknown')
            source = cell.get('source', [])
            
            # Extraire le début du contenu
            content_start = ""
            if source:
                if isinstance(source, list):
                    content_start = "".join(source)[:100]
                else:
                    content_start = str(source)[:100]
            
            print(f"Cellule {i+1}: {cell_type}")
            if content_start.strip():
                print(f"  Contenu: {content_start}...")
            print()
            
    except Exception as e:
        print(f"Erreur lors de la lecture: {e}")

if __name__ == "__main__":
    analyze_notebook() 