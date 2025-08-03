#!/usr/bin/env python3
"""
Visualisations graphiques des KPIs d'un cabinet dentaire multi-sites
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

class VisualisationsDentaire:
    def __init__(self, fichier_donnees="patients_mis_a_jour.xlsx"):
        """Initialisation des visualisations"""
        print("🦷 Chargement des données pour visualisations...")
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
    
    def visualiser_performance_soins(self):
        """🦷 Visualisations - Performance des soins"""
        print("📊 Génération des graphiques - Performance des soins...")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('🦷 PERFORMANCE DES SOINS', fontsize=16, fontweight='bold')
        
        # 1. Top 10 soins par CA
        if 'type_soin' in self.df.columns and 'montant' in self.df.columns:
            top_soins = self.df.groupby('type_soin')['montant'].sum().sort_values(ascending=False).head(10)
            
            axes[0, 0].barh(range(len(top_soins)), top_soins.values)
            axes[0, 0].set_yticks(range(len(top_soins)))
            axes[0, 0].set_yticklabels(top_soins.index, fontsize=8)
            axes[0, 0].set_title('Top 10 Soins par Chiffre d\'Affaires')
            axes[0, 0].set_xlabel('Chiffre d\'Affaires (CHF)')
            
            # 2. Distribution des montants par soin
            axes[0, 1].hist(self.df['montant'], bins=30, alpha=0.7, edgecolor='black')
            axes[0, 1].set_title('Distribution des Montants')
            axes[0, 1].set_xlabel('Montant (CHF)')
            axes[0, 1].set_ylabel('Fréquence')
            
            # 3. Nombre d'actes par soin
            actes_par_soin = self.df.groupby('type_soin').size().sort_values(ascending=False).head(10)
            axes[1, 0].bar(range(len(actes_par_soin)), actes_par_soin.values)
            axes[1, 0].set_xticks(range(len(actes_par_soin)))
            axes[1, 0].set_xticklabels(actes_par_soin.index, rotation=45, ha='right', fontsize=8)
            axes[1, 0].set_title('Nombre d\'Actes par Type de Soin')
            axes[1, 0].set_ylabel('Nombre d\'Actes')
            
            # 4. CA moyen par soin
            ca_moyen = self.df.groupby('type_soin')['montant'].mean().sort_values(ascending=False).head(10)
            axes[1, 1].bar(range(len(ca_moyen)), ca_moyen.values)
            axes[1, 1].set_xticks(range(len(ca_moyen)))
            axes[1, 1].set_xticklabels(ca_moyen.index, rotation=45, ha='right', fontsize=8)
            axes[1, 1].set_title('CA Moyen par Type de Soin')
            axes[1, 1].set_ylabel('CA Moyen (CHF)')
        
        plt.tight_layout()
        plt.savefig('performance_soins.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def visualiser_praticiens(self):
        """👨‍⚕️ Visualisations - Praticiens"""
        print("📊 Génération des graphiques - Praticiens...")
        
        if 'praticien' in self.df.columns and 'montant' in self.df.columns:
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle('👨‍⚕️ ANALYSE DES PRATICIENS', fontsize=16, fontweight='bold')
            
            # 1. CA par praticien
            ca_praticien = self.df.groupby('praticien')['montant'].sum().sort_values(ascending=False)
            axes[0, 0].bar(range(len(ca_praticien)), ca_praticien.values)
            axes[0, 0].set_xticks(range(len(ca_praticien)))
            axes[0, 0].set_xticklabels(ca_praticien.index, rotation=45, ha='right')
            axes[0, 0].set_title('CA Total par Praticien')
            axes[0, 0].set_ylabel('CA (CHF)')
            
            # 2. Nombre d'actes par praticien
            actes_praticien = self.df.groupby('praticien').size().sort_values(ascending=False)
            axes[0, 1].bar(range(len(actes_praticien)), actes_praticien.values)
            axes[0, 1].set_xticks(range(len(actes_praticien)))
            axes[0, 1].set_xticklabels(actes_praticien.index, rotation=45, ha='right')
            axes[0, 1].set_title('Nombre d\'Actes par Praticien')
            axes[0, 1].set_ylabel('Nombre d\'Actes')
            
            # 3. CA moyen par acte par praticien
            ca_moyen_praticien = self.df.groupby('praticien')['montant'].mean().sort_values(ascending=False)
            axes[1, 0].bar(range(len(ca_moyen_praticien)), ca_moyen_praticien.values)
            axes[1, 0].set_xticks(range(len(ca_moyen_praticien)))
            axes[1, 0].set_xticklabels(ca_moyen_praticien.index, rotation=45, ha='right')
            axes[1, 0].set_title('CA Moyen par Acte par Praticien')
            axes[1, 0].set_ylabel('CA Moyen (CHF)')
            
            # 4. Distribution des montants par praticien
            axes[1, 1].boxplot([self.df[self.df['praticien'] == p]['montant'] for p in self.df['praticien'].unique()])
            axes[1, 1].set_xticklabels(self.df['praticien'].unique(), rotation=45, ha='right')
            axes[1, 1].set_title('Distribution des Montants par Praticien')
            axes[1, 1].set_ylabel('Montant (CHF)')
            
            plt.tight_layout()
            plt.savefig('analyse_praticiens.png', dpi=300, bbox_inches='tight')
            plt.show()
    
    def visualiser_patients(self):
        """🧑‍🤝‍🧑 Visualisations - Patients"""
        print("📊 Génération des graphiques - Patients...")
        
        if 'patient_id' in self.df.columns:
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle('🧑‍🤝‍🧑 ANALYSE DES PATIENTS', fontsize=16, fontweight='bold')
            
            # 1. Distribution du nombre de visites par patient
            visites_par_patient = self.df.groupby('patient_id').size()
            axes[0, 0].hist(visites_par_patient, bins=20, alpha=0.7, edgecolor='black')
            axes[0, 0].set_title('Distribution du Nombre de Visites par Patient')
            axes[0, 0].set_xlabel('Nombre de Visites')
            axes[0, 0].set_ylabel('Nombre de Patients')
            
            # 2. Montant total par patient
            montant_par_patient = self.df.groupby('patient_id')['montant'].sum()
            axes[0, 1].hist(montant_par_patient, bins=30, alpha=0.7, edgecolor='black')
            axes[0, 1].set_title('Distribution du Montant Total par Patient')
            axes[0, 1].set_xlabel('Montant Total (CHF)')
            axes[0, 1].set_ylabel('Nombre de Patients')
            
            # 3. Analyse RFM si date disponible
            if 'date_soin' in self.df.columns:
                rfm = self.df.groupby('patient_id').agg({
                    'date_soin': lambda x: (pd.Timestamp.now() - x.max()).days,
                    'patient_id': 'count',
                    'montant': 'sum'
                }).rename(columns={'date_soin': 'recence', 'patient_id': 'frequence', 'montant': 'montant'})
                
                # Scatter plot Récence vs Fréquence
                axes[1, 0].scatter(rfm['recence'], rfm['frequence'], alpha=0.6)
                axes[1, 0].set_title('Récence vs Fréquence')
                axes[1, 0].set_xlabel('Récence (jours)')
                axes[1, 0].set_ylabel('Fréquence (nombre de visites)')
                
                # Scatter plot Fréquence vs Montant
                axes[1, 1].scatter(rfm['frequence'], rfm['montant'], alpha=0.6)
                axes[1, 1].set_title('Fréquence vs Montant')
                axes[1, 1].set_xlabel('Fréquence (nombre de visites)')
                axes[1, 1].set_ylabel('Montant Total (CHF)')
            
            plt.tight_layout()
            plt.savefig('analyse_patients.png', dpi=300, bbox_inches='tight')
            plt.show()
    
    def visualiser_paiements(self):
        """💰 Visualisations - Paiements"""
        print("📊 Génération des graphiques - Paiements...")
        
        if 'date_paiement' in self.df.columns and 'date_soin' in self.df.columns:
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle('💰 ANALYSE DES PAIEMENTS', fontsize=16, fontweight='bold')
            
            # Calcul des délais de paiement
            self.df['delai_paiement'] = (self.df['date_paiement'] - self.df['date_soin']).dt.days
            
            # 1. Distribution des délais de paiement
            axes[0, 0].hist(self.df['delai_paiement'], bins=30, alpha=0.7, edgecolor='black')
            axes[0, 0].axvline(x=30, color='red', linestyle='--', label='Seuil 30 jours')
            axes[0, 0].set_title('Distribution des Délais de Paiement')
            axes[0, 0].set_xlabel('Délai (jours)')
            axes[0, 0].set_ylabel('Nombre de Paiements')
            axes[0, 0].legend()
            
            # 2. Montants en retard
            retards = self.df[self.df['delai_paiement'] > 30]
            if len(retards) > 0:
                axes[0, 1].hist(retards['montant'], bins=20, alpha=0.7, edgecolor='black', color='red')
                axes[0, 1].set_title('Distribution des Montants en Retard')
                axes[0, 1].set_xlabel('Montant (CHF)')
                axes[0, 1].set_ylabel('Nombre de Paiements')
            
            # 3. Retards par type de soin
            if 'type_soin' in self.df.columns and len(retards) > 0:
                retards_par_soin = retards.groupby('type_soin')['montant'].sum().sort_values(ascending=False).head(10)
                axes[1, 0].bar(range(len(retards_par_soin)), retards_par_soin.values, color='red')
                axes[1, 0].set_xticks(range(len(retards_par_soin)))
                axes[1, 0].set_xticklabels(retards_par_soin.index, rotation=45, ha='right')
                axes[1, 0].set_title('Montants en Retard par Type de Soin')
                axes[1, 0].set_ylabel('Montant en Retard (CHF)')
            
            # 4. Évolution des retards dans le temps
            if 'date_soin' in self.df.columns:
                retards_temporel = retards.groupby(retards['date_soin'].dt.to_period('M')).size()
                axes[1, 1].plot(range(len(retards_temporel)), retards_temporel.values, marker='o')
                axes[1, 1].set_title('Évolution des Paiements en Retard')
                axes[1, 1].set_xlabel('Mois')
                axes[1, 1].set_ylabel('Nombre de Paiements en Retard')
            
            plt.tight_layout()
            plt.savefig('analyse_paiements.png', dpi=300, bbox_inches='tight')
            plt.show()
    
    def visualiser_geographie(self):
        """🏥 Visualisations - Géographie"""
        print("📊 Génération des graphiques - Géographie...")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('🏥 ANALYSE GÉOGRAPHIQUE', fontsize=16, fontweight='bold')
        
        # 1. CA par clinique
        if 'clinique' in self.df.columns:
            ca_clinique = self.df.groupby('clinique')['montant'].sum().sort_values(ascending=False)
            axes[0, 0].bar(range(len(ca_clinique)), ca_clinique.values)
            axes[0, 0].set_xticks(range(len(ca_clinique)))
            axes[0, 0].set_xticklabels(ca_clinique.index, rotation=45, ha='right')
            axes[0, 0].set_title('CA par Clinique')
            axes[0, 0].set_ylabel('CA (CHF)')
        
        # 2. Patients par région
        if 'region' in self.df.columns and 'patient_id' in self.df.columns:
            patients_region = self.df.groupby('region')['patient_id'].nunique().sort_values(ascending=False)
            axes[0, 1].bar(range(len(patients_region)), patients_region.values)
            axes[0, 1].set_xticks(range(len(patients_region)))
            axes[0, 1].set_xticklabels(patients_region.index, rotation=45, ha='right')
            axes[0, 1].set_title('Nombre de Patients par Région')
            axes[0, 1].set_ylabel('Nombre de Patients')
        
        # 3. CA moyen par région
        if 'region' in self.df.columns:
            ca_moyen_region = self.df.groupby('region')['montant'].mean().sort_values(ascending=False)
            axes[1, 0].bar(range(len(ca_moyen_region)), ca_moyen_region.values)
            axes[1, 0].set_xticks(range(len(ca_moyen_region)))
            axes[1, 0].set_xticklabels(ca_moyen_region.index, rotation=45, ha='right')
            axes[1, 0].set_title('CA Moyen par Région')
            axes[1, 0].set_ylabel('CA Moyen (CHF)')
        
        # 4. Distribution géographique des soins
        if 'region' in self.df.columns and 'type_soin' in self.df.columns:
            soins_region = self.df.groupby(['region', 'type_soin']).size().unstack(fill_value=0)
            soins_region.plot(kind='bar', ax=axes[1, 1], stacked=True)
            axes[1, 1].set_title('Répartition des Soins par Région')
            axes[1, 1].set_xlabel('Région')
            axes[1, 1].set_ylabel('Nombre de Soins')
            axes[1, 1].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        plt.savefig('analyse_geographie.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def visualiser_temporel(self):
        """📅 Visualisations - Temporel"""
        print("📊 Génération des graphiques - Analyse temporelle...")
        
        if 'date_soin' in self.df.columns:
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle('📅 ANALYSE TEMPORELLE', fontsize=16, fontweight='bold')
            
            # 1. CA mensuel
            self.df['mois'] = self.df['date_soin'].dt.to_period('M')
            ca_mensuel = self.df.groupby('mois')['montant'].sum()
            axes[0, 0].plot(range(len(ca_mensuel)), ca_mensuel.values, marker='o', linewidth=2)
            axes[0, 0].set_title('Évolution du CA Mensuel')
            axes[0, 0].set_xlabel('Mois')
            axes[0, 0].set_ylabel('CA (CHF)')
            axes[0, 0].grid(True, alpha=0.3)
            
            # 2. Patients par mois
            patients_mensuel = self.df.groupby('mois')['patient_id'].nunique()
            axes[0, 1].plot(range(len(patients_mensuel)), patients_mensuel.values, marker='s', linewidth=2, color='orange')
            axes[0, 1].set_title('Évolution du Nombre de Patients')
            axes[0, 1].set_xlabel('Mois')
            axes[0, 1].set_ylabel('Nombre de Patients')
            axes[0, 1].grid(True, alpha=0.3)
            
            # 3. Saisonnalité
            self.df['mois_num'] = self.df['date_soin'].dt.month
            saisonnalite = self.df.groupby('mois_num')['montant'].sum()
            axes[1, 0].bar(saisonnalite.index, saisonnalite.values)
            axes[1, 0].set_title('Saisonnalité - CA par Mois')
            axes[1, 0].set_xlabel('Mois')
            axes[1, 0].set_ylabel('CA (CHF)')
            axes[1, 0].set_xticks(range(1, 13))
            
            # 4. Répartition des soins par jour de la semaine
            self.df['jour_semaine'] = self.df['date_soin'].dt.day_name()
            soins_jour = self.df.groupby('jour_semaine').size()
            axes[1, 1].bar(range(len(soins_jour)), soins_jour.values)
            axes[1, 1].set_xticks(range(len(soins_jour)))
            axes[1, 1].set_xticklabels(soins_jour.index, rotation=45)
            axes[1, 1].set_title('Répartition des Soins par Jour de la Semaine')
            axes[1, 1].set_ylabel('Nombre de Soins')
            
            plt.tight_layout()
            plt.savefig('analyse_temporelle.png', dpi=300, bbox_inches='tight')
            plt.show()
    
    def generer_toutes_visualisations(self):
        """Génère toutes les visualisations"""
        print("🚀 DÉBUT DE LA GÉNÉRATION DES VISUALISATIONS")
        print("="*60)
        
        try:
            self.visualiser_performance_soins()
            self.visualiser_praticiens()
            self.visualiser_patients()
            self.visualiser_paiements()
            self.visualiser_geographie()
            self.visualiser_temporel()
            
            print("\n" + "="*60)
            print("✅ TOUTES LES VISUALISATIONS ONT ÉTÉ GÉNÉRÉES")
            print("📁 Les fichiers PNG ont été sauvegardés dans le répertoire courant")
            print("="*60)
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération des visualisations: {e}")

# Exécution des visualisations
if __name__ == "__main__":
    try:
        visu = VisualisationsDentaire()
        visu.generer_toutes_visualisations()
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        print("🔍 Vérifiez que le fichier 'patients_mis_a_jour.xlsx' est présent dans le répertoire") 