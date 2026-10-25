# Grades Starter – Notizen

## Projektstruktur

- `backend/app/main.py` – Enthält die FastAPI-Routen, Datenbankabfragen und die Verbindung zu den Templates.
- `backend/app/db.py` – Stellt die Verbindung zu PostgreSQL her.
- `backend/app/models.py` – Beschreibt die Datenmodelle für Studierende, Module und Noten.
- `backend/app/mqtt_integration.py` – Empfängt neue Noten über MQTT und speichert sie in der Datenbank.
- `backend/app/templates/` – Enthält die HTML-Templates für Startseite, Studierende und Noten.
- `db/init/001_schema.sql` – Erstellt die Tabellen und fügt Beispieldaten ein.
- `docker-compose.yml` – Startet API, PostgreSQL und MQTT.

## Formulare

- Formulare stehen in den HTML-Templates und senden ihre Daten per POST an FastAPI-Routen.
- FastAPI liest die Eingaben mit `Form(...)` aus und kann sie mit Pydantic-Modellen prüfen.
- Die Route führt eine SQL-Abfrage aus, um Daten anzulegen, zu ändern oder zu löschen.
- Nach dem Speichern wird meist mit HTTP 303 zur passenden Seite weitergeleitet.
- Das Notenformular nutzt HTMX: Nach dem Speichern wird nur die Notenliste aktualisiert, nicht die ganze Seite.

## Templates

- FastAPI bindet den Ordner `backend/app/templates` mit Jinja ein.
- Eine Route rendert ein Template mit `TemplateResponse` und übergibt Daten, zum Beispiel Studierende oder Noten.
- Jinja zeigt Werte mit `{{ ... }}` an und kann mit Schleifen und Bedingungen Listen darstellen.
- `grades/index.html` bindet `grades/_list.html` ein. Dieses Teil-Template zeigt die Notentabelle und kann separat aktualisiert werden.

## Einfache CRUD-Flows

- **Studierende anlegen:** `POST /students` speichert die Formularwerte in der Tabelle `student`.
- **Studierende anzeigen:** `GET /students` lädt die Studierenden und zeigt sie als Liste an.
- **Studierende bearbeiten:** Die Edit-Seite lädt einen Studierenden; `POST /students/{student_id}/edit` speichert Änderungen.
- **Studierende löschen:** `POST /students/{student_id}/delete` löscht den Studierenden. Zugehörige Noten werden durch die Datenbank ebenfalls gelöscht.
- **Module anlegen:** `POST /modules` speichert ein Modul. Bearbeiten und Löschen von Modulen ist nicht umgesetzt.
- **Noten anzeigen:** `GET /grades` zeigt die Noten eines ausgewählten Studierenden.
- **Noten anlegen:** `POST /grades/htmx` speichert eine Note und liefert die aktualisierte Notenliste zurück.
- **Noten exportieren:** `GET /grades.csv` lädt alle Noten als CSV herunter.

