PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

CREATE TABLE genres (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32));

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;