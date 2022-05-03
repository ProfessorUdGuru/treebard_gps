# parse_lines_and_use_directly_re_gedcom
from re import sub
import sqlite3
# from mockup import records_dict
import dev_tools as dt
from dev_tools import looky, seeline



create_table_person = '''
    CREATE TABLE IF NOT EXISTS person (person_id INTEGER PRIMARY KEY AUTOINCREMENT, names TEXT, gender TEXT NOT NULL DEFAULT 'unknown')
'''

insert_person = '''
    INSERT INTO person (person_id, names)
    VALUES (?, ?)
'''


conn = sqlite3.connect("d:/test/gedcom_001.db")
cur = conn.cursor()


def parse_line(person_id, line):
    n = line[0]
    tag = line[1]
    if len(line) == 3:
        data = line[2]
    if n == 1:
        if tag == 'NAME':
            insert_name(person_id, data)

def make_name_table():
    cur.execute(create_table_person)
    conn.commit()

def insert_name(person_id, data):
    person_id = int(sub("\D", "", person_id))
    make_name_table()
    cur.execute(insert_person, (person_id, data))
    conn.commit()

    print("line", looky(seeline()).lineno, "data:", data)


for k,v in records_dict.items():
    print("line", looky(seeline()).lineno, "k:", k)
    if k == "INDI":
        record = v
        for kk, vv in record.items():
            person_id = kk
            person_data = vv


            for line in person_data:
                print("line", looky(seeline()).lineno, "line:", line)
                parse_line(person_id, line)





cur.close()
conn.close()