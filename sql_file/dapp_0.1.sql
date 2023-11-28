CREATE TABLE "network" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "chain_id" INT NOT NULL UNIQUE,
    "name" VARCHAR(128) NOT NULL,
    "native_currency" VARCHAR(200) NOT NULL,
    "tbd_token" VARCHAR(10) NOT NULL,
    "logo" VARCHAR(200) NULL,
    "technology" VARCHAR(100) NULL,
    "description" VARCHAR(1000) NULL,
    "rpc" VARCHAR(500) NULL,
    "block_explorer" VARCHAR(100) NULL,
    "milestones" TEXT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE "dapp" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(128) NOT NULL,
    "route" VARCHAR(200) NULL,
    "tbd_token" VARCHAR(10) NOT NULL,
    "logo" VARCHAR(100) NULL,
    "default_chain_id" INT NULL,
    "description" VARCHAR(1000) NULL,
    "favorite" INT NULL DEFAULT 0,
    "recommend" BOOL NULL DEFAULT False,
    "recommend_icon" VARCHAR(100) NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX "idx_dapp_create" ON "dapp" ("created_at");
CREATE INDEX "idx_dapp_update" ON "dapp" ("updated_at");


CREATE TABLE "ad" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "category_id" INT NOT NULL,
    "category"  VARCHAR(50) NOT NULL,
    "ad_link" VARCHAR(200) NULL,
    "ad_images" TEXT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE UNIQUE INDEX "idx_ad_category_id" ON "ad" ("category","category_id");
CREATE INDEX "idx_ad_category_update" ON "ad" ("category","updated_at");
CREATE INDEX "idx_ad_update" ON "ad" ("updated_at");


CREATE TABLE "category" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "category"."name" IS 'Bridge,Dex,Lending,Liquidity,Staking,Yield';

CREATE TABLE "dapp_favorite" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "account_id" INT NOT NULL,
    "dapp_id" INT NOT NULL,
    "is_favorite" BOOL NOT NULL DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX "idx_dapp_favorite_dapp" ON "dapp_category" ("dapp_id","created_at");
CREATE UNIQUE INDEX "idx_dapp_favorite_account_id" ON "dapp_favorite" ("account_id","dapp_id");


CREATE TABLE "dapp_relate" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "dapp_id" INT NOT NULL,
    "dapp_id_relate" INT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dapp_id) REFERENCES dapp (id)
);
CREATE INDEX "idx_dapp_relate_dapp_id" ON "dapp_relate" ("dapp_id");
CREATE UNIQUE INDEX "idx_dapp_relate_dapp_relate" ON "dapp_relate" ("dapp_id","dapp_id_relate");


CREATE TABLE "dapp_network" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "dapp_id" INT NOT NULL,
    "network_id" INT NOT NULL,
    "dapp_src" VARCHAR(200) NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dapp_id) REFERENCES dapp (id)
);
CREATE INDEX "idx_dapp_network_network_id" ON "dapp_network" ("network_id");
CREATE INDEX "idx_dapp_network_dapp_id" ON "dapp_network" ("dapp_id");
CREATE UNIQUE INDEX "idx_dapp_network_dapp_network" ON "dapp_network" ("dapp_id","network_id");


CREATE TABLE "dapp_category" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "dapp_id" INT NOT NULL,
    "category_id" INT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dapp_id) REFERENCES dapp (id)
);
CREATE INDEX "idx_dapp_category_category_id" ON "dapp_category" ("category_id");
CREATE UNIQUE INDEX "idx_dapp_category_dapp_id" ON "dapp_category" ("dapp_id","category_id");