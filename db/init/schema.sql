CREATE TABLE
  IF NOT EXISTS raw_exchange_rates (
    id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL,
    country VARCHAR(50) DEFAULT 'Sri Lanka' NOT NULL,
    last_updated TIMESTAMP NOT NULL,
    source_url VARCHAR(255),
    currency_name VARCHAR(50) NOT NULL,
    currency_code VARCHAR(10) NOT NULL,
    tt_buying FLOAT,
    tt_selling FLOAT,
    draft_buying FLOAT,
    draft_selling FLOAT,
    cheques_buying FLOAT,
    cheques_selling FLOAT,
    currency_buying FLOAT,
    currency_selling FLOAT,
    other_buying FLOAT,
    other_selling FLOAT,
    notes TEXT,
    tag VARCHAR(50),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    correlation_id VARCHAR(100)
  );