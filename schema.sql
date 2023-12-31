DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
    id TEXT PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    original_url TEXT NOT NULL,
    short_url TEXT,
    expiry TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+10 years')),
    clicks INTEGER NOT NULL DEFAULT 0,
    clicks_last_24h INTEGER NOT NULL DEFAULT 0,
    clicks_past_week INTEGER NOT NULL DEFAULT 0
);
