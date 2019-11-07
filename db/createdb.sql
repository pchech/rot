CREATE TABLE tickets_data (
    id SERIAL,
    company_id TEXT,
    price NUMERIC,
    departure_place TEXT,
    arrival_place TEXT,
    departure_date TIMESTAMP WITHOUT TIME ZONE,
    arrival_date TIMESTAMP WITHOUT TIME ZONE,
    event_time TIMESTAMP WITHOUT TIME ZONE,
    url TEXT
);