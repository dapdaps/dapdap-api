CREATE TABLE "quest_campaign" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "description" VARCHAR(200) NULL,
    "start_time" BIGINT NOT NULL,
    "end_time" BIGINT NOT NULL,
    "favorite" INT DEFAULT 0,
    "status" VARCHAR(20) NOT NULL,
    "created_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "quest_campaign"."status" IS 'un_start,ongoing,ended';


CREATE TABLE "quest_campaign_info" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "total_reward" INT DEFAULT 0,
    "total_users" INT DEFAULT 0,
    "total_quest_execution" INT DEFAULT 0,
    "created_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE "quest_category" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL,
    "created_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "quest_category"."name" IS 'onboarding,social,engage';


CREATE TABLE "quest" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "quest_campaign_id" INT NOT NULL,
    "quest_category_id" INT NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "logo" VARCHAR(100) NULL,
    "description" VARCHAR(200) NULL,
    "is_period" boolean DEFAULT TRUE,
    "start_time" BIGINT NOT NULL,
    "end_time" BIGINT NOT NULL,
    "difficulty" INT NOT NULL,
    "gas_required" VARCHAR(20) NULL,
    "time_required" VARCHAR(20) NULL,
    "total_action" INT NOT NULL DEFAULT 0,
    "reward" INT NOT NULL DEFAULT 0,
    "priority" INT DEFAULT 0,
    "favorite" INT DEFAULT 0,
    "status" VARCHAR(20) NOT NULL,
    "tag" VARCHAR(200) NULL,
    "created_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "quest"."status" IS 'un_start,ongoing,ended';
CREATE INDEX "idx_quest_campaign_id_create" ON "quest" ("quest_campaign_id","created_at");
CREATE INDEX "idx_quest_campaign_id_priority_create" ON "quest" ("quest_campaign_id", "priority", "created_at");
CREATE INDEX "idx_quest_category_create" ON "quest" ("quest_category_id","created_at");
CREATE INDEX "idx_quest_status_campaign_id" ON "quest" ("status","quest_campaign_id");


CREATE TABLE "quest_action" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "description" VARCHAR(200) NULL,
    "quest_campaign_id" INT NOT NULL,
    "category" VARCHAR(30) NULL,
    "quest_id" INT NOT NULL,
    "category_id" INT NOT NULL DEFAULT 0,
    "source" VARCHAR(50) NULL,
    "dapps" VARCHAR(200) NULL,
    "networks" VARCHAR(100) NULL,
    "to_networks" VARCHAR(200) NULL,
    "times" INT NOT NULL DEFAULT 1,
    "created_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "quest_action"."category" IS 'dapp,twitter_follow,twitter_like,twitter_retweet,twitter_quote,twitter_create,tg_join,tg_role';
COMMENT ON COLUMN "quest_action"."source" IS '从哪里进入';
COMMENT ON COLUMN "quest_action"."dapps" IS '指定dapp上操作';
COMMENT ON COLUMN "quest_action"."networks" IS '指定链上操作';
COMMENT ON COLUMN "quest_action"."to_networks" IS '如果是bridge,指定另外的链';
COMMENT ON COLUMN "quest_action"."times" IS '需要完成几次';
CREATE INDEX "idx_quest_action_quest_id" ON "quest_action" ("quest_id");
CREATE INDEX "idx_quest_action_quest_campaign_id" ON "quest_action" ("quest_campaign_id");
CREATE INDEX "idx_quest_action_name_create" ON "quest_action" ("name","created_at");
CREATE INDEX "idx_quest_action_category_quest_campaign_id" ON "quest_action" ("category","quest_campaign_id");


CREATE TABLE "user_quest" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "account_id" INT NOT NULL DEFAULT 0,
    "quest_id" INT NOT NULL DEFAULT 0,
    "quest_campaign_id" INT NOT NULL DEFAULT 0,
    "action_completed" INT NOT NULL DEFAULT 0,
    "status" VARCHAR(20) NOT NULL,
    "is_claimed" boolean NULL DEFAULT false,
    "claimed_at" TIMESTAMP with time zone NULL,
    "created_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "user_quest"."status" IS 'in_process,expired,completed';
