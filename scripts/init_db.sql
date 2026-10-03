CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    telegram_chat_id VARCHAR(64),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS monitors (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    url VARCHAR(512) NOT NULL,
    name VARCHAR(100) NOT NULL,
    check_interval_seconds INT DEFAULT 60,
    is_active BOOLEAN DEFAULT TRUE,
    last_status_code INT,
    last_response_time_ms NUMERIC(8, 2),
    is_up BOOLEAN DEFAULT TRUE,
    ssl_valid_until TIMESTAMP WITH TIME ZONE,
    ssl_issuer VARCHAR(255),
    last_checked_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ping_logs (
    id BIGSERIAL PRIMARY KEY,
    monitor_id INT NOT NULL REFERENCES monitors(id) ON DELETE CASCADE,
    status_code INT,
    response_time_ms NUMERIC(8, 2),
    is_up BOOLEAN NOT NULL,
    error_message TEXT,
    checked_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_monitors_user_id ON monitors(user_id);
CREATE INDEX IF NOT EXISTS idx_ping_logs_monitor_time ON ping_logs(monitor_id, checked_at DESC);
