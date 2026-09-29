CREATE TABLE IF NOT EXISTS prices (
    ticker TEXT NOT NULL, date TEXT NOT NULL,
    open REAL, high REAL, low REAL, close REAL, volume REAL,
    PRIMARY KEY (ticker, date)
);
CREATE TABLE IF NOT EXISTS ecb_rates (
    date TEXT PRIMARY KEY, rate REAL
);
CREATE TABLE IF NOT EXISTS indicators (
    ticker TEXT NOT NULL, date TEXT NOT NULL,
    ret REAL, vol_30d REAL, vol_90d REAL, drawdown REAL, beta_90d REAL,
    PRIMARY KEY (ticker, date)
);
CREATE TABLE IF NOT EXISTS vol_predictions (
    ticker TEXT NOT NULL, date TEXT NOT NULL, horizon INTEGER NOT NULL,
    model TEXT NOT NULL, predicted_vol REAL,
    PRIMARY KEY (ticker, date, horizon, model)
);
