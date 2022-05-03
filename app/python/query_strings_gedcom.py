# query_strings_gedcom.py

insert_person = '''
    INSERT INTO person (person_id)
    VALUES (?)
'''

insert_name = '''
    INSERT INTO name (person_id, names, name_type_id, sort_order)
    VALUES (?, ?, 1, ?)
'''

update_name = '''
    UPDATE name 
    SET (names, sort_order) = (?, ?)
    WHERE person_id = 1
'''