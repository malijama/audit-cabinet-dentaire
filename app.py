import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from streamlit_option_menu import option_menu

# Initialize session state for language
if 'language' not in st.session_state:
    st.session_state['language'] = 'FR'

# Translations dictionary
translations = {
    'FR': {
        'title': 'Analyse Cabinet Dentaire',
        'upload': 'Télécharger un fichier Excel/CSV',
        'overview': 'Vue d\'ensemble',
        'analytics': 'Analyses',
        'insights': 'Recommandations',
        'total_patients': 'Nombre total de patients',
        'total_revenue': 'Revenu total',
        'total_treatments': 'Nombre total de soins',
        'avg_revenue': 'Revenu moyen par patient',
        'filter_clinic': 'Filtrer par clinique',
        'filter_practitioner': 'Filtrer par praticien',
        'filter_treatment': 'Filtrer par type de soin',
        'filter_date': 'Période',
        'monthly_trend': 'Évolution mensuelle',
        'top_treatments': 'Soins les plus rentables',
        'top_patients': 'Patients à forte valeur',
        'no_file': 'Veuillez télécharger un fichier Excel ou CSV',
        'error_missing_columns': 'Le fichier doit contenir les colonnes nécessaires',
        'satisfaction_analysis': 'Analyse de la satisfaction',
        'revenue_by_clinic': 'Revenus par clinique',
        'patient_loyalty': 'Fidélité des patients',
        'practitioner_performance': 'Performance des praticiens'
    },
    'EN': {
        'title': 'Dental Clinic Analytics',
        'upload': 'Upload Excel/CSV file',
        'overview': 'Overview',
        'analytics': 'Analytics',
        'insights': 'Insights',
        'total_patients': 'Total Patients',
        'total_revenue': 'Total Revenue',
        'total_treatments': 'Total Treatments',
        'avg_revenue': 'Average Revenue per Patient',
        'filter_clinic': 'Filter by Clinic',
        'filter_practitioner': 'Filter by Practitioner',
        'filter_treatment': 'Filter by Treatment Type',
        'filter_date': 'Date Range',
        'monthly_trend': 'Monthly Trend',
        'top_treatments': 'Top-Paying Treatments',
        'top_patients': 'High-Value Patients',
        'no_file': 'Please upload an Excel or CSV file',
        'error_missing_columns': 'File must contain the required columns',
        'satisfaction_analysis': 'Satisfaction Analysis',
        'revenue_by_clinic': 'Revenue by Clinic',
        'patient_loyalty': 'Patient Loyalty',
        'practitioner_performance': 'Practitioner Performance'
    }
}

def get_text(key):
    return translations[st.session_state['language']][key]

# Page config
st.set_page_config(page_title=get_text('title'), layout='wide')

# Language selector in sidebar
lang_col1, lang_col2 = st.sidebar.columns(2)
with lang_col1:
    if st.button('🇫🇷 FR'):
        st.session_state['language'] = 'FR'
        st.rerun()
with lang_col2:
    if st.button('🇬🇧 EN'):
        st.session_state['language'] = 'EN'
        st.rerun()

# Main title
st.title(get_text('title'))

