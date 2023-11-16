CREATE TABLE "mint" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "tx_hash" VARCHAR(66) NOT NULL,
    "token0" VARCHAR(66) NOT NULL,
    "token1" VARCHAR(66) NOT NULL,
    "pool_address" VARCHAR(66) NOT NULL,
    "pool_fee" INT NOT NULL,
    "timestamp" BIGINT NOT NULL
);
CREATE INDEX "idx_mint_timestamp" ON "mint" ("timestamp");
CREATE INDEX "idx_mint_token0_token1" ON "mint" ("token0", "token1");