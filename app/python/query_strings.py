# query_strings.py

import dev_tools as dt





'''
	Since Sqlite queries are inserted as string in Python code,
	the queries can be stored here to save space in the modules
	where they are used.
'''

delete_claims_findings = '''
    DELETE FROM claims_findings
    WHERE finding_id = ?
'''

delete_color_scheme = '''
    DELETE FROM color_scheme 
    WHERE color_scheme_id = ?
'''
   
delete_finding = '''
    DELETE FROM finding
    WHERE finding_id = ?    
'''

delete_finding_places = '''
    DELETE FROM finding_places
    WHERE finding_id = ?
'''

delete_findings_notes_finding = '''
    DELETE FROM findings_notes
    WHERE finding_id = ?
'''

delete_findings_persons = '''
    DELETE FROM findings_persons
    WHERE finding_id = ?
'''

delete_findings_persons_offspring = '''
    DELETE FROM findings_persons
    WHERE finding_id = ?
'''

delete_findings_roles_finding = '''
    DELETE FROM findings_roles
    WHERE finding_id = ?
''' 

delete_findings_notes = '''
    DELETE FROM findings_notes
    WHERE note_id = ? 
    AND finding_id = ?
'''

delete_findings_role = '''
    DELETE FROM findings_roles 
    WHERE findings_roles_id = ?
'''

delete_note = '''
    DELETE FROM note
    WHERE note_id = ? 
'''

insert_color_scheme = '''
    INSERT INTO color_scheme 
    VALUES (null, ?, ?, ?, ?, 0, 0)
'''

insert_event_type_new = '''
    INSERT INTO event_type (event_type_id, event_types, couple, after_death)
    VALUES (?, ?, ?, ?)
'''

insert_finding_birth = '''
    INSERT INTO finding (finding_id, age, event_type_id, person_id)
    VALUES (?, 0, 1, ?)
'''

insert_finding_new = '''
    INSERT INTO finding (finding_id, age, event_type_id, person_id)
    VALUES (?, ?, ?, ?)
'''

insert_finding_new_couple = '''
    INSERT INTO finding (finding_id, event_type_id)
    VALUES (?, ?)
'''

insert_finding_places_new = '''
    INSERT INTO finding_places (
        finding_id, nest0, nest1, nest2, nest3, nest4, nest5, nest6, nest7, nest8)
    VALUES (?, 1, null, null, null, null, null, null, null, null)
'''

insert_finding_places_new_event = '''
    INSERT INTO finding_places
       (nest0, nest1, nest2, nest3, nest4, nest5, nest6, nest7, nest8, finding_id)
    VALUES ({})
'''.format(','.join(['?'] * 10))

insert_findings_notes = '''
    INSERT INTO findings_notes 
    VALUES (null, ?, ?, ?)
'''

insert_findings_persons_new_couple = '''
    INSERT INTO findings_persons (
        finding_id, person_id1, age1, kin_type_id1, 
        person_id2, age2, kin_type_id2)
    VALUES (?, ?, ?, ?, ?, ?, ?)
'''

insert_findings_roles = '''
    INSERT INTO findings_roles 
    VALUES (null, ?, ?, ?)
'''

insert_image_new = '''
    INSERT INTO image
    VALUES (null, ?, '')
'''

insert_images_entities = '''
    INSERT INTO images_entities (image_id, main_image, person_id) 
    VALUES (?, 0, ?) 
'''

insert_kin_type_new = '''
    INSERT INTO kin_type (kin_types, kin_code)
    VALUES (?, ?)
'''

insert_name = '''
    INSERT INTO name 
    VALUES (null, ?, ?, ?, ?, null)
'''

insert_name_type_new = '''
    INSERT INTO name_type
    VALUES (?, ?)
'''

insert_note = '''
    INSERT INTO note 
    VALUES (null, ?, 0, ?)
'''

insert_person_new = '''
    INSERT INTO person VALUES (?, ?)
'''

insert_place_new = '''
    INSERT INTO place (place_id, places)
    VALUES (?, ?)
'''

insert_places_places_new = '''
    INSERT INTO places_places (place_id1, place_id2)
    VALUES (?, ?)
'''

