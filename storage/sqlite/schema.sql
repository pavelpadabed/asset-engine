CREATE TABLE IF NOT EXISTS assets(
asset_id TEXT PRIMARY KEY,
path TEXT NOT NULL,
asset_type TEXT NOT NULL,
file_hash TEXT NOT NULL,
source TEXT NOT NULL,
file_size INTEGER NOT NULL,
modified_time TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_assets_file_hash
ON assets(file_hash);