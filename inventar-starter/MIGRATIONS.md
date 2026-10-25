# Datenbankmigration: Schadensbeschreibung bei der Rueckgabe

## Fachliche Idee

Bei der Rueckgabe eines Geraets soll eine kurze Beschreibung von Schaeden oder
Auffaelligkeiten festgehalten werden koennen.

## Entscheidung zum Attribut

- Tabelle: `assignment`
- Name: `return_damage_description`
- Typ: `VARCHAR(255)`
- Optionalitaet: optional (`NULL` ist erlaubt)

Der Name stellt den Bezug zur Rueckgabe her. Eine Laenge von 255 Zeichen reicht
fuer eine kurze Beschreibung aus. Das Feld ist optional, da nicht bei jeder
Rueckgabe ein Schaden vorliegt. `NULL` bedeutet dabei, dass keine
Schadensbeschreibung erfasst wurde.

## Migration ausfuehren

Die laufenden Container neu bauen und anschliessend die Migration ausfuehren:

```bash
docker compose up -d --build
docker compose run --rm api alembic upgrade head
```

Die Migration kann wieder rueckgaengig gemacht werden:

```bash
docker compose run --rm api alembic downgrade -1
```

## Ergebnis pruefen

Die Spalte kann direkt in PostgreSQL geprueft werden:

```bash
docker compose exec db psql -U appuser -d appdb -c \
  "SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'assignment' AND column_name = 'return_damage_description';"
```

Erwartet wird eine Spalte vom Typ `character varying`, bei der `is_nullable`
den Wert `YES` hat.
