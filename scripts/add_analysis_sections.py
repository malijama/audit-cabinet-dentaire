#!/usr/bin/env python3
import json
import os

def add_analysis_sections():
    # Charger le notebook existant
    notebook_files = [f for f in os.listdir('.') if f.endswith('.ipynb')]
    notebook_file = notebook_files[0]
    
    with open(notebook_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Nouvelles cellules à ajouter
    new_cells = []
    
    # 1. Performance des soins
    new_cells.extend([
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 🦷 1. Performance des soins\n\n",
                "### KPIs à analyser :\n",
                "- **Top 10 soins par chiffre d'affaires**\n",
                "- **Rentabilité moyenne par soin** = CA / nombre d'actes\n",
                "- **Durée moyenne d'un soin** (si dispo) → rentabilité par minute\n",
                "- **Nombre moyen de soins par patient**\n\n",
                "### Analyses :\n",
                "- Comparaison entre soins préventifs vs curatifs\n",
                "- Évolution du nombre de soins par type dans le temps\n"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 🦷 1.1 Top 10 soins par chiffre d'affaires\n",
                "top_10_ca_soins = df.groupby('Type De Soin Normalisé')['Montant (CHF)'].sum().sort_values(ascending=False).head(10)\n",
                "print('Top 10 soins par chiffre d\\'affaires :')\n",
                "print(top_10_ca_soins)\n",
                "\n",
                "# Visualisation\n",
                "plt.figure(figsize=(12, 8))\n",
                "top_10_ca_soins.plot(kind='barh')\n",
                "plt.title('Top 10 soins par chiffre d\\'affaires')\n",
                "plt.xlabel('Chiffre d\\'affaires (CHF)')\n",
                "plt.ylabel('Type de soin')\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 🦷 1.2 Rentabilité moyenne par soin\n",
                "rentabilite_soins = df.groupby('Type De Soin Normalisé').agg({\n",
                "    'Montant (CHF)': 'sum',\n",
                "    'Type De Soin Normalisé': 'count'\n",
                "}).rename(columns={'Type De Soin Normalisé': 'Nombre_actes'})\n",
                "rentabilite_soins['Rentabilite_moyenne'] = rentabilite_soins['Montant (CHF)'] / rentabilite_soins['Nombre_actes']\n",
                "rentabilite_soins = rentabilite_soins.sort_values('Rentabilite_moyenne', ascending=False)\n",
                "\n",
                "print('Rentabilité moyenne par soin :')\n",
                "print(rentabilite_soins.head(10))\n",
                "\n",
                "# Visualisation\n",
                "plt.figure(figsize=(12, 8))\n",
                "rentabilite_soins.head(15)['Rentabilite_moyenne'].plot(kind='barh')\n",
                "plt.title('Rentabilité moyenne par type de soin')\n",
                "plt.xlabel('Rentabilité moyenne (CHF)')\n",
                "plt.ylabel('Type de soin')\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 🦷 1.3 Nombre moyen de soins par patient\n",
                "soins_par_patient = df.groupby('Patient')['Type De Soin Normalisé'].count()\n",
                "moyenne_soins_patient = soins_par_patient.mean()\n",
                "median_soins_patient = soins_par_patient.median()\n",
                "\n",
                "print(f'Nombre moyen de soins par patient : {moyenne_soins_patient:.2f}')\n",
                "print(f'Nombre médian de soins par patient : {median_soins_patient:.2f}')\n",
                "\n",
                "# Distribution du nombre de soins par patient\n",
                "plt.figure(figsize=(10, 6))\n",
                "soins_par_patient.hist(bins=30, edgecolor='black')\n",
                "plt.title('Distribution du nombre de soins par patient')\n",
                "plt.xlabel('Nombre de soins')\n",
                "plt.ylabel('Nombre de patients')\n",
                "plt.axvline(moyenne_soins_patient, color='red', linestyle='--', label=f'Moyenne: {moyenne_soins_patient:.2f}')\n",
                "plt.legend()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 🦷 1.4 Comparaison soins préventifs vs curatifs\n",
                "# Définir les catégories (à adapter selon vos données)\n",
                "soins_preventifs = ['Consultation', 'Détartrage', 'Examen', 'Radiographie', 'Nettoyage']\n",
                "soins_curatifs = ['Canal', 'Couronne', 'Implant', 'Extraction', 'Obturation']\n",
                "\n",
                "# Créer une colonne de catégorie\n",
                "def categoriser_soin(soin):\n",
                "    if any(preventif in soin for preventif in soins_preventifs):\n",
                "        return 'Préventif'\n",
                "    elif any(curatif in soin for curatif in soins_curatifs):\n",
                "        return 'Curatif'\n",
                "    else:\n",
                "        return 'Autre'\n",
                "\n",
                "df['Categorie_soin'] = df['Type De Soin Normalisé'].apply(categoriser_soin)\n",
                "\n",
                "# Analyse comparative\n",
                "comparaison_categories = df.groupby('Categorie_soin').agg({\n",
                "    'Montant (CHF)': ['sum', 'mean', 'count'],\n",
                "    'Patient': 'nunique'\n",
                "}).round(2)\n",
                "\n",
                "print('Comparaison soins préventifs vs curatifs :')\n",
                "print(comparaison_categories)\n",
                "\n",
                "# Visualisation\n",
                "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))\n",
                "\n",
                "# CA par catégorie\n",
                "ca_par_categorie = df.groupby('Categorie_soin')['Montant (CHF)'].sum()\n",
                "ax1.pie(ca_par_categorie.values, labels=ca_par_categorie.index, autopct='%1.1f%%')\n",
                "ax1.set_title('Répartition du CA par catégorie de soin')\n",
                "\n",
                "# Nombre d'actes par catégorie\n",
                "actes_par_categorie = df.groupby('Categorie_soin').size()\n",
                "ax2.bar(actes_par_categorie.index, actes_par_categorie.values)\n",
                "ax2.set_title('Nombre d\\'actes par catégorie de soin')\n",
                "ax2.set_ylabel('Nombre d\\'actes')\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        }
    ])
    
    # 2. Praticiens
    new_cells.extend([
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 👨‍⚕️ 2. Praticiens\n\n",
                "### KPIs à analyser :\n",
                "- **CA moyen par praticien**\n",
                "- **CA par heure ou par jour travaillé** (si infos dispo)\n",
                "- **Taux de fidélisation des patients par praticien**\n",
                "- **Taux de soins en retard de paiement par praticien**\n\n",
                "### Analyses :\n",
                "- Clustering des praticiens par performance (CA, volume, fidélité)\n",
                "- Corrélation entre ancienneté du praticien et performance\n"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 👨‍⚕️ 2.1 CA moyen par praticien\n",
                "if 'Praticien' in df.columns:\n",
                "    ca_par_praticien = df.groupby('Praticien')['Montant (CHF)'].agg(['sum', 'mean', 'count']).round(2)\n",
                "    ca_par_praticien.columns = ['CA_total', 'CA_moyen', 'Nombre_actes']\n",
                "    ca_par_praticien = ca_par_praticien.sort_values('CA_total', ascending=False)\n",
                "    \n",
                "    print('Performance par praticien :')\n",
                "    print(ca_par_praticien)\n",
                "    \n",
                "    # Visualisation\n",
                "    plt.figure(figsize=(12, 8))\n",
                "    ca_par_praticien.head(10)['CA_total'].plot(kind='bar')\n",
                "    plt.title('Top 10 praticiens par CA total')\n",
                "    plt.xlabel('Praticien')\n",
                "    plt.ylabel('CA total (CHF)')\n",
                "    plt.xticks(rotation=45)\n",
                "    plt.tight_layout()\n",
                "    plt.show()\n",
                "else:\n",
                "    print('Colonne \\'Praticien\\' non trouvée dans les données')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 👨‍⚕️ 2.2 Taux de fidélisation par praticien\n",
                "if 'Praticien' in df.columns:\n",
                "    # Calculer le nombre de patients uniques par praticien\n",
                "    patients_par_praticien = df.groupby('Praticien')['Patient'].nunique()\n",
                "    \n",
                "    # Calculer le nombre de patients fidèles (plus d'un soin)\n",
                "    patients_fideles = df.groupby(['Praticien', 'Patient']).size().reset_index()\n",
                "    patients_fideles = patients_fideles[patients_fideles[0] > 1].groupby('Praticien').size()\n",
                "    \n",
                "    # Calculer le taux de fidélisation\n",
                "    taux_fidelisation = (patients_fideles / patients_par_praticien * 100).round(2)\n",
                "    \n",
                "    print('Taux de fidélisation par praticien :')\n",
                "    print(taux_fidelisation.sort_values(ascending=False))\n",
                "    \n",
                "    # Visualisation\n",
                "    plt.figure(figsize=(12, 8))\n",
                "    taux_fidelisation.plot(kind='bar')\n",
                "    plt.title('Taux de fidélisation par praticien')\n",
                "    plt.xlabel('Praticien')\n",
                "    plt.ylabel('Taux de fidélisation (%)')\n",
                "    plt.xticks(rotation=45)\n",
                "    plt.tight_layout()\n",
                "    plt.show()\n",
                "else:\n",
                "    print('Colonne \\'Praticien\\' non trouvée dans les données')"
            ]
        }
    ])
    
    # 3. Patients
    new_cells.extend([
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 🧑‍🤝‍🧑 3. Patients\n\n",
                "### KPIs à analyser :\n",
                "- **Taux de rétention** = % de patients revenus 2+ fois\n",
                "- **Temps moyen entre 2 soins**\n",
                "- **Nombre de nouveaux patients par mois**\n",
                "- **Proportion de patients VIP par clinique**\n\n",
                "### Analyses :\n",
                "- Analyse RFM : Récence, Fréquence, Montant\n",
                "- Profils des VIP vs non-VIP : âge, localisation, clinique, type de soin\n"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 🧑‍🤝‍🧑 3.1 Taux de rétention\n",
                "visites_par_patient = df.groupby('Patient').size()\n",
                "patients_fideles = (visites_par_patient > 1).sum()\n",
                "total_patients = len(visites_par_patient)\n",
                "taux_retention = (patients_fideles / total_patients * 100).round(2)\n",
                "\n",
                "print(f'Taux de rétention : {taux_retention}%')\n",
                "print(f'Nombre de patients fidèles : {patients_fideles}')\n",
                "print(f'Nombre total de patients : {total_patients}')\n",
                "\n",
                "# Distribution du nombre de visites\n",
                "plt.figure(figsize=(10, 6))\n",
                "visites_par_patient.value_counts().sort_index().plot(kind='bar')\n",
                "plt.title('Distribution du nombre de visites par patient')\n",
                "plt.xlabel('Nombre de visites')\n",
                "plt.ylabel('Nombre de patients')\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 🧑‍🤝‍🧑 3.2 Temps moyen entre 2 soins\n",
                "# Calculer les intervalles entre soins pour chaque patient\n",
                "df_sorted = df.sort_values(['Patient', 'Date'])\n",
                "intervalles = []\n",
                "\n",
                "for patient in df_sorted['Patient'].unique():\n",
                "    patient_data = df_sorted[df_sorted['Patient'] == patient]\n",
                "    if len(patient_data) > 1:\n",
                "        dates = patient_data['Date'].sort_values()\n",
                "        for i in range(1, len(dates)):\n",
                "            intervalle = (dates.iloc[i] - dates.iloc[i-1]).days\n",
                "            intervalles.append(intervalle)\n",
                "\n",
                "if intervalles:\n",
                "    intervalle_moyen = np.mean(intervalles)\n",
                "    intervalle_median = np.median(intervalles)\n",
                "    \n",
                "    print(f'Temps moyen entre 2 soins : {intervalle_moyen:.1f} jours')\n",
                "    print(f'Temps médian entre 2 soins : {intervalle_median:.1f} jours')\n",
                "    \n",
                "    # Histogramme des intervalles\n",
                "    plt.figure(figsize=(10, 6))\n",
                "    plt.hist(intervalles, bins=30, edgecolor='black')\n",
                "    plt.title('Distribution des intervalles entre soins')\n",
                "    plt.xlabel('Jours entre soins')\n",
                "    plt.ylabel('Nombre d\\'intervalles')\n",
                "    plt.axvline(intervalle_moyen, color='red', linestyle='--', label=f'Moyenne: {intervalle_moyen:.1f} jours')\n",
                "    plt.legend()\n",
                "    plt.show()\n",
                "else:\n",
                "    print('Pas assez de données pour calculer les intervalles')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 🧑‍🤝‍🧑 3.3 Nouveaux patients par mois\n",
                "nouveaux_patients = df.groupby(['Année-Mois', 'Patient']).first().reset_index()\n",
                "nouveaux_patients_mensuel = nouveaux_patients.groupby('Année-Mois').size()\n",
                "\n",
                "print('Nouveaux patients par mois :')\n",
                "print(nouveaux_patients_mensuel)\n",
                "\n",
                "# Visualisation\n",
                "plt.figure(figsize=(12, 6))\n",
                "nouveaux_patients_mensuel.plot(kind='line', marker='o')\n",
                "plt.title('Évolution du nombre de nouveaux patients par mois')\n",
                "plt.xlabel('Mois')\n",
                "plt.ylabel('Nombre de nouveaux patients')\n",
                "plt.xticks(rotation=45)\n",
                "plt.grid(True, alpha=0.3)\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 🧑‍🤝‍🧑 3.4 Analyse RFM (Récence, Fréquence, Montant)\n",
                "from datetime import datetime\n",
                "\n",
                "# Date de référence (dernière date dans les données)\n",
                "date_reference = df['Date'].max()\n",
                "\n",
                "# Calcul RFM par patient\n",
                "rfm = df.groupby('Patient').agg({\n",
                "    'Date': lambda x: (date_reference - x.max()).days,  # Récence\n",
                "    'Type De Soin Normalisé': 'count',  # Fréquence\n",
                "    'Montant (CHF)': 'sum'  # Montant\n",
                "}).rename(columns={\n",
                "    'Date': 'Recence',\n",
                "    'Type De Soin Normalisé': 'Frequence',\n",
                "    'Montant (CHF)': 'Montant'\n",
                "})\n",
                "\n",
                "# Créer des scores RFM (1-5)\n",
                "def score_rfm(data, column, ascending=True):\n",
                "    return pd.qcut(data[column], q=5, labels=[5,4,3,2,1] if ascending else [1,2,3,4,5])\n",
                "\n",
                "rfm['Score_R'] = score_rfm(rfm, 'Recence', ascending=True)\n",
                "rfm['Score_F'] = score_rfm(rfm, 'Frequence', ascending=False)\n",
                "rfm['Score_M'] = score_rfm(rfm, 'Montant', ascending=False)\n",
                "\n",
                "rfm['Score_RFM'] = rfm['Score_R'].astype(str) + rfm['Score_F'].astype(str) + rfm['Score_M'].astype(str)\n",
                "\n",
                "print('Analyse RFM - Top 10 patients :')\n",
                "print(rfm.sort_values('Score_RFM', ascending=False).head(10))\n",
                "\n",
                "# Distribution des scores RFM\n",
                "plt.figure(figsize=(15, 5))\n",
                "\n",
                "plt.subplot(1, 3, 1)\n",
                "rfm['Recence'].hist(bins=20)\n",
                "plt.title('Distribution de la Récence')\n",
                "plt.xlabel('Jours depuis dernière visite')\n",
                "\n",
                "plt.subplot(1, 3, 2)\n",
                "rfm['Frequence'].hist(bins=20)\n",
                "plt.title('Distribution de la Fréquence')\n",
                "plt.xlabel('Nombre de visites')\n",
                "\n",
                "plt.subplot(1, 3, 3)\n",
                "rfm['Montant'].hist(bins=20)\n",
                "plt.title('Distribution du Montant')\n",
                "plt.xlabel('Montant total (CHF)')\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        }
    ])
    
    # 4. Paiements et créances
    new_cells.extend([
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 💰 4. Paiements et créances\n\n",
                "### KPIs à analyser :\n",
                "- **% de paiements en retard**\n",
                "- **Montant total des paiements en retard**\n",
                "- **Délai moyen de paiement**\n",
                "- **Taux de recouvrement à 30 / 60 / 90 jours**\n\n",
                "### Analyses :\n",
                "- Corrélation entre type de soin ou clinique et retards\n",
                "- Analyse des retards par canton, ville, ou praticien\n"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 💰 4.1 Analyse des paiements en retard\n",
                "# Vérifier si nous avons des colonnes de paiement\n",
                "colonnes_paiement = [col for col in df.columns if 'paiement' in col.lower() or 'retard' in col.lower() or 'delai' in col.lower()]\n",
                "print('Colonnes liées aux paiements trouvées :', colonnes_paiement)\n",
                "\n",
                "if colonnes_paiement:\n",
                "    for col in colonnes_paiement:\n",
                "        print(f'\\nAnalyse de {col}:')\n",
                "        print(df[col].value_counts().head())\n",
                "        print(f'Valeurs manquantes : {df[col].isnull().sum()}')\n",
                "else:\n",
                "    print('Aucune colonne de paiement trouvée. Création d\\'indicateurs simulés...')\n",
                "    \n",
                "    # Simulation d'analyses de paiement\n",
                "    np.random.seed(42)\n",
                "    df['Delai_paiement_jours'] = np.random.exponential(30, len(df))\n",
                "    df['En_retard'] = df['Delai_paiement_jours'] > 30\n",
                "    \n",
                "    # Statistiques de paiement\n",
                "    taux_retard = df['En_retard'].mean() * 100\n",
                "    montant_retard = df[df['En_retard']]['Montant (CHF)'].sum()\n",
                "    delai_moyen = df['Delai_paiement_jours'].mean()\n",
                "    \n",
                "    print(f'Taux de paiements en retard : {taux_retard:.2f}%')\n",
                "    print(f'Montant total en retard : {montant_retard:,.0f} CHF')\n",
                "    print(f'Délai moyen de paiement : {delai_moyen:.1f} jours')\n",
                "    \n",
                "    # Visualisation\n",
                "    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))\n",
                "    \n",
                "    # Distribution des délais\n",
                "    ax1.hist(df['Delai_paiement_jours'], bins=30, edgecolor='black')\n",
                "    ax1.set_title('Distribution des délais de paiement')\n",
                "    ax1.set_xlabel('Jours')\n",
                "    ax1.set_ylabel('Nombre de paiements')\n",
                "    ax1.axvline(30, color='red', linestyle='--', label='Seuil 30 jours')\n",
                "    ax1.legend()\n",
                "    \n",
                "    # Répartition retard/non-retard\n",
                "    df['En_retard'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax2)\n",
                "    ax2.set_title('Répartition paiements en retard')\n",
                "    \n",
                "    plt.tight_layout()\n",
                "    plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 💰 4.2 Analyse des retards par type de soin\n",
                "if 'En_retard' in df.columns:\n",
                "    retards_par_soin = df.groupby('Type De Soin Normalisé')['En_retard'].agg(['mean', 'sum', 'count']).round(4)\n",
                "    retards_par_soin.columns = ['Taux_retard', 'Nombre_retards', 'Nombre_total']\n",
                "    retards_par_soin['Taux_retard_pct'] = retards_par_soin['Taux_retard'] * 100\n",
                "    \n",
                "    print('Taux de retard par type de soin :')\n",
                "    print(retards_par_soin.sort_values('Taux_retard_pct', ascending=False).head(10))\n",
                "    \n",
                "    # Visualisation\n",
                "    plt.figure(figsize=(12, 8))\n",
                "    retards_par_soin.head(15)['Taux_retard_pct'].plot(kind='barh')\n",
                "    plt.title('Taux de retard par type de soin')\n",
                "    plt.xlabel('Taux de retard (%)')\n",
                "    plt.ylabel('Type de soin')\n",
                "    plt.tight_layout()\n",
                "    plt.show()\n",
                "else:\n",
                "    print('Colonne \\'En_retard\\' non disponible')"
            ]
        }
    ])
    
    # 5. Analyse géographique
    new_cells.extend([
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 🏥 5. Analyse géographique\n\n",
                "### KPIs à analyser :\n",
                "- **CA par clinique / canton / ville**\n",
                "- **Nombre de patients uniques par région**\n",
                "- **Taux de VIP par région**\n\n",
                "### Analyses :\n",
                "- Visualisation cartographique des performances\n",
                "- Benchmark entre cliniques\n"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 🏥 5.1 CA par ville/canton\n",
                "if 'Ville' in df.columns:\n",
                "    ca_par_ville = df.groupby('Ville')['Montant (CHF)'].agg(['sum', 'mean', 'count']).round(2)\n",
                "    ca_par_ville.columns = ['CA_total', 'CA_moyen', 'Nombre_actes']\n",
                "    ca_par_ville = ca_par_ville.sort_values('CA_total', ascending=False)\n",
                "    \n",
                "    print('CA par ville (Top 15) :')\n",
                "    print(ca_par_ville.head(15))\n",
                "    \n",
                "    # Visualisation\n",
                "    plt.figure(figsize=(12, 8))\n",
                "    ca_par_ville.head(15)['CA_total'].plot(kind='barh')\n",
                "    plt.title('CA total par ville')\n",
                "    plt.xlabel('CA total (CHF)')\n",
                "    plt.ylabel('Ville')\n",
                "    plt.tight_layout()\n",
                "    plt.show()\n",
                "else:\n",
                "    print('Colonne \\'Ville\\' non trouvée')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 🏥 5.2 Patients uniques par région\n",
                "if 'Ville' in df.columns:\n",
                "    patients_par_ville = df.groupby('Ville')['Patient'].nunique().sort_values(ascending=False)\n",
                "    \n",
                "    print('Nombre de patients uniques par ville (Top 15) :')\n",
                "    print(patients_par_ville.head(15))\n",
                "    \n",
                "    # Visualisation\n",
                "    plt.figure(figsize=(12, 8))\n",
                "    patients_par_ville.head(15).plot(kind='barh')\n",
                "    plt.title('Nombre de patients uniques par ville')\n",
                "    plt.xlabel('Nombre de patients')\n",
                "    plt.ylabel('Ville')\n",
                "    plt.tight_layout()\n",
                "    plt.show()\n",
                "else:\n",
                "    print('Colonne \\'Ville\\' non trouvée')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 🏥 5.3 Taux de VIP par région\n",
                "if 'Ville' in df.columns and 'Type De Patient' in df.columns:\n",
                "    # Calculer le taux de VIP par ville\n",
                "    vip_par_ville = df.groupby('Ville')['Type De Patient'].apply(lambda x: (x == 'VIP').mean() * 100).round(2)\n",
                "    vip_par_ville = vip_par_ville.sort_values(ascending=False)\n",
                "    \n",
                "    print('Taux de patients VIP par ville (Top 15) :')\n",
                "    print(vip_par_ville.head(15))\n",
                "    \n",
                "    # Visualisation\n",
                "    plt.figure(figsize=(12, 8))\n",
                "    vip_par_ville.head(15).plot(kind='barh')\n",
                "    plt.title('Taux de patients VIP par ville')\n",
                "    plt.xlabel('Taux de VIP (%)')\n",
                "    plt.ylabel('Ville')\n",
                "    plt.tight_layout()\n",
                "    plt.show()\n",
                "else:\n",
                "    print('Colonnes \\'Ville\\' ou \\'Type De Patient\\' non trouvées')"
            ]
        }
    ])
    
    # 6. Analyse temporelle
    new_cells.extend([
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 📅 6. Analyse temporelle\n\n",
                "### KPIs à analyser :\n",
                "- **CA par mois / trimestre / année**\n",
                "- **Nombre de patients par mois**\n",
                "- **Répartition des soins dans l'année (saisonnalité)**\n"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 📅 6.1 CA par période\n",
                "# CA par mois\n",
                "ca_mensuel = df.groupby('Année-Mois')['Montant (CHF)'].sum()\n",
                "print('CA mensuel :')\n",
                "print(ca_mensuel)\n",
                "\n",
                "# CA par trimestre\n",
                "df['Trimestre'] = df['Date'].dt.quarter\n",
                "df['Année-Trimestre'] = df['Année'].astype(str) + '-T' + df['Trimestre'].astype(str)\n",
                "ca_trimestriel = df.groupby('Année-Trimestre')['Montant (CHF)'].sum()\n",
                "print('\\nCA trimestriel :')\n",
                "print(ca_trimestriel)\n",
                "\n",
                "# CA par année\n",
                "ca_annuel = df.groupby('Année')['Montant (CHF)'].sum()\n",
                "print('\\nCA annuel :')\n",
                "print(ca_annuel)\n",
                "\n",
                "# Visualisations\n",
                "fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15))\n",
                "\n",
                "ca_mensuel.plot(kind='line', marker='o', ax=ax1)\n",
                "ax1.set_title('Évolution du CA mensuel')\n",
                "ax1.set_ylabel('CA (CHF)')\n",
                "ax1.grid(True, alpha=0.3)\n",
                "\n",
                "ca_trimestriel.plot(kind='bar', ax=ax2)\n",
                "ax2.set_title('CA par trimestre')\n",
                "ax2.set_ylabel('CA (CHF)')\n",
                "ax2.tick_params(axis='x', rotation=45)\n",
                "\n",
                "ca_annuel.plot(kind='bar', ax=ax3)\n",
                "ax3.set_title('CA par année')\n",
                "ax3.set_ylabel('CA (CHF)')\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 📅 6.2 Saisonnalité des soins\n",
                "# Répartition par mois de l'année\n",
                "df['Mois_annee'] = df['Date'].dt.month\n",
                "soins_par_mois = df.groupby('Mois_annee').size()\n",
                "ca_par_mois = df.groupby('Mois_annee')['Montant (CHF)'].sum()\n",
                "\n",
                "# Noms des mois\n",
                "noms_mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']\n",
                "soins_par_mois.index = [noms_mois[i-1] for i in soins_par_mois.index]\n",
                "ca_par_mois.index = [noms_mois[i-1] for i in ca_par_mois.index]\n",
                "\n",
                "fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))\n",
                "\n",
                "soins_par_mois.plot(kind='bar', ax=ax1)\n",
                "ax1.set_title('Répartition des soins par mois')\n",
                "ax1.set_ylabel('Nombre de soins')\n",
                "ax1.tick_params(axis='x', rotation=45)\n",
                "\n",
                "ca_par_mois.plot(kind='bar', ax=ax2)\n",
                "ax2.set_title('CA par mois')\n",
                "ax2.set_ylabel('CA (CHF)')\n",
                "ax2.tick_params(axis='x', rotation=45)\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.show()\n",
                "\n",
                "# Analyse de saisonnalité par type de soin\n",
                "soins_saisonniers = df.groupby(['Mois_annee', 'Type De Soin Normalisé']).size().unstack(fill_value=0)\n",
                "soins_saisonniers.index = [noms_mois[i-1] for i in soins_saisonniers.index]\n",
                "\n",
                "plt.figure(figsize=(15, 8))\n",
                "soins_saisonniers.plot(kind='bar', stacked=True)\n",
                "plt.title('Répartition saisonnière par type de soin')\n",
                "plt.xlabel('Mois')\n",
                "plt.ylabel('Nombre de soins')\n",
                "plt.xticks(rotation=45)\n",
                "plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        }
    ])
    
    # Ajouter les nouvelles cellules au notebook
    data['cells'].extend(new_cells)
    
    # Sauvegarder le notebook mis à jour
    with open(notebook_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ {len(new_cells)} nouvelles cellules ajoutées au notebook")
    print("📊 Sections ajoutées :")
    print("   🦷 1. Performance des soins")
    print("   👨‍⚕️ 2. Praticiens") 
    print("   🧑‍🤝‍🧑 3. Patients")
    print("   💰 4. Paiements et créances")
    print("   🏥 5. Analyse géographique")
    print("   📅 6. Analyse temporelle")

if __name__ == "__main__":
    add_analysis_sections() 