CREATE unique index "idx_user_request_account_quest" ON "user_quest" ("account_id","quest_id");
CREATE INDEX "idx_user_request_account_campaign_creat" ON "user_quest" ("account_id","quest_campaign_id","created_at");
CREATE INDEX "idx_user_request_quest_id" ON "user_quest" ("quest_id");
CREATE INDEX "idx_user_request_quest_campaign_id" ON "user_quest" ("quest_campaign_id");
CREATE INDEX "idx_user_request_account_claimed_create" ON "user_quest" ("account_id","is_claimed","claimed_at");


CREATE TABLE "user_quest_action" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "account_id" INT NOT NULL,
    "quest_action_id" INT NOT NULL,
    "quest_id" INT NOT NULL,
    "quest_campaign_id" INT NOT NULL,
    "times" INT NOT NULL,
    "status" VARCHAR(20) NOT NULL,
    "created_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "user_quest_action"."status" IS 'in_process,expired,completed';
CREATE unique index "idx_user_quest_action_account_action" ON "user_quest_action" ("account_id","quest_action_id");
CREATE INDEX "idx_user_quest_action_account_quest" ON "user_quest_action" ("account_id","quest_id");
CREATE INDEX "idx_user_quest_action_campaign_status" ON "user_quest_action" ("quest_campaign_id","status");


CREATE TABLE "user_reward" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "account_id" INT NOT NULL,
    "reward" INT NOT NULL DEFAULT 0,
    "invite_reward" INT NULL DEFAULT 0,
    "claimed_reward" INT NULL DEFAULT 0,
    "created_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE unique INDEX "idx_user_reward_account" ON "user_reward" ("account_id");


CREATE TABLE "user_reward_rank" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "account_id" INT NOT NULL,
    "reward" INT NOT NULL DEFAULT 0,
    "rank" INT NOT NULL DEFAULT 0,
    "created_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE unique INDEX "idx_user_reward_rank_account" ON "user_reward_rank" ("account_id");
CREATE INDEX "idx_user_reward_rank_rank" ON "user_reward_rank" ("rank");


CREATE TABLE "user_favorite" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "account_id" INT NOT NULL,
    "relate_id" INT NOT NULL,
    "category" varchar(20) NOT NULL,
    "is_favorite" BOOL NOT NULL,
    "created_at" TIMESTAMP with time zone DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "user_favorite"."category" IS 'dapp,quest_campaign,quest';
CREATE INDEX "idx_user_favorite_category_relate_id" ON "user_favorite" ("category","relate_id");
CREATE INDEX "idx_user_favorite_account_category_favorite_create" ON "user_favorite" ("account_id", "category", "is_favorite", "created_at");
CREATE unique index "idx_user_favorite_account_category_relate" ON "user_favorite" ("account_id","relate_id","category");


CREATE TABLE "quest_long" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL,
    "description" VARCHAR(200) NULL,
    "rule" TEXT NULL,
    "category" VARCHAR(50) NOT NULL,
    "status" VARCHAR(20) NOT NULL,
    "created_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "quest_long"."category" IS 'daily_check_in,invite';
COMMENT ON COLUMN "quest_long"."status" IS 'ongoing,completed';
CREATE INDEX "idx_quest_long_category" ON "quest_long" ("category","status");


CREATE TABLE "user_daily_check_in" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "quest_long_id" INT NOT NULL,
    "account_id" INT NOT NULL,
    "reward" INT NOT NULL,
    "check_in_time" bigint NOT NULL,
    "created_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "user_daily_check_in"."check_in_time" IS 'check in time/utc 0点';
CREATE unique INDEX "idx_user_daily_check_in_account_check_in_time" ON "user_daily_check_in" ("account_id","check_in_time");


alter table user_info add column "avatar" varchar(200) NULL;
alter table user_info add column "username" varchar(50) NULL;
alter table t_action_record add column "source" varchar(50) NULL;
alter table t_action_record add column "network_id" INT NULL;
alter table t_action_record add column "dapp_id" INT NULL;
alter table t_action_record add column "to_network_id" INT NULL;
alter table t_action_record add column "category_id" INT NULL;
alter table invite_code_pool add column "is_claimed" BOOL DEFAULT false;
alter table invite_code_pool add column "status" VARCHAR(20) NULL DEFAULT '';
CREATE INDEX "idx_invite_code_pool_used_id_used_status" ON "invite_code_pool" ("used_user_id", "is_used", "status");
CREATE INDEX "idx_invite_code_pool_creator_id_used_updated" ON "invite_code_pool" ("creator_user_id", "is_used", "updated_at");
CREATE INDEX "idx_t_action_record_dapp_id" ON "t_action_record" ("dapp_id", "id");