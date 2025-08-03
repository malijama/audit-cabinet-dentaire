#!/usr/bin/env python3
"""
Analyse complète des KPIs d'un cabinet dentaire multi-sites
Auteur: Assistant IA
Date: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configuration pour les graphiques
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class AnalyseDentaire:
    def __init__(self, fichier_donnees="patients_mis_a_jour.xlsx"):
        """Initialisation de l'analyse"""
        print("🦷 Chargement des données dentaires...")
        self.df = pd.read_excel(fichier_donnees)
        print(f"✅ Données chargées: {self.df.shape[0]} lignes, {self.df.shape[1]} colonnes")
        
        # Nettoyage initial
        self.nettoyer_donnees()
        
    def nettoyer_donnees(self):
        """Nettoyage et préparation des données"""
        print("🧹 Nettoyage des données...")
        
        # Conversion des colonnes de dates
        colonnes_dates = self.df.select_dtypes(include=['object']).columns
        for col in colonnes_dates:
            if 'date' in col.lower() or 'jour' in col.lower():
                try:
                    self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                except:
                    pass
        
        # Nettoyage des colonnes numériques
        colonnes_numeriques = self.df.select_dtypes(include=[np.number]).columns
        for col in colonnes_numeriques:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
    
    def analyse_performance_soins(self):
        """🦷 1. Performance des soins"""
        print("\n" + "="*50)
        print("🦷 ANALYSE 1: PERFORMANCE DES SOINS")
        print("="*50)
        
        # Top 10 soins par chiffre d'affaires
        if 'type_soin' in self.df.columns and 'montant' in self.df.columns:
            top_soins = self.df.groupby('type_soin')['montant'].agg(['sum', 'count', 'mean']).round(2)
            top_soins.columns = ['CA_Total', 'Nombre_Actes', 'CA_Moyen']
            top_soins = top_soins.sort_values('CA_Total', ascending=False).head(10)
            
            print("\n📊 TOP 10 SOINS PAR CHIFFRE D'AFFAIRES:")
            print(top_soins)
            
            # Rentabilité par minute (si durée disponible)
            if 'duree_soin' in self.df.columns:
                rentabilite_minute = self.df.groupby('type_soin').apply(
                    lambda x: (x['montant'].sum() / x['duree_soin'].sum()) if x['duree_soin'].sum() > 0 else 0
                ).round(2)
                print("\n⏱️ RENTABILITÉ PAR MINUTE:")
                print(rentabilite_minute.sort_values(ascending=False).head(10))
        
        # Nombre moyen de soins par patient
        if 'patient_id' in self.df.columns:
            soins_par_patient = self.df.groupby('patient_id').size()
            print(f"\n👥 NOMBRE MOYEN DE SOINS PAR PATIENT: {soins_par_patient.mean():.2f}")
            print(f"📈 Médiane: {soins_par_patient.median():.0f}")
            print(f"🔝 Max: {soins_par_patient.max()}")
    
    def analyse_praticiens(self):
        """👨‍⚕️ 2. Praticiens"""
        print("\n" + "="*50)
        print("👨‍⚕️ ANALYSE 2: PRATICIENS")
        print("="*50)
        
        if 'praticien' in self.df.columns and 'montant' in self.df.columns:
            # CA moyen par praticien
            ca_praticien = self.df.groupby('praticien')['montant'].agg(['sum', 'count', 'mean']).round(2)
            ca_praticien.columns = ['CA_Total', 'Nombre_Actes', 'CA_Moyen']
            ca_praticien = ca_praticien.sort_values('CA_Total', ascending=False)
            
            print("\n💰 CA PAR PRATICIEN:")
            print(ca_praticien)
            
            # Taux de fidélisation (patients revenus)
            if 'patient_id' in self.df.columns:
                fidelisation = self.df.groupby(['praticien', 'patient_id']).size().reset_index()
                fidelisation = fidelisation.groupby('praticien').apply(
                    lambda x: (x[x[0] > 1].shape[0] / x.shape[0]) * 100
                ).round(2)
                
                print("\n👥 TAUX DE FIDÉLISATION PAR PRATICIEN (%):")
                print(fidelisation.sort_values(ascending=False))
    
    def analyse_patients(self):
        """🧑‍🤝‍🧑 3. Patients"""
        print("\n" + "="*50)
        print("🧑‍🤝‍🧑 ANALYSE 3: PATIENTS")
        print("="*50)
        
        if 'patient_id' in self.df.columns:
            # Taux de rétention
            visites_par_patient = self.df.groupby('patient_id').size()
            patients_fideles = (visites_par_patient > 1).sum()
            taux_retention = (patients_fideles / len(visites_par_patient)) * 100
            
            print(f"\n📊 TAUX DE RÉTENTION: {taux_retention:.1f}%")
            print(f"👥 Patients fidèles (2+ visites): {patients_fideles}")
            print(f"👤 Total patients: {len(visites_par_patient)}")
            
            # Analyse RFM
            if 'date_soin' in self.df.columns:
                self.analyse_rfm()
    
    def analyse_rfm(self):
        """Analyse RFM (Récence, Fréquence, Montant)"""
        print("\n📊 ANALYSE RFM:")
        
        # Calcul RFM
        rfm = self.df.groupby('patient_id').agg({
            'date_soin': lambda x: (pd.Timestamp.now() - x.max()).days,  # Récence
            'patient_id': 'count',  # Fréquence
            'montant': 'sum'  # Montant
        }).rename(columns={'date_soin': 'recence', 'patient_id': 'frequence', 'montant': 'montant'})
        
        # Segmentation RFM
        rfm['R'] = pd.qcut(rfm['recence'], q=4, labels=['4', '3', '2', '1'])
        rfm['F'] = pd.qcut(rfm['frequence'], q=4, labels=['1', '2', '3', '4'])
        rfm['M'] = pd.qcut(rfm['montant'], q=4, labels=['1', '2', '3', '4'])
        
        rfm['RFM_Score'] = rfm['R'].astype(str) + rfm['F'].astype(str) + rfm['M'].astype(str)
        
        # Classification des segments
        def segment_rfm(row):
            if row['RFM_Score'] >= '444':
                return 'VIP'
            elif row['RFM_Score'] >= '333':
                return 'Fidèle'
            elif row['RFM_Score'] >= '222':
                return 'Actif'
            else:
                return 'À risque'
        
        rfm['Segment'] = rfm.apply(segment_rfm, axis=1)
        
        print("\n📈 RÉPARTITION DES SEGMENTS:")
        print(rfm['Segment'].value_counts())
        
        print("\n💰 MONTANT MOYEN PAR SEGMENT:")
        print(rfm.groupby('Segment')['montant'].mean().round(2))
    
    def analyse_paiements(self):
        """💰 4. Paiements et créances"""
        print("\n" + "="*50)
        print("💰 ANALYSE 4: PAIEMENTS ET CRÉANCES")
        print("="*50)
        
        if 'date_paiement' in self.df.columns and 'date_soin' in self.df.columns:
            # Calcul des retards de paiement
            self.df['delai_paiement'] = (self.df['date_paiement'] - self.df['date_soin']).dt.days
            retards = self.df[self.df['delai_paiement'] > 30]
            
            print(f"\n⏰ PAIEMENTS EN RETARD (>30 jours): {len(retards)}")
            print(f"💰 Montant total en retard: {retards['montant'].sum():.2f}")
            print(f"📊 % de paiements en retard: {(len(retards)/len(self.df)*100):.1f}%")
            
            if len(retards) > 0:
                print(f"⏱️ Délai moyen de paiement: {self.df['delai_paiement'].mean():.1f} jours")
                
                # Analyse par type de soin
                retards_par_soin = retards.groupby('type_soin')['montant'].sum().sort_values(ascending=False)
                print("\n🦷 RETARDS PAR TYPE DE SOIN:")
                print(retards_par_soin.head(10))
    
    def analyse_geographique(self):
        """🏥 5. Analyse géographique"""
        print("\n" + "="*50)
        print("🏥 ANALYSE 5: GÉOGRAPHIE")
        print("="*50)
        
        # CA par clinique
        if 'clinique' in self.df.columns:
            ca_clinique = self.df.groupby('clinique')['montant'].agg(['sum', 'count']).round(2)
            ca_clinique.columns = ['CA_Total', 'Nombre_Actes']
            ca_clinique['CA_Moyen'] = (ca_clinique['CA_Total'] / ca_clinique['Nombre_Actes']).round(2)
            
            print("\n🏥 CA PAR CLINIQUE:")
            print(ca_clinique.sort_values('CA_Total', ascending=False))
        
        # Patients uniques par région
        if 'region' in self.df.columns and 'patient_id' in self.df.columns:
            patients_region = self.df.groupby('region')['patient_id'].nunique()
            print("\n👥 PATIENTS UNIQUES PAR RÉGION:")
            print(patients_region.sort_values(ascending=False))
    
    def analyse_temporelle(self):
        """📅 6. Analyse temporelle"""
        print("\n" + "="*50)
        print("📅 ANALYSE 6: TEMPORELLE")
        print("="*50)
        
        if 'date_soin' in self.df.columns:
            # CA par mois
            self.df['mois'] = self.df['date_soin'].dt.to_period('M')
            ca_mensuel = self.df.groupby('mois')['montant'].sum()
            
            print("\n📈 CA MENSUEL:")
            print(ca_mensuel.round(2))
            
            # Patients par mois
            patients_mensuel = self.df.groupby('mois')['patient_id'].nunique()
            print("\n👥 NOUVEAUX PATIENTS PAR MOIS:")
            print(patients_mensuel)
            
            # Saisonnalité
            self.df['mois_num'] = self.df['date_soin'].dt.month
            saisonnalite = self.df.groupby('mois_num')['montant'].sum()
            print("\n🌤️ SAISONNALITÉ (CA par mois):")
            print(saisonnalite.round(2))
    
    def generer_rapport_complet(self):
        """Génère un rapport complet de toutes les analyses"""
        print("🚀 DÉBUT DE L'ANALYSE COMPLÈTE")
        print("="*60)
        
        # Exécution de toutes les analyses
        self.analyse_performance_soins()
        self.analyse_praticiens()
        self.analyse_patients()
        self.analyse_paiements()
        self.analyse_geographique()
        self.analyse_temporelle()
        
        print("\n" + "="*60)
        print("✅ ANALYSE TERMINÉE")
        print("="*60)

# Exécution de l'analyse
if __name__ == "__main__":
    try:
        analyse = AnalyseDentaire()
        analyse.generer_rapport_complet()
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        print("🔍 Vérifiez que le fichier 'patients_mis_a_jour.xlsx' est présent dans le répertoire") 