insert_role_type = '''
    INSERT INTO role_type VALUES (null, ?, 0, 0)
'''

select_all_color_schemes = '''
    SELECT bg, highlight_bg, head_bg, fg 
    FROM color_scheme
'''

select_all_color_schemes_plus = '''
    SELECT bg, highlight_bg, head_bg, fg, built_in, color_scheme_id 
    FROM color_scheme
'''

select_all_event_types = '''
    SELECT event_types
    FROM event_type
'''

select_all_event_types_couple = '''
    SELECT event_types
    FROM event_type
    WHERE hidden != 1
        AND couple == 1
'''

select_all_finding_places_findings = '''
    SELECT finding_id FROM finding_places
'''

select_all_findings_current_person = '''
    SELECT finding_id
    FROM finding
    WHERE person_id = ?
'''

select_all_findings_roles_ids = '''
    SELECT finding_id
    FROM findings_roles
'''

select_all_findings_roles_ids_distinct = '''
    SELECT DISTINCT finding_id
    FROM findings_roles
'''

select_all_findings_notes_ids = '''
    SELECT finding_id
    FROM findings_notes
'''

select_all_images = '''
    SELECT images FROM image
'''

select_all_kin_type_ids_couple = '''
    SELECT kin_type_id
    FROM kin_type
    WHERE kin_code = 'D'
        AND hidden = 0
'''

select_all_kin_ids_types_couple = '''
    SELECT kin_type_id, kin_types
    FROM kin_type
    WHERE kin_code = 'D'
        AND hidden = 0
'''

select_all_name_types = '''
    SELECT name_types FROM name_type ORDER BY name_types
'''

select_all_names_ids = '''
    SELECT names, name.person_id, sort_order 
    FROM name JOIN person 
        ON person.person_id = name.person_id 
'''

select_birth_names_ids = '''
    SELECT names, name.person_id, sort_order 
    FROM name JOIN person 
        ON person.person_id = name.person_id 
    WHERE name_type_id = 1 
'''

select_all_nested_pairs = '''
    SELECT place_id1, place_id2   
    FROM places_places
'''

select_all_nested_places = '''
    SELECT nest0, nest1, nest2, nest3, nest4, nest5, nest6, nest7, nest8
    FROM nested_places
'''

select_all_person_ids = '''
    SELECT person_id FROM person
'''

# select_all_person_images = '''
    # SELECT names, images, caption, main_image
    # FROM images_entities
        # JOIN person
            # ON images_entities.person_id = person.person_id
        # JOIN image
            # ON image.image_id = images_entities.image_id 
        # JOIN name
            # ON person.person_id = name.person_id
    # WHERE images_entities.person_id = ?
        # AND name_type_id = 1
# '''


select_all_person_images = '''
    SELECT names, images, caption, main_image
    FROM images_entities
        JOIN person
            ON images_entities.person_id = person.person_id
        JOIN image
            ON image.image_id = images_entities.image_id 
        JOIN name
            ON person.person_id = name.person_id
    WHERE images_entities.person_id = ?
        AND name_type_id = 1
'''

select_all_place_ids = '''
    SELECT place_id
    FROM place
'''

select_all_place_images = '''
    SELECT places, images, caption, main_image
    FROM images_entities
        JOIN place
            ON images_entities.place_id = place.place_id 
        JOIN current
            ON current.place_id = place.place_id
        JOIN image
            ON image.image_id = images_entities.image_id 
'''

select_all_places = '''
    SELECT places
    FROM place
'''

select_all_places_places = '''
    SELECT place_id1, place_id2
    FROM places_places
'''

select_all_source_images = '''
    SELECT citations, images, caption, main_image, sources
    FROM images_entities
        JOIN source
            ON citation.source_id = source.source_id
        JOIN citation
            ON images_entities.citation_id = citation.citation_id
        JOIN current
            ON current.citation_id = citation.citation_id
        JOIN image
            ON image.image_id = images_entities.image_id 
'''

select_color_scheme_current = '''
    SELECT bg, highlight_bg, head_bg, fg 
    FROM format 
    WHERE format_id = 1
'''

