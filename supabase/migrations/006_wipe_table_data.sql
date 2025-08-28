BEGIN;
TRUNCATE TABLE flags, stages, orders, customers;
TRUNCATE TABLE sync_state;
COMMIT;
