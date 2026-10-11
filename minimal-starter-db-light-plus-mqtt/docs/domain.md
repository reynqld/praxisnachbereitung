
# Datenmodell – Geräteausleihe

## ER-Diagramm

```mermaid
erDiagram
    Person ||--o{ Assignment : borrows
    Device ||--o{ Assignment : is_assigned_in

    Person {
        int person_id PK
        string name
        string email
        string department
    }

    Device {
        int device_id PK
        string inventory_number UK
        string type
        string model
        string status
    }

    Assignment {
        int assignment_id PK
        int person_id FK
        int device_id FK
        datetime borrowed_at
        datetime returned_at
    }
```

## Fachregeln

1. Eine Person kann mehrere Geräte gleichzeitig ausleihen.
2. Ein Gerät kann über die Zeit mehrfach ausgeliehen werden.
3. Ein Gerät darf maximal eine aktive Ausleihe haben.
4. Eine Ausleihe gilt als aktiv, wenn `returned_at = NULL` ist.
5. Das Rückgabedatum darf nicht vor dem Ausleihdatum liegen.
6. Jede Ausleihe gehört genau einer Person und einem Gerät.
7. Jede Inventarnummer muss eindeutig sein.
8. Geräte dürfen nur ausgeliehen werden, wenn sie verfügbar sind.
9. Vergangene Ausleihen bleiben für die Historie gespeichert.