select_count_finding_id_sources = '''
    SELECT COUNT(finding_id) 
        FROM claims_findings 
        WHERE finding_id = ?
'''

select_count_findings_notes_note_id = '''
    SELECT COUNT (findings_notes_id) 
    FROM findings_notes
    WHERE note_id = ?
'''

select_count_findings_notes_finding_id = '''
    SELECT COUNT (findings_notes_id)
    FROM findings_notes
    WHERE finding_id = ?
'''

select_count_findings_roles = '''
    SELECT COUNT (findings_roles_id)
    FROM findings_roles
    WHERE finding_id = ?
'''

select_count_places = '''
    SELECT COUNT (places)
    FROM place
    WHERE places = ?
'''

select_count_place_id = '''
    SELECT COUNT (place_id) 
    FROM place WHERE place_id = ?
'''

select_count_subtopic = '''
    SELECT COUNT (subtopic)
    FROM note
    WHERE subtopic = ?
'''

select_couple_event_ids = '''
    SELECT finding_id
    FROM findings_persons
    WHERE person_id = ?
'''

select_couple_event_roles = '''    
        SELECT 
            findings_roles.finding_id,
            findings_roles.role_type_id,
            findings_roles.person_id
        FROM
            finding
            JOIN findings_roles
                ON findings_roles.finding_id = finding.finding_id 
            JOIN person
                ON person.person_id = findings_roles.person_id
            JOIN role_type
                ON role_type.role_type_id = 
                    findings_roles.role_type_id                      
        WHERE findings_roles.finding_id IN ({})       
    '''

select_current_person = '''
    SELECT name.person_id, names 
    FROM name 
    JOIN person 
        ON person.person_id = name.person_id 
    JOIN current 
        ON name.person_id = current.person_id
'''

select_current_person_id = '''
    SELECT person_id 
    FROM current WHERE current_id = 1'''

select_current_person_image = '''
    SELECT images 
    FROM image 
        JOIN images_entities 
            ON image.image_id = images_entities.image_id 
    WHERE main_image = 1 
        AND images_entities.person_id = ?
'''

select_current_tree = '''
    SELECT current_tree 
    FROM closing_state 
    WHERE closing_state_id = 1
'''

select_date_format = '''
    SELECT date_formats, abt, est, cal, bef_aft, bc_ad, os_ns, span, range
    FROM date_format
    WHERE date_format_id = 1
'''

select_event_type_id = '''
    SELECT event_type_id, couple
    FROM event_type
    WHERE event_types = ?
'''

select_event_type_after_death = '''
    SELECT event_types
    FROM event_type
    WHERE after_death = 1
'''

select_event_type_after_death_bool = '''
    SELECT after_death
    FROM event_type
    WHERE event_types = ?
'''

select_event_type_couple_bool = '''
    SELECT couple
    FROM event_type
    WHERE event_types = ?
'''

select_finding_event_type = '''
    SELECT event_type_id
    FROM finding
    WHERE finding_id = ?
'''

select_finding_id_birth = '''
    SELECT finding_id 
    FROM finding
    WHERE event_type_id = 1
        AND person_id = ?
'''

select_finding_ids_age1_parents = '''
    SELECT finding_id, age1
    FROM findings_persons
    WHERE person_id1 = ?
        AND kin_type_id1 in (1, 2)
'''

select_finding_ids_age2_parents = '''
    SELECT finding_id, age2
    FROM findings_persons
    WHERE person_id2 = ?
        AND kin_type_id2 in (1, 2)
'''

select_finding_ids_offspring = '''
    SELECT finding_id
    FROM findings_persons
    WHERE person_id1 = ?
        AND kin_type_id1 in (1, 2)
'''

select_finding_places = '''
    SELECT finding_places_id
    FROM finding_places
    WHERE finding_id = ?
'''

select_finding_places_id = '''
    SELECT finding_places_id
    FROM finding_places
    WHERE nest0 = ? 
        AND (nest1 = ? OR nest1 is null) 
        AND (nest2 = ? OR nest2 is null) 
        AND (nest3 = ? OR nest3 is null) 
        AND (nest4 = ? OR nest4 is null) 
        AND (nest5 = ? OR nest5 is null) 
        AND (nest6 = ? OR nest6 is null) 
        AND (nest7 = ? OR nest7 is null) 
        AND (nest8 = ? OR nest8 is null)
'''

