#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import seaborn as sns

# Configuration de la page
st.set_page_config(
    page_title="Audit Analytique Cabinet Dentaire",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre principal
st.title("🦷 Audit Analytique d'un Cabinet Dentaire Multi-Sites")
st.markdown("---")

# Fonction pour charger les données
@st.cache_data
def load_data():
    """Charger les données réelles du fichier Excel"""
    try:
        df = pd.read_excel("data/patients_mis_a_jour.xlsx")
        st.sidebar.success("✅ Données réelles chargées")
        
        # Conversion de la date
        df['date_du_soin'] = pd.to_datetime(df['date_du_soin'], errors='coerce')
        # Création des colonnes temporelles
        df['Annee'] = df['date_du_soin'].dt.year
        df['Mois'] = df['date_du_soin'].dt.month
        df['Année-Mois'] = df['Annee'].astype(str) + '-' + df['Mois'].astype(str).str.zfill(2)
        
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données : {e}")
        return None

# Chargement des données
with st.spinner("Chargement des données..."):
    df = load_data()

if df is None:
    st.error("Impossible de charger les données. Vérifiez que le fichier 'data/patients_mis_a_jour.xlsx' existe.")
    st.stop()

# Sidebar pour la navigation et les filtres
st.sidebar.title("📊 Navigation et Filtres")

# Sélecteur de cabinet
st.sidebar.subheader("🏥 Sélection du Cabinet")
all_cabinets = ["Tous les cabinets"] + sorted(df['cabinet'].unique().tolist())
selected_cabinet = st.sidebar.selectbox(
    "Choisissez un cabinet :",
    all_cabinets,
    index=0
)

# Filtrer les données selon le cabinet sélectionné
if selected_cabinet == "Tous les cabinets":
    df_filtered = df.copy()
    st.sidebar.info(f"📊 Données affichées : Tous les cabinets ({len(df_filtered)} enregistrements)")
else:
    df_filtered = df[df['cabinet'] == selected_cabinet].copy()
    st.sidebar.info(f"📊 Données affichées : {selected_cabinet} ({len(df_filtered)} enregistrements)")

# Navigation
page = st.sidebar.selectbox(
    "Choisissez une section :",
    [
        "🏠 Dashboard Général",
        "🦷 Performance des Soins",
        "👨‍⚕️ Analyse des Praticiens", 
        "🧑‍🤝‍🧑 Analyse des Patients",
        "💰 Paiements et Créances",
        "🏥 Analyse Géographique",
        "📅 Analyse Temporelle"
    ]
)

# Métriques générales
def show_general_metrics():
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Patients", f"{df_filtered['patientid'].nunique():,}")
    
    with col2:
        st.metric("Total Soins", f"{len(df_filtered):,}")
    
    with col3:
        st.metric("CA Total", f"{df_filtered['montant_total_chf'].sum():,.0f} CHF")
    
    with col4:
        st.metric("CA Moyen/Soin", f"{df_filtered['montant_total_chf'].mean():.0f} CHF")

# Dashboard Général
if page == "🏠 Dashboard Général":
    st.header("🏠 Dashboard Général")
    
    # Afficher le cabinet sélectionné
    if selected_cabinet != "Tous les cabinets":
        st.info(f"📊 Analyses pour le cabinet : **{selected_cabinet}**")
    
    show_general_metrics()
    
    # Graphiques principaux
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Évolution du CA mensuel")
        ca_mensuel = df_filtered.groupby('Année-Mois')['montant_total_chf'].sum()
        if len(ca_mensuel) > 0:
            fig = px.line(ca_mensuel, title="CA par mois")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Pas assez de données pour afficher l'évolution du CA")
    
    with col2:
        st.subheader("🦷 Top 10 Soins par CA")
        top_soins = df_filtered.groupby('type_de_soin_normalisé')['montant_total_chf'].sum().sort_values(ascending=False).head(10)
        if len(top_soins) > 0:
            fig = px.bar(x=top_soins.values, y=top_soins.index, orientation='h', title="Top 10 soins par chiffre d'affaires")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Pas assez de données pour afficher les soins")

# Performance des Soins
elif page == "🦷 Performance des Soins":
    st.header("🦷 Performance des Soins")
    
    if selected_cabinet != "Tous les cabinets":
        st.info(f"📊 Analyses pour le cabinet : **{selected_cabinet}**")
    
    # Top 10 soins par CA
    st.subheader("1. Top 10 soins par chiffre d'affaires")
    top_10_ca_soins = df_filtered.groupby('type_de_soin_normalisé')['montant_total_chf'].sum().sort_values(ascending=False).head(10)
    
    if len(top_10_ca_soins) > 0:
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(top_10_ca_soins.reset_index().rename(columns={'type_de_soin_normalisé': 'Type de Soin', 'montant_total_chf': 'CA Total (CHF)'}))
        
        with col2:
            fig = px.bar(x=top_10_ca_soins.values, y=top_10_ca_soins.index, orientation='h', title="Top 10 soins par CA")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Pas assez de données pour cette analyse")
    
    # Rentabilité moyenne par soin
    st.subheader("2. Rentabilité moyenne par soin")
    rentabilite_soins = df_filtered.groupby('type_de_soin_normalisé').agg({
        'montant_total_chf': 'sum',
        'type_de_soin_normalisé': 'count'
    }).rename(columns={'type_de_soin_normalisé': 'Nombre_actes'})
    
    if len(rentabilite_soins) > 0:
        rentabilite_soins['Rentabilite_moyenne'] = rentabilite_soins['montant_total_chf'] / rentabilite_soins['Nombre_actes']
        rentabilite_soins = rentabilite_soins.sort_values('Rentabilite_moyenne', ascending=False)
        
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(rentabilite_soins.head(10).reset_index().rename(columns={
                'type_de_soin_normalisé': 'Type de Soin',
                'montant_total_chf': 'CA Total',
                'Nombre_actes': 'Nombre d\'actes',
                'Rentabilite_moyenne': 'Rentabilité moyenne'
            }))
        
        with col2:
            fig = px.bar(x=rentabilite_soins.head(15)['Rentabilite_moyenne'], y=rentabilite_soins.head(15).index, orientation='h', title="Rentabilité moyenne par type de soin")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Pas assez de données pour cette analyse")
    
    # Nombre moyen de soins par patient
    st.subheader("3. Nombre moyen de soins par patient")
    soins_par_patient = df_filtered.groupby('patientid')['type_de_soin_normalisé'].count()
    
    if len(soins_par_patient) > 0:
        moyenne_soins_patient = soins_par_patient.mean()
        median_soins_patient = soins_par_patient.median()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Moyenne", f"{moyenne_soins_patient:.2f}")
        with col2:
            st.metric("Médiane", f"{median_soins_patient:.2f}")
        with col3:
            st.metric("Écart-type", f"{soins_par_patient.std():.2f}")
        
        # Distribution
        fig = px.histogram(x=soins_par_patient.values, nbins=30, title="Distribution du nombre de soins par patient")
        fig.add_vline(x=moyenne_soins_patient, line_dash="dash", line_color="red", annotation_text=f"Moyenne: {moyenne_soins_patient:.2f}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Pas assez de données pour cette analyse")

# Analyse des Praticiens
elif page == "👨‍⚕️ Analyse des Praticiens":
    st.header("👨‍⚕️ Analyse des Praticiens")
    
    if selected_cabinet != "Tous les cabinets":
        st.info(f"📊 Analyses pour le cabinet : **{selected_cabinet}**")
    
    if 'nom_complet_praticien' in df_filtered.columns:
        # CA par praticien
        st.subheader("1. CA par praticien")
        ca_par_praticien = df_filtered.groupby('nom_complet_praticien')['montant_total_chf'].agg(['sum', 'mean', 'count']).round(2)
        ca_par_praticien.columns = ['CA_total', 'CA_moyen', 'Nombre_actes']
        ca_par_praticien = ca_par_praticien.sort_values('CA_total', ascending=False)
        
        if len(ca_par_praticien) > 0:
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(ca_par_praticien.head(10).reset_index().rename(columns={'nom_complet_praticien': 'Praticien'}))
            
            with col2:
                fig = px.bar(x=ca_par_praticien.head(10)['CA_total'], y=ca_par_praticien.head(10).index, orientation='h', title="Top 10 praticiens par CA total")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Pas assez de données pour cette analyse")
        
        # Taux de fidélisation par praticien
        st.subheader("2. Taux de fidélisation par praticien")
        patients_par_praticien = df_filtered.groupby('nom_complet_praticien')['patientid'].nunique()
        patients_fideles = df_filtered.groupby(['nom_complet_praticien', 'patientid']).size().reset_index()
        patients_fideles = patients_fideles[patients_fideles[0] > 1].groupby('nom_complet_praticien').size()
        
        if len(patients_par_praticien) > 0 and len(patients_fideles) > 0:
            taux_fidelisation = (patients_fideles / patients_par_praticien * 100).round(2)
            
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(taux_fidelisation.sort_values(ascending=False).head(10).reset_index().rename(columns={
                    'nom_complet_praticien': 'Praticien',
                    0: 'Taux de fidélisation (%)'
                }))
            
            with col2:
                fig = px.bar(x=taux_fidelisation.values, y=taux_fidelisation.index, title="Taux de fidélisation par praticien")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Pas assez de données pour cette analyse")
    else:
        st.warning("Colonne 'nom_complet_praticien' non trouvée dans les données")

# Analyse des Patients
elif page == "🧑‍🤝‍🧑 Analyse des Patients":
    st.header("🧑‍🤝‍🧑 Analyse des Patients")
    
    if selected_cabinet != "Tous les cabinets":
        st.info(f"📊 Analyses pour le cabinet : **{selected_cabinet}**")
    
    # Taux de rétention
    st.subheader("1. Taux de rétention")
    visites_par_patient = df_filtered.groupby('patientid').size()
    patients_fideles = (visites_par_patient > 1).sum()
    total_patients = len(visites_par_patient)
    
    if total_patients > 0:
        taux_retention = (patients_fideles / total_patients * 100).round(2)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Taux de rétention", f"{taux_retention}%")
            st.metric("Patients fidèles", f"{patients_fideles:,}")
            st.metric("Total patients", f"{total_patients:,}")
        
        with col2:
            fig = px.pie(values=[patients_fideles, total_patients - patients_fideles], 
                         names=['Patients fidèles', 'Patients uniques'], 
                         title="Répartition patients fidèles vs uniques")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Pas assez de données pour cette analyse")
    
    # Temps moyen entre soins
    st.subheader("2. Temps moyen entre soins")
    df_sorted = df_filtered.sort_values(['patientid', 'date_du_soin'])
    intervalles = []
    
    for patient in df_sorted['patientid'].unique():
        patient_data = df_sorted[df_sorted['patientid'] == patient]
        if len(patient_data) > 1:
            dates = patient_data['date_du_soin'].sort_values()
            for i in range(1, len(dates)):
                intervalle = (dates.iloc[i] - dates.iloc[i-1]).days
                intervalles.append(intervalle)
    
    if intervalles:
        intervalle_moyen = np.mean(intervalles)
        intervalle_median = np.median(intervalles)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Temps moyen", f"{intervalle_moyen:.1f} jours")
            st.metric("Temps médian", f"{intervalle_median:.1f} jours")
        
        with col2:
            fig = px.histogram(x=intervalles, nbins=30, title="Distribution des intervalles entre soins")
            fig.add_vline(x=intervalle_moyen, line_dash="dash", line_color="red", annotation_text=f"Moyenne: {intervalle_moyen:.1f} jours")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Pas assez de données pour cette analyse")
    
    # Nouveaux patients par mois
    st.subheader("3. Nouveaux patients par mois")
    nouveaux_patients = df_filtered.groupby(['Année-Mois', 'patientid']).first().reset_index()
    nouveaux_patients_mensuel = nouveaux_patients.groupby('Année-Mois').size()
    
    if len(nouveaux_patients_mensuel) > 0:
        fig = px.line(x=nouveaux_patients_mensuel.index, y=nouveaux_patients_mensuel.values, 
                       title="Évolution du nombre de nouveaux patients par mois")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Pas assez de données pour cette analyse")

# Paiements et Créances
elif page == "💰 Paiements et Créances":
    st.header("💰 Paiements et Créances")
    
    if selected_cabinet != "Tous les cabinets":
        st.info(f"📊 Analyses pour le cabinet : **{selected_cabinet}**")
    
    # Vérifier si les colonnes de retard existent
    if 'retard_paiement_jours' in df_filtered.columns and 'retard' in df_filtered.columns:
        st.subheader("1. Analyse des délais de paiement")
        
        # Statistiques de paiement
        taux_retard = df_filtered['retard'].mean() * 100
        montant_retard = df_filtered[df_filtered['retard']]['montant_total_chf'].sum()
        delai_moyen = df_filtered['retard_paiement_jours'].mean()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Taux de retard", f"{taux_retard:.2f}%")
        with col2:
            st.metric("Montant en retard", f"{montant_retard:,.0f} CHF")
        with col3:
            st.metric("Délai moyen", f"{delai_moyen:.1f} jours")
        
        # Visualisations
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.histogram(df_filtered, x='retard_paiement_jours', nbins=30, title="Distribution des délais de paiement")
            fig.add_vline(x=30, line_dash="dash", line_color="red", annotation_text="Seuil 30 jours")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.pie(values=df_filtered['retard'].value_counts().values, 
                         names=['À jour', 'En retard'], 
                         title="Répartition paiements en retard")
            st.plotly_chart(fig, use_container_width=True)
        
        # Analyse des retards par type de soin
        st.subheader("2. Taux de retard par type de soin")
        retards_par_soin = df_filtered.groupby('type_de_soin_normalisé')['retard'].agg(['mean', 'sum', 'count']).round(4)
        retards_par_soin.columns = ['Taux_retard', 'Nombre_retards', 'Nombre_total']
        retards_par_soin['Taux_retard_pct'] = retards_par_soin['Taux_retard'] * 100
        
        if len(retards_par_soin) > 0:
            fig = px.bar(x=retards_par_soin.head(15)['Taux_retard_pct'], 
                          y=retards_par_soin.head(15).index, 
                          orientation='h', 
                          title="Taux de retard par type de soin")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Pas assez de données pour cette analyse")
    else:
        st.warning("Colonnes de retard non trouvées dans les données")

# Analyse Géographique
elif page == "🏥 Analyse Géographique":
    st.header("🏥 Analyse Géographique")
    
    if selected_cabinet != "Tous les cabinets":
        st.info(f"📊 Analyses pour le cabinet : **{selected_cabinet}**")
    
    if 'nom_de_la_clinique' in df_filtered.columns:
        # CA par clinique
        st.subheader("1. CA par clinique")
        ca_par_clinique = df_filtered.groupby('nom_de_la_clinique')['montant_total_chf'].agg(['sum', 'mean', 'count']).round(2)
        ca_par_clinique.columns = ['CA_total', 'CA_moyen', 'Nombre_actes']
        ca_par_clinique = ca_par_clinique.sort_values('CA_total', ascending=False)
        
        if len(ca_par_clinique) > 0:
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(ca_par_clinique.reset_index().rename(columns={'nom_de_la_clinique': 'Clinique'}))
            
            with col2:
                fig = px.bar(x=ca_par_clinique['CA_total'], y=ca_par_clinique.index, orientation='h', title="CA total par clinique")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Pas assez de données pour cette analyse")
        
        # Patients uniques par clinique
        st.subheader("2. Nombre de patients uniques par clinique")
        patients_par_clinique = df_filtered.groupby('nom_de_la_clinique')['patientid'].nunique().sort_values(ascending=False)
        
        if len(patients_par_clinique) > 0:
            fig = px.bar(x=patients_par_clinique.values, y=patients_par_clinique.index, orientation='h', title="Nombre de patients uniques par clinique")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Pas assez de données pour cette analyse")
        
        # Taux de VIP par clinique
        if 'type_de_patient' in df_filtered.columns:
            st.subheader("3. Taux de patients VIP par clinique")
            vip_par_clinique = df_filtered.groupby('nom_de_la_clinique')['type_de_patient'].apply(lambda x: (x == 'VIP').mean() * 100).round(2)
            vip_par_clinique = vip_par_clinique.sort_values(ascending=False)
            
            if len(vip_par_clinique) > 0:
                fig = px.bar(x=vip_par_clinique.values, y=vip_par_clinique.index, orientation='h', title="Taux de patients VIP par clinique")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Pas assez de données pour cette analyse")
    else:
        st.warning("Colonne 'nom_de_la_clinique' non trouvée dans les données")

# Analyse Temporelle
elif page == "📅 Analyse Temporelle":
    st.header("📅 Analyse Temporelle")
    
    if selected_cabinet != "Tous les cabinets":
        st.info(f"📊 Analyses pour le cabinet : **{selected_cabinet}**")
    
    # CA par période
    st.subheader("1. CA par période")
    
    # CA par mois
    ca_mensuel = df_filtered.groupby('Année-Mois')['montant_total_chf'].sum()
    
    # CA par trimestre
    df_filtered['Trimestre'] = df_filtered['date_du_soin'].dt.quarter
    df_filtered['Année-Trimestre'] = df_filtered['Annee'].astype(str) + '-T' + df_filtered['Trimestre'].astype(str)
    ca_trimestriel = df_filtered.groupby('Année-Trimestre')['montant_total_chf'].sum()
    
    # CA par année
    ca_annuel = df_filtered.groupby('Annee')['montant_total_chf'].sum()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if len(ca_mensuel) > 0:
            fig = px.line(x=ca_mensuel.index, y=ca_mensuel.values, title="Évolution du CA mensuel")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Pas assez de données")
    
    with col2:
        if len(ca_trimestriel) > 0:
            fig = px.bar(x=ca_trimestriel.index, y=ca_trimestriel.values, title="CA par trimestre")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Pas assez de données")
    
    with col3:
        if len(ca_annuel) > 0:
            fig = px.bar(x=ca_annuel.index, y=ca_annuel.values, title="CA par année")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Pas assez de données")
    
    # Saisonnalité
    st.subheader("2. Saisonnalité des soins")
    df_filtered['Mois_annee'] = df_filtered['date_du_soin'].dt.month
    soins_par_mois = df_filtered.groupby('Mois_annee').size()
    ca_par_mois = df_filtered.groupby('Mois_annee')['montant_total_chf'].sum()
    
    # Noms des mois
    noms_mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
    soins_par_mois.index = [noms_mois[i-1] for i in soins_par_mois.index]
    ca_par_mois.index = [noms_mois[i-1] for i in ca_par_mois.index]
    
    col1, col2 = st.columns(2)
    
    with col1:
        if len(soins_par_mois) > 0:
            fig = px.bar(x=soins_par_mois.index, y=soins_par_mois.values, title="Répartition des soins par mois")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Pas assez de données")
    
    with col2:
        if len(ca_par_mois) > 0:
            fig = px.bar(x=ca_par_mois.index, y=ca_par_mois.values, title="CA par mois")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Pas assez de données")

# Footer
st.markdown("---")
st.markdown("📊 **Audit Analytique Cabinet Dentaire** - Développé avec Streamlit") 