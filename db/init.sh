#!/usr/bin/env bash
set -euo pipefail

psql \
  -v ON_ERROR_STOP=1 \
  --username "$POSTGRES_USER" \
  --dbname "$POSTGRES_DB" <<'EOSQL'
BEGIN;

CREATE SEQUENCE IF NOT EXISTS public.data_item_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 2147483647
  CACHE 1;

CREATE TABLE IF NOT EXISTS public.data (
  item_id integer DEFAULT nextval('public.data_item_id_seq') NOT NULL,
  item_first_name text,
  item_last_name text,
  item_number text NOT NULL,
  CONSTRAINT data_pkey PRIMARY KEY (item_id)
);

ALTER SEQUENCE public.data_item_id_seq
  OWNED BY public.data.item_id;

CREATE INDEX IF NOT EXISTS index_first_name
  ON public.data (item_first_name);

CREATE INDEX IF NOT EXISTS index_last_name
  ON public.data (item_last_name);

CREATE INDEX IF NOT EXISTS index_number
  ON public.data (item_number);

COMMIT;
EOSQL
