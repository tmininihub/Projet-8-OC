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
- **`Minini_Tristan_n6_AnalyseDrift_112026.ipynb`** et **`drift_report.html`** : comparaison des données d'entraînement avec les données enregistrées en production.

Pour illustrer la détection du *Data Drift*, l'analyse sélectionne volontairement les clients appartenant aux 25 % de revenus les plus élevés en production. Le rapport indique **65 variables en drift sur 117 (55,56 %)**. Ce résultat illustre une différence de distribution sur ce sous-groupe et ne signifie pas que toute la production a naturellement dérivé.

## Fichiers principaux du dépôt

| Livrable | Fichier |
|---|---|
| API FastAPI | `Minini_Tristan_n2_ScriptAPI_112026.py` |
| Dockerfile | `Minini_Tristan_n3_DockerFile_112026.dockerfile` |
| Tests | `Minini_Tristan_n4_Tests_112026.py` |
| Pipeline CI/CD | `.github/workflows/main.yml` |
| Analyse du Data Drift | `Minini_Tristan_n6_AnalyseDrift_112026.ipynb` |
| Historique des versions | Commits GitHub |

## Exécution

Le pipeline et le Dockerfile font référence aux noms de fichiers standards `main.py`, `test_main.py` et `Dockerfile`. **Les fichiers déposés ici portent des noms de livrables** : il faut leur redonner ces noms dans le dossier d'exécution, avec les fichiers nécessaires au modèle et à l'interface, avant de lancer l'API ou le pipeline.

La connexion à PostgreSQL utilise la variable d'environnement `URLBDD` ; les identifiants ne doivent pas être ajoutés au dépôt.
