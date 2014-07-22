# Themenstadtscraper

Das ist ein kleines Pythontool, mit dem man den Themenstadtplan Dresden scrapen und in eine eigene Postgres Datenbank übertragen kann.

## Voraussetzungen

Python (getestet auf Python 3.3.3), außerdem einige Pythondependencies (installierbar über `pip install -r requirements.txt`), außerdem PostgreSQL >= 9.2 und PostGIS.

## Nutzung

Vor der ersten Benutzung muss eine Datenbank mit einer Tabelle angelegt werden (siehe `database.sql`). Der Scrapingvorgang kann mit `./themenstadtscraper.py` gestartet werden. *Hinweis:* Der Server vom Themenstadtplan ist nicht der schnellste und die Methode, mit der die Daten herausgeholt werden, ist ziemlich brute force. Es dauert also schon durchaus mehrere Stunden, um die Daten zu bekommen.
