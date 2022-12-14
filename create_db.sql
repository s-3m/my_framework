PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

CREATE TABLE films (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32), actor VARCHAR (32), director VARCHAR (32), genre VARCHAR (32));

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;