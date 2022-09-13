PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS "passwords" (
	"user_id"	INTEGER NOT NULL UNIQUE,
	"hashed"	TEXT NOT NULL,
	"salt"	TEXT NOT NULL,
	FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER,
	"username"	TEXT(64) NOT NULL UNIQUE,
	"fname"	TEXT(60),
	"lname"	TEXT(60),
	"logon_allowed"	BOOLEAN NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "sessions" (
	"user_id"	INTEGER NOT NULL,
	"token"	TEXT NOT NULL UNIQUE,
	"expiration"	TEXT NOT NULL,
	FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "categories" (
	"id"	INTEGER,
	"user_id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT),
	UNIQUE("user_id","name")
);
CREATE TABLE IF NOT EXISTS "receipts_junction" (
	"receipt_id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"item"	TEXT(200) NOT NULL,
	"price"	REAL NOT NULL,
	"quantity"	REAL NOT NULL,
	"comment"	TEXT(500),
	FOREIGN KEY("receipt_id") REFERENCES "receipts"("id") ON DELETE CASCADE,
	FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE,
	UNIQUE("receipt_id","item")
);
CREATE TABLE IF NOT EXISTS "receipts" (
	"id"	INTEGER,
	"user_id"	INTEGER NOT NULL,
	"store"	TEXT,
	"comment"	TEXT,
	"timestamp"	DATETIME,
	"created"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	"category"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE,
	FOREIGN KEY("category") REFERENCES "categories"("id") ON DELETE SET NULL
);
