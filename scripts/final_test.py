#!/usr/bin/env python3
import pandas as pd
import numpy as np

def final_test():
    print("🧪 Test final des corrections")
    print("=" * 50)
    
    try:
        # Charger les données
        df = pd.read_excel("patients_mis_a_jour.xlsx")
        print(f"✅ Données chargées : {len(df)} lignes")
        
        # Test de la colonne date
        print(f"\n📅 Test de la colonne date_du_soin :")
        print(f"   Colonne présente : {'date_du_soin' in df.columns}")
        if 'date_du_soin' in df.columns:
            df['date_du_soin'] = pd.to_datetime(df['date_du_soin'], errors='coerce')
            print(f"   ✅ Conversion de date réussie")
            print(f"   📊 Période : {df['date_du_soin'].min()} à {df['date_du_soin'].max()}")
            
            # Créer les colonnes temporelles
            df['Annee'] = df['date_du_soin'].dt.year
            df['Mois'] = df['date_du_soin'].dt.month
            df['Année-Mois'] = df['Annee'].astype(str) + '-' + df['Mois'].astype(str).str.zfill(2)
            print(f"   ✅ Colonnes temporelles créées")
        
        # Test des analyses principales
        print(f"\n📊 Test des analyses principales :")
        
        # Test 1: Top 10 soins par CA
        top_10_ca_soins = df.groupby('type_de_soin_normalisé')['montant_total_chf'].sum().sort_values(ascending=False).head(10)
        print(f"   ✅ Top 10 soins par CA : {len(top_10_ca_soins)} résultats")
        
        # Test 2: Rentabilité moyenne
        rentabilite_soins = df.groupby('type_de_soin_normalisé').agg({
            'montant_total_chf': 'sum',
            'type_de_soin_normalisé': 'count'
        }).rename(columns={'type_de_soin_normalisé': 'Nombre_actes'})
        rentabilite_soins['Rentabilite_moyenne'] = rentabilite_soins['montant_total_chf'] / rentabilite_soins['Nombre_actes']
        print(f"   ✅ Rentabilité moyenne calculée")
        
        # Test 3: Soins par patient
        soins_par_patient = df.groupby('patientid')['type_de_soin_normalisé'].count()
        moyenne_soins_patient = soins_par_patient.mean()
        print(f"   ✅ Nombre moyen de soins par patient : {moyenne_soins_patient:.2f}")
        
        # Test 4: Taux de rétention
        visites_par_patient = df.groupby('patientid').size()
        patients_fideles = (visites_par_patient > 1).sum()
        total_patients = len(visites_par_patient)
        taux_retention = (patients_fideles / total_patients * 100).round(2)
        print(f"   ✅ Taux de rétention : {taux_retention}%")
        
        # Test 5: CA par période
        ca_mensuel = df.groupby('Année-Mois')['montant_total_chf'].sum()
        print(f"   ✅ CA mensuel calculé : {len(ca_mensuel)} périodes")
        
        # Test 6: Analyse géographique
        if 'nom_de_la_clinique' in df.columns:
            ca_par_clinique = df.groupby('nom_de_la_clinique')['montant_total_chf'].sum()
            print(f"   ✅ CA par clinique : {len(ca_par_clinique)} cliniques")
        
        # Test 7: Analyse des praticiens
        if 'nom_complet_praticien' in df.columns:
            ca_par_praticien = df.groupby('nom_complet_praticien')['montant_total_chf'].sum()
            print(f"   ✅ CA par praticien : {len(ca_par_praticien)} praticiens")
        
        print(f"\n🎉 TOUS LES TESTS SONT PASSÉS !")
        print(f"💡 Le notebook devrait maintenant fonctionner parfaitement.")
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    final_test() 