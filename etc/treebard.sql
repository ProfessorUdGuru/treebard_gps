PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE closing_state (closing_state_id INTEGER PRIMARY KEY AUTOINCREMENT, prior_tree TEXT DEFAULT null, openpic TEXT NOT NULL DEFAULT 'tree_of_life_lib_o_congress.jpg', tree_is_open BOOLEAN NOT NULL DEFAULT 0, recent_files TEXT DEFAULT "");
INSERT INTO closing_state VALUES(1,'sample_tree.tbd','tree_live_oak_virginia_pixabay.jpg',1,'Sample Tree');
CREATE TABLE app_setting (app_setting_id INTEGER PRIMARY KEY AUTOINCREMENT, openpic_dir TEXT, default_openpic_dir TEXT NOT NULL DEFAULT 'images/openpic');
INSERT INTO app_setting VALUES(1,NULL,'images/openpic');
CREATE TABLE default_format (default_format_id INTEGER PRIMARY KEY AUTOINCREMENT, default_bg TEXT, default_highlight_bg TEXT, default_head_bg TEXT, default_fg TEXT, default_output_font TEXT, default_input_font TEXT, default_font_size INTEGER);
INSERT INTO default_format VALUES(1,'#061d2f','#284b80','#267d82','#71cfd5','courier','dejavu sans mono',12);
CREATE TABLE default_date_format (default_date_format_id INTEGER PRIMARY KEY AUTOINCREMENT, default_date_formats TEXT, default_abt TEXT, default_est TEXT, default_cal TEXT, default_bef_aft TEXT, default_bc_ad TEXT, default_os_ns TEXT, default_span TEXT, default_range TEXT);
INSERT INTO default_date_format VALUES(1,'dmy','abt','est','calc','bef/aft','BCE/CE','OS/NS','from_to','btwn_&');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('closing_state',1);
INSERT INTO sqlite_sequence VALUES('app_setting',1);
INSERT INTO sqlite_sequence VALUES('default_format',1);
INSERT INTO sqlite_sequence VALUES('default_date_format',1);
COMMIT;
