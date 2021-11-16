# images.py

import sqlite3
from query_strings import select_all_images
from files import get_current_file

def get_all_pics():
    current_file = get_current_file()[0]
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_all_images)
    picvals = cur.fetchall()
    cur.close()
    conn.close()
    return picvals