CREATE TABLE "chain_token_swap" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "chain_id" BIGINT NOT NULL,
    "token_in" VARCHAR(100) NOT NULL,
    "token_in_decimal" INT NOT NULL,
    "token_in_name" VARCHAR(100) NOT NULL,
    "token_out" VARCHAR(100) NOT NULL,
    "token_out_decimal" INT NOT NULL,
    "token_out_name" VARCHAR(100) NOT NULL,
    "quote_price" VARCHAR(255),
    "quote_fee" INT
    "updated_timestamp" INT
);