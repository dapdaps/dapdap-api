DROP TABLE IF EXISTS user_address;
CREATE TABLE "user_address" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "address" VARCHAR(25) NOT NULL UNIQUE,
    "chain_type" VARCHAR(5) NOT NULL  DEFAULT 'eth'
);
COMMENT ON COLUMN "user_address"."address" IS 'user''s evm address';
COMMENT ON COLUMN "user_address"."chain_type" IS 'ETH: eth\nOTHER: other';

DROP TABLE IF EXISTS invite_code_pool;
CREATE TABLE "invite_code_pool" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "code" VARCHAR(25) NOT NULL UNIQUE,
    "creator_type" SMALLINT NOT NULL  DEFAULT 1,
    "is_used" BOOL NOT NULL  DEFAULT False,
    "creator_user_id" BIGINT,
    "used_user_id" BIGINT
);
COMMENT ON COLUMN "invite_code_pool"."creator_type" IS 'user type';
COMMENT ON COLUMN "invite_code_pool"."is_used" IS 'code is used';
COMMENT ON COLUMN "invite_code_pool"."creator_user_id" IS 'address create invite code';
COMMENT ON COLUMN "invite_code_pool"."used_user_id" IS 'address used invite code';

DROP TABLE IF EXISTS aerich;
CREATE TABLE "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