# File uploader
uploaded_file = st.file_uploader(get_text('upload'), type=['xlsx', 'csv'])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Navigation menu
        selected = option_menu(
            menu_title=None,
            options=[get_text('overview'), get_text('analytics'), get_text('insights')],
            icons=['house', 'bar-chart', 'lightbulb'],
            orientation='horizontal',
        )

        # Sidebar filters
        st.sidebar.header('Filters')

        # Date filter
        df['Date du soin'] = pd.to_datetime(df['Date du soin'])
        min_date = df['Date du soin'].min()
        max_date = df['Date du soin'].max()
        start_date, end_date = st.sidebar.date_input(
            get_text('filter_date'),
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        # Apply date filter
        mask = (df['Date du soin'].dt.date >= start_date) & (df['Date du soin'].dt.date <= end_date)
        df_filtered = df.loc[mask]

        # Other filters
        if 'Nom de la clinique' in df.columns:
            clinic = st.sidebar.multiselect(get_text('filter_clinic'), df['Nom de la clinique'].unique())
            if clinic:
                df_filtered = df_filtered[df_filtered['Nom de la clinique'].isin(clinic)]

        if 'Nom complet praticien' in df.columns:
            practitioner = st.sidebar.multiselect(get_text('filter_practitioner'), df['Nom complet praticien'].unique())
            if practitioner:
                df_filtered = df_filtered[df_filtered['Nom complet praticien'].isin(practitioner)]

        if 'Type de soin normalisé' in df.columns:
            treatment = st.sidebar.multiselect(get_text('filter_treatment'), df['Type de soin normalisé'].unique())
            if treatment:
                df_filtered = df_filtered[df_filtered['Type de soin normalisé'].isin(treatment)]

        # Overview page
        if selected == get_text('overview'):
            # 1. Vue d'ensemble (Dashboard général)
            st.subheader('1. ' + get_text('overview'))
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.metric('🧑‍🤝‍🧑 ' + get_text('total_patients'), len(df_filtered['PatientID'].unique()))

            with col2:
                total_revenue = df_filtered['Montant total (CHF)'].sum()
                st.metric('💰 ' + get_text('total_revenue'), f"CHF {total_revenue:,.2f}")

            with col3:
                total_paid = df_filtered['Montant payé (CHF)'].sum()
                st.metric('🏦 Montant payé', f"CHF {total_paid:,.2f}")

            with col4:
                remaining = df_filtered['Reste à charge (CHF)'].sum()
                st.metric('📉 Reste à charge', f"CHF {remaining:,.2f}")

            with col5:
                avg_satisfaction = df_filtered['Satisfaction (1-5)'].mean()
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=avg_satisfaction,
                    title={'text': "😃 Satisfaction moyenne"},
                    gauge={'axis': {'range': [1, 5]},
                           'bar': {'color': "darkblue"},
                           'steps': [
                               {'range': [1, 2], 'color': "red"},
                               {'range': [2, 3], 'color': "orange"},
                               {'range': [3, 4], 'color': "yellow"},
                               {'range': [4, 5], 'color': "green"}
                           ]}
                ))
                st.plotly_chart(fig, use_container_width=True)

            # 2. Activité des soins
            st.subheader('2. Activité des soins')
            col1, col2 = st.columns(2)

            with col1:
                # Nombre de soins par mois
                monthly_treatments = df_filtered.groupby(df_filtered['Date du soin'].dt.to_period('M')).size().reset_index()
                monthly_treatments.columns = ['Date du soin', 'Nombre de soins']
                monthly_treatments['Date du soin'] = monthly_treatments['Date du soin'].astype(str)
                fig = px.line(monthly_treatments, x='Date du soin', y='Nombre de soins',
                             title='📅 Nombre de soins par mois')
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Soins les plus fréquents
                top_treatments = df_filtered['Type de soin normalisé'].value_counts().head(5)
                fig = px.bar(top_treatments, orientation='h',
                            title='🦷 Top 5 des soins les plus fréquents')
                st.plotly_chart(fig, use_container_width=True)

            col3, col4 = st.columns(2)

            with col3:
                # Durée moyenne des soins
                avg_duration = df_filtered['Durée (minutes)'].mean()
                fig = go.Figure(go.Indicator(
                    mode="number+gauge",
                    value=avg_duration,
                    title={'text': "⏱️ Durée moyenne des soins (minutes)"},
                    gauge={'axis': {'range': [0, df_filtered['Durée (minutes)'].max()]},
                           'bar': {'color': "darkblue"}}
                ))
                st.plotly_chart(fig, use_container_width=True)

            with col4:
                # Taux de rendez-vous manqués
                missed_appointments = (df_filtered['Rendez-vous manqué'] == 'Oui').mean() * 100
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=missed_appointments,
                    number={'suffix': "%"},
                    title={'text': "📆 Taux de rendez-vous manqués"},
                    gauge={'axis': {'range': [0, 100]},
                           'bar': {'color': "red"}}
                ))
                st.plotly_chart(fig, use_container_width=True)

        # Analytics page
        elif selected == get_text('analytics'):
            # Revenue by Treatment Type
            st.subheader(get_text('top_treatments'))
            treatment_revenue = df_filtered.groupby('Type de soin normalisé')['Montant total (CHF)'].sum().sort_values(ascending=False)
            fig = px.bar(treatment_revenue, labels={'Type de soin normalisé': 'Type de soin', 'Montant total (CHF)': 'Revenu (CHF)'})
            st.plotly_chart(fig, use_container_width=True)

            # Revenue by Clinic
            st.subheader(get_text('revenue_by_clinic'))
            clinic_revenue = df_filtered.groupby('Nom de la clinique')['Montant total (CHF)'].sum().sort_values(ascending=False)
            fig = px.bar(clinic_revenue, labels={'Nom de la clinique': 'Clinique', 'Montant total (CHF)': 'Revenu (CHF)'})
            st.plotly_chart(fig, use_container_width=True)

        # Insights page
        elif selected == get_text('insights'):
            # 4. Analyse patientèle
            st.subheader('4. Analyse patientèle')
            col1, col2 = st.columns(2)

            with col1:
                # Taux de fidélisation
                loyalty_data = df_filtered[df_filtered['Patient fidèle'] == True]['PatientID'].count()
                total_patients = len(df_filtered['PatientID'].unique())
                loyalty_percentage = (loyalty_data / total_patients) * 100
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=loyalty_percentage,
                    number={'suffix': "%"},
                    title={'text': "🔁 Taux de fidélisation"},
                    gauge={'axis': {'range': [0, 100]},
                           'bar': {'color': "green"}}
                ))
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Répartition hommes/femmes
                gender_dist = df_filtered['Sexe'].value_counts()
                fig = px.pie(values=gender_dist.values, names=gender_dist.index,
                            title='👥 Répartition hommes/femmes')
                st.plotly_chart(fig, use_container_width=True)

            col3, col4 = st.columns(2)

            with col3:
                # Visites moyennes par patient
                visits_per_patient = df_filtered.groupby('PatientID').size()
                fig = px.histogram(visits_per_patient, title='📈 Distribution des visites par patient',
                                  labels={'value': 'Nombre de visites', 'count': 'Nombre de patients'})
                st.plotly_chart(fig, use_container_width=True)

            with col4:
                # Répartition par canton
                canton_dist = df_filtered['Canton clinique'].value_counts()
                fig = px.bar(canton_dist, title='🗺️ Répartition par canton',
                            labels={'index': 'Canton', 'value': 'Nombre de patients'})
                st.plotly_chart(fig, use_container_width=True)

            # 5. Performances individuelles
            st.subheader('5. Performances individuelles')
            col1, col2 = st.columns(2)

            with col1:
                # Revenu horaire moyen par praticien
                hourly_revenue = df_filtered.groupby('Nom complet praticien')['Revenu horaire (CHF/h)'].mean().sort_values(ascending=True)
                fig = px.bar(hourly_revenue, orientation='h',
                            title='💸 Revenu horaire moyen par praticien',
                            labels={'Nom complet praticien': 'Praticien', 'value': 'CHF/h'})
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Satisfaction par praticien
                satisfaction_by_pract = df_filtered.groupby('Nom complet praticien')['Satisfaction (1-5)'].mean().sort_values(ascending=True)
                fig = px.bar(satisfaction_by_pract, orientation='h',
                            title='🌟 Satisfaction moyenne par praticien',
                            labels={'Nom complet praticien': 'Praticien', 'value': 'Note /5'})
                st.plotly_chart(fig, use_container_width=True)

            # Montant moyen par soin
            avg_amount_by_treatment = df_filtered.groupby('Type de soin normalisé')['Montant total (CHF)'].mean().sort_values(ascending=False)
            st.subheader('🧾 Montant moyen par type de soin')
            fig = px.bar(avg_amount_by_treatment,
                        labels={'Type de soin normalisé': 'Type de soin', 'value': 'Montant moyen (CHF)'})
            st.plotly_chart(fig, use_container_width=True)
            practitioner_performance = df_filtered.groupby('Nom complet praticien').agg({
                'Montant total (CHF)': 'sum',
                'PatientID': 'nunique',
                'Satisfaction (1-5)': 'mean'
            }).sort_values('Montant total (CHF)', ascending=False)
            
            fig = go.Figure(data=[
                go.Bar(name='Revenu', x=practitioner_performance.index, y=practitioner_performance['Montant total (CHF)']),
                go.Bar(name='Nombre de patients', x=practitioner_performance.index, y=practitioner_performance['PatientID'])
            ])
            fig.update_layout(barmode='group')
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")

else:
    st.info(get_text('no_file'))