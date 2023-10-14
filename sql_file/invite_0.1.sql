DROP TABLE IF EXISTS aerich;
CREATE TABLE "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);

CREATE TABLE "group_info" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(100) NOT NULL UNIQUE,
    "title" VARCHAR(255) NOT NULL
);
COMMENT ON COLUMN "group_info"."name" IS 'group name';
COMMENT ON COLUMN "group_info"."title" IS 'group title';

CREATE TABLE "user_info" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "address" VARCHAR(50) NOT NULL UNIQUE,
    "account_info" VARCHAR(25),
    "chain_type" VARCHAR(5) NOT NULL  DEFAULT 'eth'
);
COMMENT ON COLUMN "user_info"."address" IS 'user''s evm address';
COMMENT ON COLUMN "user_info"."chain_type" IS 'ETH: eth\nOTHER: other';

CREATE TABLE "group_info_user_info" (
    "group_info_id" BIGINT NOT NULL,
    "userinfo_id" BIGINT NOT NULL
);


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

CREATE TABLE "activity_config" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "title" VARCHAR(255) NOT NULL,
    "status" SMALLINT NOT NULL  DEFAULT 1,
    "start_date" DATE NOT NULL,
    "end_date" DATE NOT NULL,
    "description" TEXT NOT NULL
);
COMMENT ON COLUMN "activity_config"."status" IS 'PRE_START: 1\nIN_PROGRESS: 2\nEND: 3';

CREATE TABLE "activity_report" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "chain_id" VARCHAR(11) NOT NULL  DEFAULT 'Other',
    "report_type" VARCHAR(5) NOT NULL,
    "tx_count" INT NOT NULL  DEFAULT 0,
    "activity_id" BIGINT NOT NULL,
    "group_id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL
);
COMMENT ON COLUMN "activity_report"."chain_id" IS 'ALL: all\nMantle: Mantle\nBase: Base\nzkEVM: zkEVM\nMAINNET: MAINNET\nArbitrumOne: ArbitrumOne\nArbitrum: Arbitrum\nOther: Other';
COMMENT ON COLUMN "activity_report"."report_type" IS 'USER: user\nGROUP: group\nOTHER: other';

CREATE TABLE "task_config" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "task_name" VARCHAR(255) NOT NULL,
    "network" VARCHAR(11) NOT NULL  DEFAULT 'all',
    "action_type" VARCHAR(8) NOT NULL  DEFAULT 'Other',
    "position" INT NOT NULL  DEFAULT 0,
    "task_type" VARCHAR(5) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True
);
COMMENT ON COLUMN "task_config"."network" IS 'ALL: all\nMantle: Mantle\nBase: Base\nzkEVM: zkEVM\nMAINNET: MAINNET\nArbitrumOne: ArbitrumOne\nArbitrum: Arbitrum\nOther: Other';
COMMENT ON COLUMN "task_config"."action_type" IS 'Deposit: Deposit\nRedeem: Redeem\nRepay: Repay\nWithdraw: Withdraw\nSupply: Supply\nMint: Mint\nBridge: Bridge\nSwap: Swap\nOther: Other';
COMMENT ON COLUMN "task_config"."task_type" IS 'like daily task monthly task';

CREATE TABLE "user_integral" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "integral" INT NOT NULL  DEFAULT 0,
    "user_id" BIGINT NOT NULL
);
COMMENT ON COLUMN "user_integral"."integral" IS 'user‘s integral';

CREATE TABLE "user_task_result" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "status" SMALLINT NOT NULL  DEFAULT 1,
    "task_id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL
);
COMMENT ON COLUMN "user_task_result"."status" IS 'INIT: 1\nDONE: 2\nFAIL: 3';


