# Crypto Data Pipeline with Hadoop, Airflow, and Docker

## 📌 Objectifs du Projet

Ce projet vise à construire un pipeline complet de traitement des données de cryptomonnaies en utilisant des outils Big Data. L’objectif est de récupérer, transformer, stocker et analyser les données de prix et de volume en temps quasi-réel.

### 🛠️ Étapes principales :

### 1️⃣ Ingestion des données :
- Récupération quotidienne des prix et volumes des cryptomonnaies via l’API CoinGecko.

### 2️⃣ Stockage dans un Data Lake :
- Stockage des données brutes dans HDFS (Hadoop Distributed File System).

### 3️⃣ Transformation et agrégation (MapReduce en Python) :
- Nettoyage des données (validation des champs, gestion des valeurs manquantes).
- Calcul de métriques : prix moyen, minimum, maximum, volume moyen, etc.
- Génération d’une sortie structurée au format CSV ou Parquet.

### 4️⃣ Chargement dans HBase :
- Insertion des données traitées pour des requêtes rapides (ex : recherche par ID de crypto et date).

### 5️⃣ Orchestration avec Apache Airflow :
- Gestion de la planification et de l'exécution automatisée du pipeline.

### 📚 API Source : CoinGecko API

---

## 🏗️ Architecture & Conception du Data Lake Hadoop

           ┌────────────────────────┐
           │       CoinGecko API    │
           └────────────┬───────────┘
                        │
     ┌───────────────────┴────────────────────┐
     │     DAG d’Ingestion (Airflow)          │
     │ (Appel de l’API + stockage dans HDFS)  │
     └───────────────────┬────────────────────┘
                        │
              Zone Brute (Raw) dans HDFS
                        ▼
     ┌───────────────────┴────────────────────┐
     │   DAG de Traitement (Airflow + MR)     │
     │ (MapReduce en Python : transformation  │
     │  et agrégation)                        │
     └───────────────────┬────────────────────┘
                        │
            Zone Traité/Structuré dans HDFS
                        ▼
        ┌───────────────────────────────────┐
        │               HBase              │
        │ (pour requêtes rapides/analyses) │
        └───────────────────────────────────┘
                        │
                        ▼
                    Analytics / BI

---

## 🐳 Déploiement avec Docker & Docker Compose

Le projet est entièrement conteneurisé avec Docker pour simplifier le déploiement. Les services sont orchestrés avec Docker Compose pour faciliter la mise en place de l’environnement.

### 📂 Structure des conteneurs :
- **Hadoop (HDFS, YARN, MapReduce)**
- **HBase**
- **Apache Airflow** (Scheduler, Webserver, Worker)
- **Python** (scripts de traitement des données)

### ▶️ Lancement du projet :

#### 1️⃣ Cloner le dépôt :
```bash
git clone <URL_REPO>
cd <nom_du_projet>
```

#### 1️⃣ Lancer les conteneurs :
```
docker-compose up -d
```
#### 3️⃣ Accéder à l'interface Airflow :
URL : http://localhost:8080

#### 4️⃣ Visualiser HBase :
Utiliser hbase shell à l’intérieur du conteneur pour interroger les données traitées.

#### 🛑 Arrêter les conteneurs :
```
docker-compose down
```
