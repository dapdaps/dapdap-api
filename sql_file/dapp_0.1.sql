CREATE TABLE "network" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "chain_id" INT NOT NULL UNIQUE,
    "name" VARCHAR(128) NOT NULL,
    "technology" VARCHAR(100) NULL,
    "description" VARCHAR(1000) NULL,
    "native_token" VARCHAR(50) NULL,
    "milestones" TEXT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE "dapp" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(128) NOT NULL,
    "description" VARCHAR(1000) NULL,
    "native_token" VARCHAR(50) NULL,
    "favorite" INT NULL DEFAULT 0,
    "recommend" BOOL NULL DEFAULT False,
    "recommend_icon" VARCHAR(100) NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE "category" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "category"."name" IS 'Bridge,Dex,Lending,Liquidity,Staking,Yield';


CREATE TABLE "dapp_favorite" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "account_id" INT NOT NULL,
    "dapp_id" INT NOT NULL,
    "is_favorite" BOOL NOT NULL DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE UNIQUE INDEX "idx_dapp_favorite_account_id" ON "dapp_favorite" ("account_id","dapp_id");


CREATE TABLE "dapp_relate" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "dapp_id" INT NOT NULL,
    "dapp_id_relate" INT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX "idx_dapp_relate_dapp_id" ON "dapp_relate" ("dapp_id");


CREATE TABLE "dapp_network" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "dapp_id" INT NOT NULL,
    "network_id" INT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX "idx_dapp_network_network_id" ON "dapp_network" ("network_id");
CREATE INDEX "idx_dapp_network_dapp_id" ON "dapp_network" ("dapp_id");


CREATE TABLE "dapp_category" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "dapp_id" INT NOT NULL,
    "category_id" INT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX "idx_dapp_category_category_id" ON "dapp_category" ("category_id");
CREATE UNIQUE INDEX "idx_dapp_category_dapp_id" ON "dapp_category" ("dapp_id","category_id");