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

CREATE TABLE IF NOT EXISTS occurrences(
occurrence_id TEXT PRIMARY KEY,
asset_id TEXT NOT NULL,
path TEXT NOT NULL,
scan_id TEXT NOT NULL,
FOREIGN KEY(asset_id) REFERENCES assets(asset_id)
);

CREATE INDEX IF NOT EXISTS idx_occurrences_asset_scan
ON occurrences(asset_id, scan_id);

-- TODO: normalize tags into separate table
-- tables:
-- assets
--tags
--asset_tags (many-to-many)