# query_strings_gedcom.py

delete_person_all = '''
    DELETE FROM person
    WHERE person_id != 1
'''

delete_name_all = '''
    DELETE FROM name
    WHERE person_id != 1
'''

delete_finding_all = '''
    DELETE FROM finding
'''

delete_source_all = '''
    DELETE FROM source
'''

insert_claims_person = '''
    INSERT INTO claim (person_id, source_id)
    VALUES (?, ?)
'''

insert_finding_birth = '''
    INSERT INTO finding (date, date_sorter, nest0, event_type_id, person_id)
    VALUES ('-0000-00-00-------', '0, 0, 0', 1, 1, ?)    
'''

insert_finding_default_person = '''
    INSERT INTO finding (finding_id, date, date_sorter, nest0, event_type_id, person_id)
    VALUES (1, '-0000-00-00-------', '0, 0, 0', 1, 1, 1)    
'''

insert_name = '''
    INSERT INTO name (person_id, names, name_type_id, sort_order)
    VALUES (?, ?, 1, ?)
'''

insert_person = '''
    INSERT INTO person (person_id)
    VALUES (?)
'''

insert_source = '''
    INSERT INTO source 
    VALUES (?, ?)
'''

select_finding_birth = '''
    SELECT finding_id 
    FROM finding
    WHERE person_id = ?
'''

update_finding_parents = '''
    UPDATE finding 
    SET (person_id1, person_id2) = (?, ?)
    WHERE finding_id = ?
'''

update_gender_default_person = '''
    UPDATE person
    SET gender = 'unknown'
    WHERE person_id = 1
'''

update_name = '''
    UPDATE name 
    SET (names, sort_order) = (?, ?)
    WHERE person_id = 1
'''

update_name_default_person = '''
    UPDATE name
    SET (names, name_type_id, sort_order) = 
        ('person #1', 24, 'person #1')
    WHERE person_id = 1
'''