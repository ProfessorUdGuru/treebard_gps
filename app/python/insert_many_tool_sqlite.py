# insert_many_tool_sqlite

import sqlite3
import files



# EXAMPLE ONE--start with a list of single items, change it to a list of one-tuples
# list_o_tups = []
# for item in new_list:
    # item = (item,)
    # list_o_tups.append(item)

# EXAMPLE TWO--hard-coded tuple
# list_o_tups = [
	# (1,3,3,5),
	# (2,3,1,0),
	# (3,11,4,2),
	# (5,4,5,0),
	# (6,3,2,2),
	# (7,5,6,0),
	# (8,26,7,1),
	# (9,16,8,2),
	# (10,26,9,0),
	# (11,27,10,0),
	# (12,15,11,0),
	# (50,3,67,1),
	# (120,3,145,3),
	# (162,2,187,0)]

# current_file = files.get_current_file()[0] # commented out for safety
# DON'T RUN THIS CODE EXPERIMENTALLY, MAKE SURE IT'S RIGHT AND WHAT YOU REALLY WANT TO DO
# E.G. "EXAMPLE 2" WAS USED TO REPLACE A WHOLE TABLE OF VALUES WIPED OUT BY A CARELESS DELETE QUERY WITHOUT A WHERE STATEMENT TO FILTER IT DOWN.........................GOOD THING I'D JUST DONE A SELECT * SO i COULD JUST PUT STUFF BACK IN INSTEAD OF HAVING TO FIND AN OLD COPY OF DB
conn = sqlite3.connect(current_file)
conn.execute('PRAGMA foreign_keys = 1')
cur = conn.cursor()

cur.executemany(
    '''
        INSERT INTO findings_notes
        VALUES (?, ?, ?, ?)
    ''', 
    list_o_tups)
conn.commit()

cur.close()
conn.close()

