CREATE TABLE "swap_record" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "tx_hash" VARCHAR(100) NOT NULL UNIQUE,
    "sender" VARCHAR(100) NOT NULL,
    "token_in_address" VARCHAR(100) NOT NULL,
    "token_in_volume" VARCHAR(100) NOT NULL,
    "token_in_usd_amount" VARCHAR(100) NOT NULL,
    "token_out_address" VARCHAR(100) NOT NULL,
    "token_out_volume" VARCHAR(100) NOT NULL,
    "token_out_usd_amount" VARCHAR(100) NOT NULL,
    "timestamp" BIGINT NOT NULL
);
CREATE INDEX "idx_swap_record_sender" ON "swap_record" ("sender");
CREATE INDEX "idx_swap_record_sender_timestamp" ON "swap_record" ("sender", "timestamp");