select_finding_places_nesting = '''
    SELECT a.places, b.places, c.places, d.places, 
        e.places, f.places, g.places, h.places, i.places
    FROM finding_places
    LEFT JOIN place a ON a.place_id = finding_places.nest0
    LEFT JOIN place b ON b.place_id = finding_places.nest1
    LEFT JOIN place c ON c.place_id = finding_places.nest2
    LEFT JOIN place d ON d.place_id = finding_places.nest3
    LEFT JOIN place e ON e.place_id = finding_places.nest4
    LEFT JOIN place f ON f.place_id = finding_places.nest5
    LEFT JOIN place g ON g.place_id = finding_places.nest6
    LEFT JOIN place h ON h.place_id = finding_places.nest7
    LEFT JOIN place i ON i.place_id = finding_places.nest8             
    WHERE finding_id = ? 
'''

select_finding_sorter = '''
    SELECT date_sorter
    FROM finding
    WHERE finding_id = ?
'''

select_findings_details_couple = '''
    SELECT findings_persons.person_id1, findings_persons.age1, a.kin_types,
        findings_persons.person_id2, findings_persons.age2, b.kin_types
    FROM findings_persons
    JOIN finding
        ON finding.finding_id = findings_persons.finding_id
    JOIN kin_type as a
        ON a.kin_type_id = findings_persons.kin_type_id1
    JOIN kin_type as b
        ON b.kin_type_id = findings_persons.kin_type_id2
    WHERE findings_persons.finding_id = ?
'''

select_findings_details_couple_generic = '''
    SELECT event_types, date, date_sorter, particulars, finding_places_id 
    FROM finding 
        JOIN finding_places 
            ON finding_places.finding_id = finding.finding_id 
        JOIN event_type 
            ON finding.event_type_id = event_type.event_type_id 
    WHERE finding_places.finding_id = ?
'''

select_findings_details_generic = '''
    SELECT event_types, particulars, age, date, date_sorter
    FROM finding
    JOIN event_type
        ON finding.event_type_id = event_type.event_type_id
    WHERE  finding_id = ?
'''

select_findings_details_offspring = '''
    SELECT date, date_sorter, particulars, finding_places_id
    FROM finding
    JOIN finding_places
        ON finding_places.finding_id = finding.finding_id
    WHERE person_id = ?
        AND event_type_id = 1
'''

select_findings_for_person = '''
    SELECT event_types
    FROM finding
    JOIN event_type
        ON finding.event_type_id = event_type.event_type_id
    WHERE person_id = ?
'''

select_findings_persons_age = '''
    SELECT age
    FROM findings_persons
    WHERE person_id = ?
        AND finding_id = ?
'''

select_findings_persons_ma_id1 = '''
    SELECT person_id1
    FROM findings_persons
    WHERE kin_type_id1 = 1
        AND finding_id = ?
'''

select_findings_persons_ma_id2 = '''
    SELECT person_id2
    FROM findings_persons
    WHERE kin_type_id2 = 1
        AND finding_id = ?
'''

select_findings_persons_pa_id1 = '''
    SELECT person_id1
    FROM findings_persons
    WHERE kin_type_id1 = 2
        AND finding_id = ?
'''

select_findings_persons_pa_id2 = '''
    SELECT person_id2
    FROM findings_persons
    WHERE kin_type_id2 = 2
        AND finding_id = ?
'''

select_findings_persons_person_id = '''
    SELECT person_id1, person_id2
    FROM findings_persons
    WHERE finding_id = ?
'''

select_findings_persons_parents = '''
    SELECT person_id1, person_id2
    FROM findings_persons
    WHERE finding_id = ?
'''

select_findings_roles_generic = '''
    SELECT 
        finding.finding_id,
        findings_roles.role_type_id,
        findings_roles.person_id
    FROM
        finding
        JOIN findings_roles
            ON findings_roles.finding_id = finding.finding_id 
        JOIN person
            ON person.person_id = findings_roles.person_id
        JOIN role_type
            ON role_type.role_type_id = findings_roles.role_type_id 
    WHERE finding.person_id = ?
'''

