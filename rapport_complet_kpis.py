#!/usr/bin/env python3
"""
Rapport complet des KPIs d'un cabinet dentaire multi-sites
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
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

class RapportCompletDentaire:
    def __init__(self, fichier_donnees="patients_mis_a_jour.xlsx"):
        """Initialisation du rapport complet"""
        print("🦷 CHARGEMENT DES DONNÉES DENTAIRES")
        print("="*60)
        
        try:
            self.df = pd.read_excel(fichier_donnees)
            print(f"✅ Données chargées: {self.df.shape[0]} lignes, {self.df.shape[1]} colonnes")
            print(f"📊 Colonnes disponibles: {list(self.df.columns)}")
            
            # Nettoyage initial
            self.nettoyer_donnees()
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {e}")
            raise
    
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
        
        print("✅ Nettoyage terminé")
    
    def explorer_donnees(self):
        """Exploration initiale des données"""
        print("\n🔍 EXPLORATION DES DONNÉES")
        print("="*40)
        
        print(f"📊 Forme du dataset: {self.df.shape}")
        print(f"📅 Période couverte: {self.df.select_dtypes(include=['datetime64']).columns.tolist()}")
        print(f"💰 Colonnes numériques: {self.df.select_dtypes(include=[np.number]).columns.tolist()}")
        print(f"📝 Colonnes catégorielles: {self.df.select_dtypes(include=['object']).columns.tolist()}")
        
        # Statistiques descriptives
        if 'montant_total_chf' in self.df.columns:
            print(f"\n💰 STATISTIQUES MONÉTAIRES:")
            print(f"   CA total: {self.df['montant_total_chf'].sum():,.2f} CHF")
            print(f"   CA moyen: {self.df['montant_total_chf'].mean():.2f} CHF")
            print(f"   CA médian: {self.df['montant_total_chf'].median():.2f} CHF")
            print(f"   Écart-type: {self.df['montant_total_chf'].std():.2f} CHF")
    
    def kpi_performance_soins(self):
        """🦷 KPIs - Performance des soins"""
        print("\n" + "="*60)
        print("🦷 KPI 1: PERFORMANCE DES SOINS")
        print("="*60)
        
        if 'type_de_soin' in self.df.columns and 'montant_total_chf' in self.df.columns:
            # Top 10 soins par CA
            top_soins = self.df.groupby('type_de_soin')['montant_total_chf'].agg(['sum', 'count', 'mean']).round(2)
            top_soins.columns = ['CA_Total', 'Nombre_Actes', 'CA_Moyen']
            top_soins = top_soins.sort_values('CA_Total', ascending=False)
            
            print("\n📊 TOP 10 SOINS PAR CHIFFRE D'AFFAIRES:")
            print(top_soins.head(10).to_string())
            
            # Rentabilité par minute (si durée disponible)
            if 'durée_minutes' in self.df.columns:
                rentabilite_minute = self.df.groupby('type_de_soin').apply(
                    lambda x: (x['montant_total_chf'].sum() / x['durée_minutes'].sum()) if x['durée_minutes'].sum() > 0 else 0
                ).round(2)
                print("\n⏱️ RENTABILITÉ PAR MINUTE (TOP 10):")
                print(rentabilite_minute.sort_values(ascending=False).head(10).to_string())
        
        # Nombre moyen de soins par patient
        if 'patientid' in self.df.columns:
            soins_par_patient = self.df.groupby('patientid').size()
            print(f"\n👥 STATISTIQUES SOINS PAR PATIENT:")
            print(f"   Moyenne: {soins_par_patient.mean():.2f}")
            print(f"   Médiane: {soins_par_patient.median():.0f}")
            print(f"   Maximum: {soins_par_patient.max()}")
            print(f"   Écart-type: {soins_par_patient.std():.2f}")
    
    def kpi_praticiens(self):
        """👨‍⚕️ KPIs - Praticiens"""
        print("\n" + "="*60)
        print("👨‍⚕️ KPI 2: PRATICIENS")
        print("="*60)
        
        if 'dentiste' in self.df.columns and 'montant_total_chf' in self.df.columns:
            # CA par praticien
            ca_praticien = self.df.groupby('dentiste')['montant_total_chf'].agg(['sum', 'count', 'mean']).round(2)
            ca_praticien.columns = ['CA_Total', 'Nombre_Actes', 'CA_Moyen']
            ca_praticien = ca_praticien.sort_values('CA_Total', ascending=False)
            
            print("\n💰 PERFORMANCE PAR PRATICIEN:")
            print(ca_praticien.to_string())
            
            # Taux de fidélisation
            if 'patientid' in self.df.columns:
                fidelisation = self.df.groupby(['dentiste', 'patientid']).size().reset_index()
                fidelisation = fidelisation.groupby('dentiste').apply(
                    lambda x: (x[x[0] > 1].shape[0] / x.shape[0]) * 100
                ).round(2)
                
                print("\n👥 TAUX DE FIDÉLISATION PAR PRATICIEN (%):")
                print(fidelisation.sort_values(ascending=False).to_string())
    
    def kpi_patients(self):
        """🧑‍🤝‍🧑 KPIs - Patients"""
        print("\n" + "="*60)
        print("🧑‍🤝‍🧑 KPI 3: PATIENTS")
        print("="*60)
        
        if 'patientid' in self.df.columns:
            # Taux de rétention
            visites_par_patient = self.df.groupby('patientid').size()
            patients_fideles = (visites_par_patient > 1).sum()
            taux_retention = (patients_fideles / len(visites_par_patient)) * 100
            
            print(f"\n📊 FIDÉLISATION DES PATIENTS:")
            print(f"   Taux de rétention: {taux_retention:.1f}%")
            print(f"   Patients fidèles (2+ visites): {patients_fideles}")
            print(f"   Total patients: {len(visites_par_patient)}")
            print(f"   Patients uniques: {self.df['patientid'].nunique()}")
            
            # Analyse RFM
            if 'date_du_soin' in self.df.columns:
                self.analyse_rfm()
    
    def analyse_rfm(self):
        """Analyse RFM (Récence, Fréquence, Montant)"""
        print("\n📊 ANALYSE RFM (Récence, Fréquence, Montant):")
        
        # Calcul RFM
        rfm = self.df.groupby('patientid').agg({
            'date_du_soin': lambda x: (pd.Timestamp.now() - x.max()).days,  # Récence
            'patientid': 'count',  # Fréquence
            'montant_total_chf': 'sum'  # Montant
        }).rename(columns={'date_du_soin': 'recence', 'patientid': 'frequence', 'montant_total_chf': 'montant'})
        
        # Segmentation RFM avec gestion des doublons
        try:
            rfm['R'] = pd.qcut(rfm['recence'], q=4, labels=['4', '3', '2', '1'], duplicates='drop')
            rfm['F'] = pd.qcut(rfm['frequence'], q=4, labels=['1', '2', '3', '4'], duplicates='drop')
            rfm['M'] = pd.qcut(rfm['montant'], q=4, labels=['1', '2', '3', '4'], duplicates='drop')
            
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
            print(rfm['Segment'].value_counts().to_string())
            
            print("\n💰 MONTANT MOYEN PAR SEGMENT:")
            print(rfm.groupby('Segment')['montant'].mean().round(2).to_string())
            
        except Exception as e:
            print(f"⚠️ Erreur dans l'analyse RFM: {e}")
            print("📊 Statistiques RFM de base:")
            print(f"   Récence moyenne: {rfm['recence'].mean():.1f} jours")
            print(f"   Fréquence moyenne: {rfm['frequence'].mean():.2f} visites")
            print(f"   Montant moyen: {rfm['montant'].mean():.2f} CHF")
    
    def kpi_paiements(self):
        """💰 KPIs - Paiements et créances"""
        print("\n" + "="*60)
        print("💰 KPI 4: PAIEMENTS ET CRÉANCES")
        print("="*60)
        
        if 'montant_payé_chf' in self.df.columns and 'montant_total_chf' in self.df.columns:
            # Calcul des montants en retard
            self.df['montant_impayé'] = self.df['montant_total_chf'] - self.df['montant_payé_chf']
            retards = self.df[self.df['montant_impayé'] > 0]
            
            print(f"\n⏰ ANALYSE DES IMPAYÉS:")
            print(f"   Paiements en retard: {len(retards)}")
            print(f"   Montant total en retard: {retards['montant_impayé'].sum():,.2f} CHF")
            print(f"   % de paiements en retard: {(len(retards)/len(self.df)*100):.1f}%")
            print(f"   Montant moyen impayé: {retards['montant_impayé'].mean():.2f} CHF")
            
            if len(retards) > 0:
                # Analyse par type de soin
                retards_par_soin = retards.groupby('type_de_soin')['montant_impayé'].sum().sort_values(ascending=False)
                print("\n🦷 IMPAYÉS PAR TYPE DE SOIN (TOP 10):")
                print(retards_par_soin.head(10).to_string())
    
    def kpi_geographie(self):
        """🏥 KPIs - Analyse géographique"""
        print("\n" + "="*60)
        print("🏥 KPI 5: ANALYSE GÉOGRAPHIQUE")
        print("="*60)
        
        # CA par clinique
        if 'nom_de_la_clinique' in self.df.columns:
            ca_clinique = self.df.groupby('nom_de_la_clinique')['montant_total_chf'].agg(['sum', 'count']).round(2)
            ca_clinique.columns = ['CA_Total', 'Nombre_Actes']
            ca_clinique['CA_Moyen'] = (ca_clinique['CA_Total'] / ca_clinique['Nombre_Actes']).round(2)
            
            print("\n🏥 PERFORMANCE PAR CLINIQUE:")
            print(ca_clinique.sort_values('CA_Total', ascending=False).to_string())
        
        # Patients uniques par canton
        if 'canton_clinique' in self.df.columns and 'patientid' in self.df.columns:
            patients_canton = self.df.groupby('canton_clinique')['patientid'].nunique()
            print("\n👥 PATIENTS UNIQUES PAR CANTON:")
            print(patients_canton.sort_values(ascending=False).to_string())
    
    def kpi_temporel(self):
        """📅 KPIs - Analyse temporelle"""
        print("\n" + "="*60)
        print("📅 KPI 6: ANALYSE TEMPORELLE")
        print("="*60)
        
        if 'date_du_soin' in self.df.columns:
            # CA par mois
            self.df['mois'] = self.df['date_du_soin'].dt.to_period('M')
            ca_mensuel = self.df.groupby('mois')['montant_total_chf'].sum()
            
            print("\n📈 CA MENSUEL:")
            print(ca_mensuel.round(2).to_string())
            
            # Patients par mois
            patients_mensuel = self.df.groupby('mois')['patientid'].nunique()
            print("\n👥 NOUVEAUX PATIENTS PAR MOIS:")
            print(patients_mensuel.to_string())
            
            # Saisonnalité
            self.df['mois_num'] = self.df['date_du_soin'].dt.month
            saisonnalite = self.df.groupby('mois_num')['montant_total_chf'].sum()
            print("\n🌤️ SAISONNALITÉ (CA par mois):")
            print(saisonnalite.round(2).to_string())
    
    def generer_rapport_complet(self):
        """Génère un rapport complet de toutes les analyses"""
        print("\n🚀 DÉBUT DU RAPPORT COMPLET")
        print("="*80)
        
        # Exploration des données
        self.explorer_donnees()
        
        # Exécution de tous les KPIs
        self.kpi_performance_soins()
        self.kpi_praticiens()
        self.kpi_patients()
        self.kpi_paiements()
        self.kpi_geographie()
        self.kpi_temporel()
        
        print("\n" + "="*80)
        print("✅ RAPPORT COMPLET TERMINÉ")
        print("="*80)
        
        # Résumé des insights clés
        self.resume_insights()
    
    def resume_insights(self):
        """Résumé des insights clés"""
        print("\n🎯 INSIGHTS CLÉS:")
        print("="*40)
        
        if 'montant_total_chf' in self.df.columns:
            ca_total = self.df['montant_total_chf'].sum()
            ca_moyen = self.df['montant_total_chf'].mean()
            print(f"💰 CA total: {ca_total:,.2f} CHF")
            print(f"💰 CA moyen par acte: {ca_moyen:.2f} CHF")
        
        if 'patientid' in self.df.columns:
            nb_patients = self.df['patientid'].nunique()
            print(f"👥 Nombre de patients uniques: {nb_patients}")
        
        if 'dentiste' in self.df.columns:
            nb_praticiens = self.df['dentiste'].nunique()
            print(f"👨‍⚕️ Nombre de praticiens: {nb_praticiens}")
        
        if 'nom_de_la_clinique' in self.df.columns:
            nb_cliniques = self.df['nom_de_la_clinique'].nunique()
            print(f"🏥 Nombre de cliniques: {nb_cliniques}")

# Exécution du rapport complet
if __name__ == "__main__":
    try:
        rapport = RapportCompletDentaire()
        rapport.generer_rapport_complet()
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        print("🔍 Vérifiez que le fichier 'patients_mis_a_jour.xlsx' est présent dans le répertoire") 