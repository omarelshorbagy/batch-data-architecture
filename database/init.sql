CREATE TABLE IF NOT EXISTS ml_ready_data (
    id SERIAL PRIMARY KEY,
    date DATE,
    domain VARCHAR(100),
    location VARCHAR(100),
    value FLOAT,
    transaction_count INT
);