select_findings_roles_generic_finding = '''
    SELECT 
        findings_roles.role_type_id,
        findings_roles.person_id        
    FROM
        finding
        JOIN findings_roles
            ON findings_roles.finding_id = finding.finding_id 
        JOIN person
            ON person.person_id = findings_roles.person_id
        JOIN role_type
            ON role_type.role_type_id = findings_roles.role_type_id 
    WHERE findings_roles.finding_id = ?
'''

select_format_font_size = '''
    SELECT font_size, default_font_size
    FROM format
    WHERE format_id = 1
'''

select_format_font_scheme = '''
    SELECT output_font, font_size
    FROM format
    WHERE format_id = 1
'''

select_image_id = '''
    SELECT image_id FROM image WHERE images = ?
'''

select_images_entities_main_image = '''
    SELECT images
    FROM images_entities
        JOIN person
            ON images_entities.person_id = person.person_id 
        JOIN current
            ON current.person_id = person.person_id
        JOIN image
            ON image.image_id = images_entities.image_id 
    WHERE images_entities.main_image = 1
'''

select_kin_type_string = '''
    SELECT kin_types FROM kin_type WHERE kin_type_id = ?
'''

select_kin_types_finding = '''
    SELECT kin_types
    FROM kin_type
    JOIN findings_persons
        ON kin_type.kin_type_id = findings_persons.kin_type_id
    WHERE finding_id = ?
'''

select_max_event_type_id = '''
    SELECT MAX(event_type_id) FROM event_type
'''

select_max_finding_id = '''
    SELECT MAX(finding_id) FROM finding
'''

select_max_finding_places_id = '''
    SELECT MAX(finding_places_id) FROM finding_places
'''

select_max_name_type_id = '''
    SELECT MAX(name_type_id) FROM name_type
'''

select_max_kin_type_id = '''
    SELECT MAX(kin_type_id) FROM kin_type
'''

select_max_person_id = '''
    SELECT MAX(person_id) FROM person
'''

select_max_place_id = ''' SELECT MAX(place_id) FROM place '''

select_name_details = '''
    SELECT names, name_types, used_by
    FROM name
    LEFT JOIN name_type
        ON name.name_type_id = name_type.name_type_id
    WHERE person_id = ?
'''

select_name_sort_order = '''
    SELECT
        sort_order
    FROM name
    JOIN person
        ON person.person_id = name.person_id
    WHERE name.person_id = ?
        AND name_type_id = 1 
'''

select_name_type_id = '''
    SELECT name_type_id 
    FROM name_type
    WHERE name_types = ?
'''

select_name_with_id = '''
    SELECT names 
    FROM name JOIN person 
        ON name.person_id = person.person_id 
    WHERE name_type_id = 1
        AND name.person_id = ?
'''

select_name_with_id_any = '''
    SELECT names, name_types 
    FROM name 
        JOIN person 
            ON name.person_id = person.person_id
        JOIN name_type 
            ON name_type.name_type_id = name.name_type_id
    WHERE name.person_id = ?
'''

select_nested_places_same = '''
    SELECT nest0, nest1, nest2, nest3, nest4, nest5, nest6, nest7, nest8
    FROM nested_places
    WHERE nest0 = ?
'''

select_nesting_fk_finding = '''
    SELECT finding_places_id 
    FROM finding_places
    WHERE finding_id = ?
'''

select_nestings_and_ids = '''
    SELECT nest0, nest1, nest2, nest3, nest4, nest5, nest6, 
        nest7, nest8, nested_places_id
    FROM nested_places
    JOIN place
        ON nested_places.nest0 = place.place_id
    WHERE nest0 = (SELECT place_id FROM place WHERE places = ?)
'''

select_note_id = '''
    SELECT note_id
    FROM note
    WHERE subtopic = ?
'''

select_notes_refresh = '''
    SELECT 
        findings_notes.note_id, 
        subtopic, 
        notes, 
        order_subtopic 
    FROM note 
    JOIN findings_notes 
        ON note.note_id = findings_notes.note_id 
    WHERE finding_id = ?
'''

