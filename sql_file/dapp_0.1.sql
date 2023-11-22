CREATE TABLE "chain" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "network_id" VARCHAR(128) NOT NULL UNIQUE,
    "technology" VARCHAR(100) NOT NULL,
    "description" VARCHAR(1000),
    "native_token" VARCHAR(50),
    "milestones" TEXT
);

CREATE TABLE "dapp" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "template" VARCHAR(255) NOT NULL,
    "description" VARCHAR(1000),
    "favorite" INT NOT NULL,
    "native_token" VARCHAR(50),
    "quest" BOOL   DEFAULT False,
    "chains" VARCHAR(300) NOT NULL,
    "functions" VARCHAR(200) NOT NULL,
    "show" BOOL NOT NULL  DEFAULT False
);
CREATE INDEX "idx_dapp_templat" ON "dapp" ("template");