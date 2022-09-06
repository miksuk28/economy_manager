PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS receipts (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	store TEXT,
	comment TEXT,
	timestamp DATETIME,
	created DATETIME DEFAULT CURRENT_TIMESTAMP,
	category INTEGER,

	FOREIGN KEY (category) REFERENCES categories (id)
);

CREATE TABLE IF NOT EXISTS receipts_junction (
	receipt_id INTEGER NOT NULL,
	item TEXT(200) NOT NULL,
	price REAL NOT NULL,
	quantity REAL NOT NULL,
	comment TEXT(500),

	UNIQUE(receipt_id, item),
	FOREIGN KEY (receipt_id) REFERENCES receipts (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS categories (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL UNIQUE
);
