CREATE TABLE "route_pair" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "token0" VARCHAR(66) NOT NULL,
    "token0_decimals" INT NOT NULL,
    "token1" VARCHAR(66) NOT NULL,
    "token1_decimals" INT NOT NULL,
    "chain_id" INT NOT NULL DEFAULT 0,
    "status" INT NOT NULL DEFAULT 0,
    "created_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE unique INDEX "route_pair_chain_token0_token1" ON "route_pair" ("chain_id","token0","token1");
CREATE unique INDEX "route_pair_chain_token1_token0" ON "route_pair" ("chain_id","token1","token0");
CREATE INDEX "route_pair_status_chain" ON "route_pair" ("status","chain_id");
