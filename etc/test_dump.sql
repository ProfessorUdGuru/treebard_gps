PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE test_table (test_table_id INTEGER PRIMARY KEY AUTOINCREMENT, test_values TEXT);
INSERT INTO test_table VALUES(1,'red');
INSERT INTO test_table VALUES(2,'green');
INSERT INTO test_table VALUES(3,'yellow');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('test_table',3);
COMMIT;
