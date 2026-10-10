# Praxisnachbereitung SS25 – Tag 1: ETL mit Excel

## Inhalt
- excel/Geraete.csv, Ausleihen.csv, Mitarbeiter.csv – Rohdaten
- excel/Auswertung.xlsx – Import, Bereinigung, Gesamttabelle, Pivots
- excel/Gesamt_bereinigt.csv – Export der Gesamttabelle
- excel/miau.py mit python proof of concept

## Arbeitsablauf
1. Import der CSVs per Power Query
2. Bereinigung: leere Zeilen entfernt, Datentypen gesetzt
3. Merge: Ausleihen ⟕ Geraete (Gerätenummer) ⟕ Mitarbeiter (Mitarbeiter-ID)
4. Auswertung: Pivots nach Gerätetyp und Standort, Wert verfügbarer Geräte
5. Visualisierung mithilfe von unterschiedlichen Diagrammtypen 
6. Export als CSV und Einlesen mit Python (pandas)

## Probleme & Lösungen
- Datum korrekt formatiert 
- Leere Zeilen entfern 

## Erkenntnisse
- Häufigster Gerätetyp bei Ausleihen: …
- Auffällige Verteilung nach Standort: …
- Achten auf art der separieriung der values in csv und Umlaute