select_opening_settings = '''
    SELECT 
        bg,
        highlight_bg,
        head_bg, 
        fg,
        output_font,
        input_font, 
        font_size,
        default_bg,
        default_highlight_bg,
        default_head_bg, 
        default_fg,
        default_output_font,
        default_input_font, 
        default_font_size            
    FROM format
    WHERE format_id = 1
'''

select_person_birth_date = '''
    SELECT 
        finding_id,
        date
    FROM person
    JOIN finding
        ON finding.person_id = person.person_id
    JOIN event_type
        ON finding.event_type_id = event_type.event_type_id 
    WHERE finding.person_id = ?
    AND finding.event_type_id == 1 
'''

select_person_death_date = '''
    SELECT date
    FROM person
    JOIN finding
        ON finding.person_id = person.person_id
    JOIN event_type
        ON finding.event_type_id = event_type.event_type_id 
    WHERE finding.person_id = ?
    AND finding.event_type_id == 4 
'''

select_person_distinct_like = '''
    SELECT DISTINCT 
        person.person_id
    FROM person
    JOIN name
        ON person.person_id = name.person_id
    WHERE names LIKE ? 
        OR person.person_id LIKE ?
'''

select_person_gender = '''
    SELECT gender 
    FROM person 
    JOIN name
        ON person.person_id = name.person_id
    WHERE names = ? AND name_type_id = 1
'''

select_person_id_birth = '''
    SELECT person_id 
    FROM finding
    WHERE finding_id = ?
        AND event_type_id = 1
'''

select_person_id_kin_types_birth = '''
    SELECT person_id1, a.kin_types, person_id2, b.kin_types
    FROM findings_persons
    JOIN kin_type as a
        ON a.kin_type_id = findings_persons.kin_type_id1
    JOIN kin_type as b
        ON b.kin_type_id = findings_persons.kin_type_id2
    WHERE finding_id = ?
'''

select_place = '''
    SELECT places 
    FROM place 
    WHERE place_id = ?
'''

select_place_id = '''
    SELECT place_id
    FROM place
    WHERE places = ?
'''

select_place_id_hint = '''
    SELECT place_id, hint
    FROM place
    WHERE places = ?
'''

select_place_id1 = '''
    SELECT place_id1 
    FROM places_places 
    WHERE place_id2 = ?
'''

select_place_id2 = '''
    SELECT place_id2
    FROM places_places
    WHERE place_id1 = ?
'''

select_place_hint = '''
    SELECT hint
    FROM place
    WHERE place_id = ?
'''

select_places_places_id = '''
    SELECT places_places_id
    FROM places_places
    WHERE place_id1 = ?
        AND (place_id2 = ? OR place_id2 is null)
'''

select_private_note = '''
    SELECT private
    FROM note
    JOIN findings_notes 
        ON note.note_id = findings_notes.note_id
    WHERE note.subtopic = ?
    AND finding_id = ? 
'''

select_related_places = '''
    SELECT nest0, nest1, nest2, nest3, nest4, nest5, nest6, nest7, nest8
    FROM nested_places
    WHERE nest0 = ? OR nest1 = ? OR nest2 = ? OR nest3 = ? OR nest4 = ? 
        OR nest5 = ? OR nest6 = ? OR nest7 = ? OR nest8 = ?
'''

select_roles = '''
    SELECT 
        findings_roles_id, 
        role_types, 
        person_id, 
        findings_roles.role_type_id 
    FROM role_type 
        JOIN findings_roles 
            ON role_type.role_type_id = findings_roles.role_type_id 
    WHERE finding_id = ?
''' 

select_role_types = '''
    SELECT role_types 
    FROM role_type
''' 

select_role_type_id = '''
    SELECT role_type_id 
    FROM role_type 
    WHERE role_types = ?
'''

update_color_scheme_null = '''
    UPDATE format 
    SET (bg, highlight_bg, head_bg, fg) = 
        (null, null, null, null) 
                WHERE format_id = 1
'''

update_current_person = '''
    UPDATE current
    SET person_id = ?
    WHERE current_id = 1
'''

