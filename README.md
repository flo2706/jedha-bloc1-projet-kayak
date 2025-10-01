# jedha-bloc1-projet-kayak

# 🌍 Projet Kayak — Infrastructure de Données

## 📖 Contexte du projet

Ce projet a été réalisé dans le cadre du **Bootcamp Jedha Fullstack (Bloc 1 — Data Engineering)**.  
L’objectif est d’aider l’équipe marketing de **Kayak** à recommander les meilleures destinations de voyage en France, en se basant sur :

- les **conditions météorologiques**,
- la **disponibilité et les notes des hôtels**.

Le projet couvre l’ensemble d’une chaîne de traitement de données (**pipeline**) :

1. Extraction des données (scraping + API)
2. Transformation et nettoyage des données
3. Chargement dans un **Data Lake (S3)** et un **Data Warehouse (PostgreSQL sur AWS RDS)**
4. Visualisation des meilleures destinations et hôtels avec **Plotly**

---

## 🛠️ Stack technique

- **Python** : Scrapy, Requests, Pandas, Psycopg2, Asyncio
- **APIs** : OpenWeather OneCall 3.0, Nominatim (OpenStreetMap)
- **Base de données** : PostgreSQL (hébergée sur AWS RDS)
- **Data Lake** : AWS S3
- **ETL** : Scripts Python
- **Visualisation** : Plotly

---

⚠️ **Important :**

- Les fichiers complets (scraping et CSV) **ne sont pas inclus** pour des raisons de **RGPD**.
- Des **échantillons** (`sample/`) de 5 lignes sont fournis pour tester le pipeline.

---

## ⚙️ Installation et configuration

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-utilisateur/jedha-bloc1-projet-kayak.git
cd jedha-bloc1-projet-kayak

## AWS
AWS_KEY=VOTRE_AWS_KEY
AWS_SECRET_KEY=VOTRE_AWS_SECRET_KEY

# OpenWeather
OPENWEATHER_API_KEY=VOTRE_CLE_API

# PostgreSQL
DBNAME=postgres
USERNAME=mon_utilisateur
PASSWORD=mon_mot_de_passe
HOSTNAME=mon-instance-rds.amazonaws.com
PORT=5432

# User-Agent (obligatoire pour Nominatim)
USER_AGENT=KayakTripPlanner/1.0 (votre_email@example.com)
```
