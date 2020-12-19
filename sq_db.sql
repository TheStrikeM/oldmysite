CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
login text NOT NULL,
email text NOT NULL,
password text NOT NULL,
time integer NOT NULL
);