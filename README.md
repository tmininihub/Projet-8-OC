# Projet 8 OpenClassrooms — Déploiement et monitoring d'un modèle de scoring

## Objectif

Mettre à disposition le modèle de scoring crédit développé dans le projet MLOps précédent, via une API FastAPI conteneurisée avec Docker. Le projet comprend des tests automatisés, un pipeline CI/CD et un suivi des données de production.

## API et stockage

L'API expose **`POST /Predict`** : à partir d'un identifiant client `SK_ID_CURR`, elle récupère ses données dans PostgreSQL, exécute la prédiction et retourne les probabilités d'accord et de refus du crédit.

Les informations sont enregistrées dans PostgreSQL :
- **`predictions_inputs`** : données utilisées pour les prédictions ;
- **`predictions_outputs`** : résultats des prédictions ;
- **`Metrics`** : temps de traitement, temps d'inférence, latence et utilisation CPU.

La documentation interactive de l'API est accessible via **`/docs`**.

## Tests et CI/CD

Les tests avec **pytest** vérifient notamment les paramètres de l'API et les résultats de prédiction.

Le workflow GitHub Actions (`.github/workflows/main.yml`) est prévu pour s'exécuter à chaque push sur `main` : installation des dépendances, tests, puis construction et lancement de l'image Docker si les tests réussissent. Il utilise un runner **self-hosted** et des secrets pour la connexion à PostgreSQL.

## Monitoring et Data Drift

- **`Metrics.ipynb`** et **`dashboard_monitoring.html`** : statistiques et distributions des métriques de l'API avec Evidently.
- **`Analyse_Drift.ipynb`** et **`drift_report.html`** : comparaison des données d'entraînement avec les données enregistrées en production.

Pour illustrer la détection du *Data Drift*, l'analyse sélectionne volontairement les clients appartenant aux 25 % de revenus les plus élevés en production. Le rapport indique **65 variables en drift sur 117 (55,56 %)**. Ce résultat illustre une différence de distribution sur ce sous-groupe et ne signifie pas que toute la production a naturellement dérivé.

### Comment interpréter ce résultat ?

- **55,56 % des variables** ne signifie ni 55,56 % des clients en drift, ni 55,56 % de perte de performance prédictive.
- Le groupe courant analysé ne contient que **19 clients**, contre **20 000 observations de référence** : le faible effectif impose de la prudence.
- Le changement de distribution des revenus est **attendu par construction** : le filtre retient uniquement les hauts revenus. Les autres alertes peuvent notamment venir de caractéristiques associées à ce profil, mais cette hypothèse exige une vérification variable par variable.
- **Aucun drift naturel de toute la production ni aucune dégradation de l'AUC ne sont démontrés** par cette seule expérience.
- Pour analyser les variables concernées, utiliser les graphiques du [rapport Evidently](drift_report.html). Le [notebook d'analyse](Analyse_Drift.ipynb) contient l'interprétation détaillée, les limites statistiques, les hypothèses et le plan de surveillance proposé.

**Pistes de vérification :** comparer aussi la production complète, examiner les distributions individuelles (dont `AMT_INCOME_TOTAL`), contrôler les variables rares ou constantes et mesurer l'impact sur les performances seulement lorsque des résultats réels sont disponibles.

## Fichiers principaux du dépôt

| Livrable | Fichier |
|---|---|
| API FastAPI | `main.py` |
| Dockerfile | `Dockerfile` |
| Tests | `test_main.py` |
| Pipeline CI/CD | `.github/workflows/main.yml` |
| Analyse du Data Drift | `Analyse_Drift.ipynb` |
| Historique des versions | Commits GitHub |

## Exécution

Pour exécuter l'API ou le pipeline, les fichiers nécessaires au modèle et à l'interface doivent être disponibles dans le dossier d'exécution.

La connexion à PostgreSQL utilise la variable d'environnement `URLBDD` ; les identifiants ne doivent pas être ajoutés au dépôt.
