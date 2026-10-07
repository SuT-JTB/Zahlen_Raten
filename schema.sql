CREATE TABLE IF NOT EXISTS highscore (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT    NOT NULL,
    versuche  INTEGER NOT NULL,
    zeitpunkt TEXT    NOT NULL
);
