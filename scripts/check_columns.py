#!/usr/bin/env python3
import pandas as pd

def check_dataframe_columns():
    # Charger les données
    df = pd.read_excel("patients_mis_a_jour.xlsx")
    
    print("📊 Colonnes disponibles dans le DataFrame :")
    print("=" * 50)
    for i, col in enumerate(df.columns, 1):
        print(f"{i:2d}. {col}")
    
    print(f"\n📈 Informations sur le DataFrame :")
    print(f"   - Nombre de lignes : {len(df)}")
    print(f"   - Nombre de colonnes : {len(df.columns)}")
    print(f"   - Types de données :")
    print(df.dtypes.value_counts())
    
    # Chercher des colonnes similaires à 'Patient'
    colonnes_patient = [col for col in df.columns if 'patient' in col.lower() or 'nom' in col.lower() or 'client' in col.lower()]
    print(f"\n🔍 Colonnes potentiellement liées aux patients :")
    for col in colonnes_patient:
        print(f"   - {col}")
    
    # Chercher des colonnes similaires à 'Type De Soin Normalisé'
    colonnes_soin = [col for col in df.columns if 'soin' in col.lower() or 'type' in col.lower() or 'acte' in col.lower()]
    print(f"\n🦷 Colonnes potentiellement liées aux soins :")
    for col in colonnes_soin:
        print(f"   - {col}")
    
    # Afficher les premières lignes pour comprendre la structure
    print(f"\n📋 Premières lignes du DataFrame :")
    print(df.head())

if __name__ == "__main__":
    check_dataframe_columns() 