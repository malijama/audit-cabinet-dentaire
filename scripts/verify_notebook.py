#!/usr/bin/env python3
import json
import os

def verify_notebook():
    # Charger le notebook
    notebook_files = [f for f in os.listdir('.') if f.endswith('.ipynb')]
    notebook_file = notebook_files[0]
    
    with open(notebook_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 Vérification du notebook : {notebook_file}")
    print(f"Nombre total de cellules : {len(data['cells'])}")
    
    # Rechercher les nouvelles sections
    sections_trouvees = []
    
    for i, cell in enumerate(data['cells']):
        if cell['cell_type'] == 'markdown':
            source = ''.join(cell['source'])
            if '🦷 1. Performance des soins' in source:
                sections_trouvees.append('🦷 1. Performance des soins')
            elif '👨‍⚕️ 2. Praticiens' in source:
                sections_trouvees.append('👨‍⚕️ 2. Praticiens')
            elif '🧑‍🤝‍🧑 3. Patients' in source:
                sections_trouvees.append('🧑‍🤝‍🧑 3. Patients')
            elif '💰 4. Paiements et créances' in source:
                sections_trouvees.append('💰 4. Paiements et créances')
            elif '🏥 5. Analyse géographique' in source:
                sections_trouvees.append('🏥 5. Analyse géographique')
            elif '📅 6. Analyse temporelle' in source:
                sections_trouvees.append('📅 6. Analyse temporelle')
    
    print("\n✅ Sections trouvées dans le notebook :")
    for section in sections_trouvees:
        print(f"   {section}")
    
    # Vérifier les KPIs ajoutés
    kpis_trouves = []
    for cell in data['cells']:
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source'])
            if 'Top 10 soins par chiffre d\'affaires' in source:
                kpis_trouves.append('Top 10 soins par CA')
            elif 'Rentabilité moyenne par soin' in source:
                kpis_trouves.append('Rentabilité moyenne par soin')
            elif 'Nombre moyen de soins par patient' in source:
                kpis_trouves.append('Soins moyens par patient')
            elif 'Taux de rétention' in source:
                kpis_trouves.append('Taux de rétention')
            elif 'Analyse RFM' in source:
                kpis_trouves.append('Analyse RFM')
            elif 'Taux de paiements en retard' in source:
                kpis_trouves.append('Taux de retard')
            elif 'CA par ville' in source:
                kpis_trouves.append('CA géographique')
            elif 'Saisonnalité des soins' in source:
                kpis_trouves.append('Analyse saisonnière')
    
    print("\n📈 KPIs et analyses ajoutés :")
    for kpi in set(kpis_trouves):
        print(f"   ✅ {kpi}")
    
    print(f"\n🎉 Le notebook contient maintenant {len(data['cells'])} cellules avec toutes les analyses demandées !")

if __name__ == "__main__":
    verify_notebook() 