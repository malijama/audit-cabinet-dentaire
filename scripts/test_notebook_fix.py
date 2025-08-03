#!/usr/bin/env python3
import pandas as pd
import numpy as np

def test_notebook_fix():
    print("🧪 Test des corrections du notebook")
    print("=" * 50)
    
    # Charger les données
    df = pd.read_excel("patients_mis_a_jour.xlsx")
    print(f"✅ Données chargées : {len(df)} lignes, {len(df.columns)} colonnes")
    
    # Test 1: Vérifier que les colonnes principales existent
    colonnes_requises = [
        'patientid',
        'type_de_soin_normalisé', 
        'montant_total_chf',
        'date_du_soin',
        'sexe',
        'type_de_patient',
        'nom_de_la_clinique',
        'nom_complet_praticien'
    ]
    
    print("\n📋 Test des colonnes requises :")
    for col in colonnes_requises:
        if col in df.columns:
            print(f"   ✅ {col}")
        else:
            print(f"   ❌ {col} - MANQUANTE")
    
    # Test 2: Vérifier le format de date
    print("\n📅 Test du format de date :")
    try:
        df['date_du_soin'] = pd.to_datetime(df['date_du_soin'], errors='coerce')
        print(f"   ✅ Conversion de date réussie")
        print(f"   📊 Période : {df['date_du_soin'].min()} à {df['date_du_soin'].max()}")
    except Exception as e:
        print(f"   ❌ Erreur de conversion de date : {e}")
    
    # Test 3: Créer les colonnes temporelles
    print("\n⏰ Test des colonnes temporelles :")
    try:
        df['Annee'] = df['date_du_soin'].dt.year
        df['Mois'] = df['date_du_soin'].dt.month
        df['Année-Mois'] = df['Annee'].astype(str) + '-' + df['Mois'].astype(str).str.zfill(2)
        print(f"   ✅ Colonnes temporelles créées")
        print(f"   📊 Années : {sorted(df['Annee'].unique())}")
    except Exception as e:
        print(f"   ❌ Erreur création colonnes temporelles : {e}")
    
    # Test 4: Test des analyses principales
    print("\n📊 Test des analyses principales :")
    
    try:
        # Test 1.1: Top 10 soins par CA
        top_10_ca_soins = df.groupby('type_de_soin_normalisé')['montant_total_chf'].sum().sort_values(ascending=False).head(10)
        print(f"   ✅ Top 10 soins par CA calculé ({len(top_10_ca_soins)} résultats)")
        
        # Test 1.2: Rentabilité moyenne
        rentabilite_soins = df.groupby('type_de_soin_normalisé').agg({
            'montant_total_chf': 'sum',
            'type_de_soin_normalisé': 'count'
        }).rename(columns={'type_de_soin_normalisé': 'Nombre_actes'})
        rentabilite_soins['Rentabilite_moyenne'] = rentabilite_soins['montant_total_chf'] / rentabilite_soins['Nombre_actes']
        print(f"   ✅ Rentabilité moyenne calculée")
        
        # Test 1.3: Soins par patient
        soins_par_patient = df.groupby('patientid')['type_de_soin_normalisé'].count()
        moyenne_soins_patient = soins_par_patient.mean()
        print(f"   ✅ Nombre moyen de soins par patient : {moyenne_soins_patient:.2f}")
        
        # Test 3.1: Taux de rétention
        visites_par_patient = df.groupby('patientid').size()
        patients_fideles = (visites_par_patient > 1).sum()
        total_patients = len(visites_par_patient)
        taux_retention = (patients_fideles / total_patients * 100).round(2)
        print(f"   ✅ Taux de rétention : {taux_retention}%")
        
        # Test 6.1: CA par période
        ca_mensuel = df.groupby('Année-Mois')['montant_total_chf'].sum()
        print(f"   ✅ CA mensuel calculé ({len(ca_mensuel)} périodes)")
        
    except Exception as e:
        print(f"   ❌ Erreur dans les analyses : {e}")
    
    print("\n🎉 Tests terminés !")
    print("💡 Si tous les tests sont ✅, le notebook devrait fonctionner correctement.")

if __name__ == "__main__":
    test_notebook_fix() 