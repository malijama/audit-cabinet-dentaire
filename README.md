# 🦷 Audit Analytique d'un Cabinet Dentaire Multi-Sites

## 📊 Description du Projet

Ce projet d'analyse de données vise à optimiser les performances d'un cabinet dentaire multi-sites en analysant les soins, les praticiens, les patients et les paiements. Le dashboard Power BI fournit des insights stratégiques pour améliorer la rentabilité et la satisfaction client.

## 🎯 Objectifs

- **Performance des soins** : Analyser la rentabilité par type de soin
- **Analyse des praticiens** : Évaluer les performances par praticien
- **Fidélisation des patients** : Mesurer le taux de rétention
- **Gestion des paiements** : Suivre les retards et créances
- **Analyse géographique** : Comparer les performances par clinique
- **Analyse temporelle** : Identifier les tendances et saisonnalités

## 🚀 Utilisation

### Prérequis
- Python 3.8+ (pour analyse exploratoire)
- Power BI Desktop
- Excel ou outil similaire pour visualiser les données

### Structure des Données

Le projet contient un fichier de données principal:
- `data/patients_mis_a_jour.xlsx` - Données complètes des soins et patients

### Analyse avec Jupyter Notebook

1. **Ouvrir le notebook**
```bash
jupyter notebook "Audit analytique d'un cabinet dentaire multi-sites.ipynb"
```

2. **Exécuter les cellules**
Le notebook contient:
- Nettoyage et préparation des données
- Analyse exploratoire (EDA)
- Calcul des KPI
- Visualisations Python (Matplotlib, Seaborn)

### Dashboard Power BI

**À venir**: Dashboard Power BI interactif pour visualiser:
- KPI en temps réel
- Performance par clinique
- Analyse des praticiens
- Tendances temporelles

## 📁 Structure du Projet

```
audit-cabinet-dentaire/
├── 📓 Audit analytique d'un cabinet dentaire multi-sites.ipynb  # Notebook Jupyter
├── 📋 requirements.txt           # Dépendances Python
├── 📖 README.md                 # Documentation
├── 🗂️ data/                     # Données
│   └── patients_mis_a_jour.xlsx
├── 📈 scripts/                  # Scripts utilitaires
└── 📊 visualisations/           # Graphiques générés
```

## 📊 KPIs Principaux

| KPI | Description | Formule |
|-----|-------------|---------|
| **CA Total** | Chiffre d'affaires global | `sum(montant_total_chf)` |
| **Taux de Rétention** | % patients fidèles | `patients_fidèles / total_patients * 100` |
| **Rentabilité Moyenne** | CA moyen par soin | `CA_total / nombre_actes` |
| **Taux de Retard** | % paiements en retard | `paiements_retard / total_paiements * 100` |
| **Soins/Patient** | Nombre moyen de soins | `total_soins / patients_uniques` |

## 🔧 Technologies Utilisées

- **Python** : Analyse de données et préparation
- **Pandas** : Manipulation et nettoyage de données
- **Matplotlib/Seaborn** : Visualisations exploratoires
- **Jupyter Notebook** : Analyse interactive
- **Power BI** : Dashboard business intelligence (en développement)

## 📈 Insights Clés

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

**Mohamed Ali Jama** - [@malijama](https://github.com/malijama)

---

⭐ **N'oubliez pas de donner une étoile au projet si vous l'aimez !**
