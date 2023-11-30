CREATE TABLE "quest_campaign" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL,
    "description" VARCHAR(200) NULL,
    "start_time" BIGINT NOT NULL,
    "end_time" BIGINT NOT NULL,
    "favorite" INT DEFAULT 0,
    "status" VARCHAR(20) NOT NULL,
    "total_reward" INT DEFAULT 0,
    "total_users" INT DEFAULT 0,
    "total_quest_execution" INT DEFAULT 0,
    "created_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "quest_campaign"."status" IS 'un_start,ongoing,finished';


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
    "name" VARCHAR(50) NOT NULL,
    "logo" VARCHAR(100) NULL,
    "description" VARCHAR(200) NULL,
    "is_period" boolean DEFAULT TRUE,
    "start_time" BIGINT NOT NULL,
    "end_time" BIGINT NOT NULL,
    "difficulty" INT NOT NULL,
    "gas_required" VARCHAR(20) NULL,
    "time_required" VARCHAR(20) NULL,
    "reward" INT NOT NULL,
    "priority" INT DEFAULT 0,
    "status" VARCHAR(20) NOT NULL,
    "created_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "quest"."status" IS 'un_start,ongoing,finished';
CREATE INDEX "idx_quest_campaign_id_create" ON "quest" ("quest_campaign_id","created_at");
CREATE INDEX "idx_quest_priority_create" ON "quest" ("priority","created_at");
CREATE INDEX "idx_quest_category_create" ON "quest" ("quest_category_id","created_at");
CREATE INDEX "idx_quest_name_create" ON "quest" ("name","created_at");


CREATE TABLE "quest_action" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL,
    "description" VARCHAR(200) NULL,
    "quest_campaign_id" INT NOT NULL,
    "quest_id" INT NOT NULL,
    "category_id" INT NOT NULL DEFAULT 0,
    "source" VARCHAR(50) NULL,
    "dapps" VARCHAR(200) NULL,
    "networks" VARCHAR(100) NULL,
    "to_networks" VARCHAR(200) NULL,
    "difficulty" INT NOT NULL,
    "times" INT NOT NULL DEFAULT 1,
    "created_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "quest_action"."source" IS '从哪里进入';
COMMENT ON COLUMN "quest_action"."dapps" IS '指定dapp上操作';
COMMENT ON COLUMN "quest_action"."networks" IS '指定链上操作';
COMMENT ON COLUMN "quest_action"."to_networks" IS '如果是bridge,指定另外的链';
COMMENT ON COLUMN "quest_action"."times" IS '需要完成几次';
CREATE INDEX "idx_quest_action_quest_id" ON "quest_action" ("quest_id");
CREATE INDEX "idx_quest_action_quest_campaign_id" ON "quest_action" ("quest_campaign_id");
CREATE INDEX "idx_quest_action_name_create" ON "quest_action" ("name","created_at");


CREATE TABLE "user_quest" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "user_id" INT NOT NULL,
    "quest_id" INT NOT NULL,
    "quest_campaign_id" INT NOT NULL,
    "status" VARCHAR(20) NOT NULL,
    "is_claimed" boolean NULL,
    "claimed_at" TIMESTAMP with time zone NULL,
    "created_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "user_quest"."status" IS 'in_process,expired,completed,un_claimed';
CREATE unique index "idx_user_request_user_quest" ON "user_quest" ("user_id","quest_id");
CREATE INDEX "idx_user_request_user_creat" ON "user_quest" ("user_id","created_at");
CREATE INDEX "idx_user_request_quest_id" ON "user_quest" ("quest_id");
CREATE INDEX "idx_user_request_quest_campaign_id" ON "user_quest" ("quest_campaign_id");


CREATE TABLE "user_quest_action" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "user_id" INT NOT NULL,
    "quest_action_id" INT NOT NULL,
    "quest_id" INT NOT NULL,
    "quest_campaign_id" INT NOT NULL,
    "times" INT NOT NULL,
    "status" VARCHAR(20) NOT NULL,
    "created_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "user_quest_action"."status" IS 'in_process,expired,completed';
CREATE unique index "idx_user_quest_action_user_action" ON "user_quest_action" ("user_id","quest_action_id");
CREATE INDEX "idx_user_quest_action_user_quest" ON "user_quest_action" ("user_id","quest_id");


CREATE TABLE "user_reward" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "user_id" INT NOT NULL,
    "total_reward" INT NOT NULL,
    "claimed_reward" INT NOT NULL,
    "created_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX "idx_user_reward" ON "user_reward" ("user_id");


CREATE TABLE "user_reward_quest_campaign" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "user_id" INT NOT NULL,
    "quest_campaign_id" INT NOT NULL,
    "reward" INT NOT NULL,
    "rank" INT NOT NULL,
    "created_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX "idx_user_reward_quest_campaign" ON "user_reward_quest_campaign" ("quest_campaign_id","rank");
CREATE INDEX "idx_user_reward_quest_campaign_user_campaign" ON "user_reward_quest_campaign" ("user_id","quest_campaign_id");


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
CREATE INDEX "idx_user_favorite_user_category_create" ON "user_favorite" ("account_id","category","created_at");
CREATE unique index "idx_user_favorite_user_category_relate" ON "user_favorite" ("account_id","category","relate_id");

alter table user_info add column "avatar" varchar(200) NULL;
alter table user_info add column "username" varchar(50) NULL;


alter table t_action_record add column "network_id" INT NULL;
alter table t_action_record add column "dapp_id" INT NULL;
alter table t_action_record add column "to_network_id" INT NULL;
alter table t_action_record add column "category_id" INT NULL;
