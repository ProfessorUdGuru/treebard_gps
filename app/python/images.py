# images.py

import sqlite3
from query_strings import select_all_images
from files import current_file

def get_all_pics():

	conn = sqlite3.connect(current_file)
	cur = conn.cursor()
	cur.execute(select_all_images)
	picvals = cur.fetchall()
	cur.close()
	conn.close()
	return picvals