## Les données de Kayak

Les données du Datalake (archivées dans un compartiment (Bucket) S3 d'AWS) et du Datawarehouse (base de données PostgreSQL  ligne chez Neon) sont également présentes dans le repertoire de ce fichier.

| Fichier | Description | type |
| --------|-------------|------|
| kayak.csv | liste et données sur les sites d'interêt | Data Lake
| kayak.json | liste des hôtels pour le projet issus du site Booking | Data Lake
| jedha_kayak.sql | sauvegarde (dump ou backup) au format sql de la base de données PostgreSQL du projet | Data Warehouse |
