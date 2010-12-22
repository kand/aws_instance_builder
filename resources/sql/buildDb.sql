CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE status (
    "id" INTEGER PRIMARY KEY,
    "value" TEXT,
    "posted" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX "status_id" on status (id ASC);
