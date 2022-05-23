# query_strings_gedcom.py



delete_finding_all = '''
    DELETE FROM finding
'''

delete_name_all = '''
    DELETE FROM name
'''

delete_person_all = '''
    DELETE FROM person
    WHERE person_id != 1
'''

delete_place_all = '''
    DELETE FROM place
    WHERE place_id != 1
'''

delete_places_places_all = '''
    DELETE FROM places_places
    WHERE places_places_id != 1
'''

delete_source_all = '''
    DELETE FROM source
'''

insert_citation = '''
    INSERT INTO citation
    VALUES (null, ?, ?)
'''

insert_claims_person = '''
    INSERT INTO claim (person_id, source_id)
    VALUES (?, ?)
'''

insert_finding_birth = '''
    INSERT INTO finding (event_type_id, person_id)
    VALUES (1, ?)    
'''

insert_finding_burial = '''
    INSERT INTO finding (event_type_id, person_id)
    VALUES (5, ?)
'''

insert_finding_couple_new = '''
    INSERT INTO finding (event_type_id, person_id1, person_id2, kin_type_id1, kin_type_id2) 
    VALUES (2, ?, ?, 128, 129)
'''

insert_finding_death = '''
    INSERT INTO finding (event_type_id, person_id)
    VALUES (4, ?)
'''
insert_finding_job = '''
    INSERT INTO finding (event_type_id, person_id, particulars)
    VALUES (6, ?, ?)
'''

insert_finding_default_person = '''
    INSERT INTO finding (finding_id, event_type_id, person_id)
    VALUES (1, 1, 1)    
'''

insert_finding_religion = '''
    INSERT INTO finding (person_id, event_type_id, particulars)
    VALUES (?, 30, ?)
'''

insert_finding_residence = '''
    INSERT INTO finding (person_id, event_type_id)
    VALUES (?, 13)
'''

insert_links_citations_names = '''
    INSERT INTO links_links (citation_id, name_id)
    VALUES (?, ?)
'''

insert_name = '''
    INSERT INTO name (person_id, names, name_type_id, sort_order)
    VALUES (?, ?, 1, ?)
'''

insert_name_default_person = '''
    INSERT INTO name (name_id, person_id, names, name_type_id, sort_order) 
    VALUES (1, 1, 'person #1', 24, 'person #1')
'''

insert_person = '''
    INSERT INTO person (person_id)
    VALUES (?)
'''

insert_source = '''
    INSERT INTO source 
    VALUES (?, '')
'''
select_citation_newest = '''
    SELECT seq FROM SQLITE_SEQUENCE WHERE name = 'citation'
'''

select_finding_all_children = '''
    SELECT person_id 
    FROM finding 
    WHERE person_id1 IS NOT null OR person_id2 IS NOT null
'''

select_finding_birth = '''
    SELECT finding_id 
    FROM finding
    WHERE person_id = ?
'''

select_finding_couples = '''
    SELECT person_id1, person_id2
    FROM finding 
    WHERE person_id1 IS NOT null OR person_id2 IS NOT null
'''

select_name_newest = '''
    SELECT seq FROM SQLITE_SEQUENCE WHERE name = 'name'
'''

select_person_max = '''
    SELECT MAX(person_id)
    FROM person
'''

update_finding_parents = '''
    UPDATE finding 
    SET (person_id1, person_id2, kin_type_id1, kin_type_id2) = (?, ?, 1, 2)
    WHERE finding_id = ?
'''

update_gender = '''
    UPDATE person
    SET gender = ?
    WHERE person_id = ?
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

update_source_title = '''
    UPDATE source
    SET sources = ?
    WHERE source_id = ?
'''


