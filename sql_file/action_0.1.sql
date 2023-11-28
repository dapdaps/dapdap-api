CREATE TABLE "t_action_dapp" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "record_id" int NOT NULL,
    "count" INT NOT NULL  DEFAULT 0,
    "participants" INT NOT NULL DEFAULT 0,
    "template" varchar(255) NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX "idx_action_dapp_record_id" ON "t_action_dapp" ("record_id");

CREATE TABLE "t_action_chain" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "record_id" int NOT NULL,
    "count" INT NOT NULL  DEFAULT 0,
    "action_title" varchar(512) NOT NULL,
    "template" varchar(255) NOT NULL,
    "action_network_id" varchar(128) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX "idx_action_chain_record_id" ON "t_action_chain" ("record_id");
CREATE INDEX "idx_action_chain_network_count" ON "t_action_chain" ("action_network_id","count");
CREATE UNIQUE INDEX "idx_action_chain_title_template_network" ON "t_action_chain" ("action_title","template","action_network_id");