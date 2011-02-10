CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE status (
    "id" INTEGER PRIMARY KEY,
    "value" TEXT,
    "posted" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX "status_id" on status (id ASC);
CREATE TABLE "pipelineFiles" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" TEXT NOT NULL,
    "path" TEXT NOT NULL,
    "description" TEXT NOT NULL
);
