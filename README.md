# 🦷 Audit Analytique d'un Cabinet Dentaire Multi-Sites

## 📊 Description du Projet

Ce projet d'analyse de données vise à optimiser les performances d'un cabinet dentaire multi-sites en analysant les soins, les praticiens, les patients et les paiements. L'application fournit des insights stratégiques pour améliorer la rentabilité et la satisfaction client.

## 🎯 Objectifs

- **Performance des soins** : Analyser la rentabilité par type de soin
- **Analyse des praticiens** : Évaluer les performances par praticien
- **Fidélisation des patients** : Mesurer le taux de rétention
- **Gestion des paiements** : Suivre les retards et créances
- **Analyse géographique** : Comparer les performances par clinique
- **Analyse temporelle** : Identifier les tendances et saisonnalités

## 🚀 Installation et Utilisation

### Prérequis
- Python 3.8+
- pip

### Installation

1. **Cloner le repository**
```bash
git clone https://github.com/votre-username/audit-cabinet-dentaire.git
cd audit-cabinet-dentaire
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Lancer l'application Streamlit**
```bash
streamlit run streamlit_app.py
```

4. **Ouvrir dans le navigateur**
L'application sera accessible à l'adresse : `http://localhost:8501`

## 📁 Structure du Projet

```
audit-cabinet-dentaire/
├── 📊 streamlit_app.py          # Application Streamlit principale
├── 📓 Audit analytique d'un cabinet dentaire multi-sites.ipynb  # Notebook Jupyter
├── 📋 requirements.txt           # Dépendances Python
├── 📖 README.md                 # Documentation
├── 🗂️ data/                     # Données (à ajouter)
│   └── patients_mis_a_jour.xlsx
├── 📈 scripts/                  # Scripts utilitaires
│   ├── analyze_notebook.py
│   ├── add_analysis_sections.py
│   ├── fix_notebook_columns.py
│   └── test_notebook_fix.py
└── 📊 visualisations/           # Graphiques générés
    └── performance_soins.png
```

## 🎨 Fonctionnalités de l'Application

### 🏠 Dashboard Général
- Métriques clés (patients, soins, CA)
- Évolution du CA mensuel
- Top 10 soins par chiffre d'affaires

### 🦷 Performance des Soins
- **Top 10 soins par CA** : Identification des soins les plus rentables
- **Rentabilité moyenne** : CA / nombre d'actes par type de soin
- **Soins par patient** : Distribution et statistiques

### 👨‍⚕️ Analyse des Praticiens
- **CA par praticien** : Performance individuelle
- **Taux de fidélisation** : Capacité à fidéliser les patients
- **Comparaison des performances** : Benchmark entre praticiens

### 🧑‍🤝‍🧑 Analyse des Patients
- **Taux de rétention** : % de patients revenus 2+ fois
- **Temps entre soins** : Intervalles moyens
- **Nouveaux patients** : Évolution mensuelle

### 💰 Paiements et Créances
- **Délais de paiement** : Distribution et seuils
- **Taux de retard** : Analyse par type de soin
- **Montants en retard** : Impact financier

### 🏥 Analyse Géographique
- **CA par clinique** : Performance par site
- **Patients par clinique** : Répartition géographique
- **Taux VIP par région** : Analyse de la clientèle

### 📅 Analyse Temporelle
- **CA par période** : Mensuel, trimestriel, annuel
- **Saisonnalité** : Répartition des soins dans l'année
- **Tendances** : Évolution temporelle

## 📊 KPIs Principaux

| KPI | Description | Formule |
|-----|-------------|---------|
| **CA Total** | Chiffre d'affaires global | `sum(montant_total_chf)` |
| **Taux de Rétention** | % patients fidèles | `patients_fidèles / total_patients * 100` |
| **Rentabilité Moyenne** | CA moyen par soin | `CA_total / nombre_actes` |
| **Taux de Retard** | % paiements en retard | `paiements_retard / total_paiements * 100` |
| **Soins/Patient** | Nombre moyen de soins | `total_soins / patients_uniques` |

## 🔧 Technologies Utilisées

- **Streamlit** : Interface utilisateur interactive
- **Pandas** : Manipulation et analyse de données
- **Plotly** : Visualisations interactives
- **NumPy** : Calculs numériques
- **Matplotlib/Seaborn** : Graphiques statiques

## 📈 Exemples d'Insights

### Performance des Soins
- Les **implants** génèrent le CA le plus élevé
- Les **consultations** ont la meilleure rentabilité moyenne
- Les **soins préventifs** représentent 60% du volume

### Analyse des Patients
- **Taux de rétention** : 14.19%
- **Temps moyen entre soins** : 45 jours
- **Nouveaux patients/mois** : 785 en moyenne

### Géographie
- **6 cliniques** analysées
- **83 praticiens** actifs
- **Répartition équilibrée** entre sites

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

**Votre Nom** - [votre-email@example.com](mailto:votre-email@example.com)

## 🙏 Remerciements

- Équipe de développement
- Cabinet dentaire pour les données
- Communauté Streamlit

---

⭐ **N'oubliez pas de donner une étoile au projet si vous l'aimez !**# Force redeploy for Streamlit Cloud