update_current_tree = '''
    UPDATE closing_state 
    SET current_tree = ? 
    WHERE closing_state_id = 1
'''

update_event_types = '''
    UPDATE finding
    SET event_type_id = ?
    WHERE finding_id = ?
'''

update_finding_age = '''
    UPDATE finding 
    SET age = ? 
    WHERE finding_id = ?
'''

update_finding_date = '''
    UPDATE finding
    SET (date, date_sorter) = (?, ?)
    WHERE finding_id = ?
'''

update_finding_particulars = '''
    UPDATE finding 
    SET particulars = ? 
    WHERE finding_id = ?
'''

update_finding_places = '''
    UPDATE finding_places
    SET (nest0, nest1, nest2, nest3, nest4, nest5, nest6, nest7, nest8)
        = ({}) 
    WHERE finding_id = ?
'''.format(','.join(['?'] * 9))

update_finding_places_null = '''
    UPDATE finding_places
    SET (nest0, nest1, nest2, nest3, nest4, nest5, nest6, nest7, nest8)
        = (1, null, null, null, null, null, null, null, null)
    WHERE finding_id = ?    
'''

update_findings_notes = '''
    UPDATE findings_notes 
    SET order_subtopic = ? 
    WHERE finding_id = ?
        AND note_id = ? 
'''

update_findings_persons_1 = '''
    UPDATE findings_persons
    SET person_id1 = ?
    WHERE finding_id = ?
'''

update_findings_persons_2 = '''
    UPDATE findings_persons
    SET person_id2 = ?
    WHERE finding_id = ?
'''

update_findings_persons_1_2 = '''
    UPDATE findings_persons
    SET (person_id1, person_id2) = (?, ?)
    WHERE finding_id = ?
'''

update_findings_persons_age1 = '''
    UPDATE findings_persons
    SET age1 = ?
    WHERE finding_id = ?
        AND person_id1 = ?
'''

update_findings_persons_age2 = '''
    UPDATE findings_persons
    SET age2 = ?
    WHERE finding_id = ?
        AND person_id2 = ?
'''

update_finding_places_new_event = '''
    UPDATE finding_places
    SET (nest0, nest1, nest2, nest3, nest4, nest5, nest6, nest7, nest8) =
        ({})
    WHERE finding_id = ?
'''.format(','.join(['?'] * 9))

update_findings_roles_person = '''
    UPDATE findings_roles 
    SET person_id = ? 
    WHERE findings_roles_id = ?
'''

update_findings_roles_null_person = '''
    UPDATE findings_roles 
    SET person_id = null 
    WHERE findings_roles_id = ?
'''

update_findings_roles_role_type = '''
    UPDATE findings_roles 
    SET role_type_id = ? 
    WHERE findings_roles_id = ?
'''

update_format_color_scheme = '''
    UPDATE format 
    SET (bg, highlight_bg, head_bg, fg) = (?,?,?,?) 
    WHERE format_id = 1
'''

update_format_font = '''
    UPDATE format
    SET (output_font, font_size) = (?, ?)
    WHERE format_id = 1
'''

update_images_entities_zero = '''
    UPDATE images_entities 
    SET main_image = 0 
    WHERE main_image = 1 
        AND images_entities.person_id = ?
'''

update_images_entities_one = '''
    UPDATE images_entities 
    SET main_image = 1
    WHERE image_id = (
        SELECT image_id 
        FROM image WHERE images = ?)
    AND person_id = 
        (SELECT current.person_id 
        FROM current WHERE current_id = 1)
'''

update_kin_type_kin_code = '''
    UPDATE kin_type 
    SET kin_code = ? 
    WHERE kin_type_id = ?
'''

update_note = '''
    UPDATE note
    SET notes = ?
    WHERE subtopic = ?            
'''

update_note_private = '''
    UPDATE note 
    SET private = ? 
    WHERE note_id = ? 
'''

update_note_subtopic = '''
    UPDATE note 
    SET subtopic = ? 
    WHERE note_id = ? 
'''

update_place_hint = '''
    UPDATE place 
    SET hint = ?
    WHERE place_id = ?
'''







