CREATE TABLE "mint" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "tx_hash" VARCHAR(66) NOT NULL,
    "token0" VARCHAR(66) NOT NULL,
    "token1" VARCHAR(66) NOT NULL,
    "pool_address" VARCHAR(66) NOT NULL,
    "pool_fee" INT NOT NULL,
    "timestamp" BIGINT NOT NULL,
    "chain_id" INT NOT NULL DEFAULT 0,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
);
CREATE INDEX "idx_mint_timestamp" ON "mint" ("timestamp");
CREATE INDEX "idx_mint_token0_token1" ON "mint" ("token0", "token1");