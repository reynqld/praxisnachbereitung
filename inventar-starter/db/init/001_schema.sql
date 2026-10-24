CREATE TABLE department (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE person (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    department_id   BIGINT NOT NULL REFERENCES department(id),
    name            VARCHAR(200) NOT NULL
);

CREATE TABLE device_type (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE location (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE device (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    serial_number   VARCHAR(100) NOT NULL UNIQUE,
    device_type_id  BIGINT NOT NULL REFERENCES device_type(id),
    location_id     BIGINT NOT NULL REFERENCES location(id)
);

CREATE TABLE assignment (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    device_id   BIGINT NOT NULL REFERENCES device(id),
    person_id   BIGINT NOT NULL REFERENCES person(id),
    issued_at   TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    returned_at TIMESTAMPTZ
);


INSERT INTO department (name) VALUES
    ('IT'),
    ('Logistik'),
    ('Verwaltung');

INSERT INTO device_type (name) VALUES
    ('Laptop'),
    ('Monitor'),
    ('Handscanner');

INSERT INTO location (name) VALUES
    ('Gebäude E'),
    ('Gebäude F'),
    ('Gebäude H');

INSERT INTO person (department_id, name) VALUES
    ((SELECT id FROM department WHERE name = 'IT'), 'Anna Schmidt'),
    ((SELECT id FROM department WHERE name = 'Logistik'), 'Mehmet Yilmaz'),
    ((SELECT id FROM department WHERE name = 'Verwaltung'), 'Laura Becker'),
    ((SELECT id FROM department WHERE name = 'IT'), 'Jonas Weber');

INSERT INTO device (serial_number, device_type_id, location_id) VALUES
    ('LT-2026-001',
     (SELECT id FROM device_type WHERE name = 'Laptop'),
     (SELECT id FROM location WHERE name = 'Gebäude E')),
    ('LT-2026-002',
     (SELECT id FROM device_type WHERE name = 'Laptop'),
     (SELECT id FROM location WHERE name = 'Gebäude F')),
    ('MON-2026-001',
     (SELECT id FROM device_type WHERE name = 'Monitor'),
     (SELECT id FROM location WHERE name = 'Gebäude E')),
    ('MON-2026-002',
     (SELECT id FROM device_type WHERE name = 'Monitor'),
     (SELECT id FROM location WHERE name = 'Gebäude H')),
    ('SCAN-2026-001',
     (SELECT id FROM device_type WHERE name = 'Handscanner'),
     (SELECT id FROM location WHERE name = 'Gebäude F'));

INSERT INTO assignment (device_id, person_id) VALUES
    ((SELECT id FROM device WHERE serial_number = 'LT-2026-001'),
     (SELECT id FROM person WHERE name = 'Anna Schmidt')),
    ((SELECT id FROM device WHERE serial_number = 'SCAN-2026-001'),
     (SELECT id FROM person WHERE name = 'Mehmet Yilmaz')),
    ((SELECT id FROM device WHERE serial_number = 'MON-2026-001'),
     (SELECT id FROM person WHERE name = 'Jonas Weber')),
    ((SELECT id FROM device WHERE serial_number = 'LT-2026-002'),
     (SELECT id FROM person WHERE name = 'Laura Becker'));
