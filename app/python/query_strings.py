# query_strings.py

import dev_tools as dt





'''
	Since Sqlite queries are inserted as string in Python code,
	the queries can be stored here to save space in the modules
	where they are used.
'''

delete_color_scheme = '''
    DELETE FROM color_scheme 
    WHERE color_scheme_id = ?
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

insert_findings_notes = '''
    INSERT INTO findings_notes 
    VALUES (null, ?, ?, ?)
'''

insert_findings_roles = '''
    INSERT INTO findings_roles 
    VALUES (null, ?, ?, ?)
'''

insert_images_entities = '''
    INSERT INTO images_entities (image_id, main_image, person_id) 
    VALUES (?, 1, ?) 
'''

insert_name = '''
    INSERT INTO name 
    VALUES (null, ?, ?, ?, ?, null)
'''

insert_nested_pair = '''
    INSERT INTO places_places (place_id1, place_id2)
    VALUES (?, ?)
'''

insert_nested_places = '''
    INSERT INTO nested_places (
        nest0, nest1, nest2, nest3, nest4, nest5, nest6, nest7, nest8) 
    VALUES ({})
'''.format(','.join(['?'] * 9))

insert_note = '''
    INSERT INTO note 
    VALUES (null, ?, 0, ?)
'''

insert_person_null = '''
    INSERT INTO person VALUES (null, ?) 
'''

insert_place_new = '''
    INSERT INTO place (place_id, places)
    VALUES (null, ?)
'''

insert_role_type = '''
    INSERT INTO role_type VALUES (null, ?, 0, 0)
'''

select_all_color_schemes = '''
    SELECT bg, highlight_bg, table_head_bg, fg 
    FROM color_scheme
'''

select_all_color_schemes_plus = '''
    SELECT bg, highlight_bg, table_head_bg, fg, built_in, color_scheme_id 
    FROM color_scheme
'''

select_all_event_types_couple = '''
    SELECT event_types
    FROM event_type
    WHERE hidden != 1
        AND couple == 1
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

select_all_findings_notes_ids = '''
    SELECT finding_id
    FROM findings_notes
'''

select_all_images = '''
    SELECT images FROM image
'''

select_all_kin_types_couple = '''
    SELECT kin_type_id
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
    SELECT bg, highlight_bg, table_head_bg, fg 
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

select_finding_id_birth = '''
    SELECT finding_id 
    FROM finding
    WHERE event_type_id = 1
        AND person_id = ?
'''

select_finding_ids_age_parents = '''
    SELECT finding_id, age
    FROM findings_persons
    WHERE person_id = ?
        AND kin_type_id in (1, 2)
'''

select_finding_ids_offspring = '''
    SELECT finding_id
    FROM findings_persons
    WHERE person_id = ?
        AND kin_type_id in (1, 2)
'''

select_findings_details_generic = '''
    SELECT event_types, date, date_sorter, nested_places_id, particulars, age
    FROM finding

    JOIN event_type
        ON finding.event_type_id = event_type.event_type_id
    WHERE  finding_id = ?
'''

select_findings_details_couple_age = '''
    SELECT person_id, age, kin_types
    FROM findings_persons
    JOIN kin_type
        ON kin_type.kin_type_id = findings_persons.kin_type_id
    WHERE finding_id = ?
        AND findings_persons.kin_type_id = ?
'''

select_findings_details_couple_generic = '''
    SELECT event_types, date, date_sorter, finding.nested_places_id, particulars 
    FROM finding 
        JOIN nested_places 
            ON nested_places.nested_places_id = finding.nested_places_id 
        JOIN event_type 
            ON finding.event_type_id = event_type.event_type_id 
    WHERE finding_id = ?
'''

select_findings_details_offspring = '''
    SELECT date, date_sorter, finding.nested_places_id, particulars
    FROM finding
    JOIN nested_places
        ON nested_places.nested_places_id = finding.nested_places_id
    WHERE person_id = ?
        AND event_type_id = 1
'''

select_generic_event_roles = '''
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

select_image_id = '''
    SELECT image_id FROM image WHERE images = ?'''

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

select_nested_place_string = '''
    SELECT a.places, b.places, c.places, d.places, 
        e.places, f.places, g.places, h.places, i.places
    FROM nested_places
    LEFT JOIN place a ON a.place_id = nested_places.nest0
    LEFT JOIN place b ON b.place_id = nested_places.nest1
    LEFT JOIN place c ON c.place_id = nested_places.nest2
    LEFT JOIN place d ON d.place_id = nested_places.nest3
    LEFT JOIN place e ON e.place_id = nested_places.nest4
    LEFT JOIN place f ON f.place_id = nested_places.nest5
    LEFT JOIN place g ON g.place_id = nested_places.nest6
    LEFT JOIN place h ON h.place_id = nested_places.nest7
    LEFT JOIN place i ON i.place_id = nested_places.nest8             
    WHERE nested_places_id = ? 
'''

select_first_nested_place = '''
    SELECT a.places, b.places, c.places, d.places, 
        e.places, f.places, g.places, h.places, i.places
    FROM nested_places
    LEFT JOIN place a ON a.place_id = nested_places.nest0
    LEFT JOIN place b ON b.place_id = nested_places.nest1
    LEFT JOIN place c ON c.place_id = nested_places.nest2
    LEFT JOIN place d ON d.place_id = nested_places.nest3
    LEFT JOIN place e ON e.place_id = nested_places.nest4
    LEFT JOIN place f ON f.place_id = nested_places.nest5
    LEFT JOIN place g ON g.place_id = nested_places.nest6
    LEFT JOIN place h ON h.place_id = nested_places.nest7
    LEFT JOIN place i ON i.place_id = nested_places.nest8             
    WHERE nest0 = ? 
'''

select_max_place_id = ''' SELECT MAX(place_id) FROM place '''

select_nested_places_id = '''
    SELECT nested_places_id
    FROM nested_places
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

select_nested_places_same = '''
    SELECT nest0, nest1, nest2, nest3, nest4, nest5, nest6, nest7, nest8
    FROM nested_places
    WHERE nest0 = ?
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
        table_head_bg, 
        fg,
        output_font,
        input_font, 
        font_size,
        default_bg,
        default_highlight_bg,
        default_table_head_bg, 
        default_fg,
        default_output_font,
        default_input_font, 
        default_font_size            
    FROM format
    WHERE format_id = 1
'''

select_person_id_birth = '''
    SELECT person_id 
    FROM finding
    WHERE finding_id = ?
        AND event_type_id = 1
'''

select_person_id_kin_types_birth = '''
    SELECT person_id, kin_types
    FROM findings_persons
    JOIN kin_type
        ON kin_type.kin_type_id = findings_persons.kin_type_id
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

# select_place_place_id = '''
    # SELECT places, place_id
    # FROM place
    # WHERE places = ?
# '''

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

select_all_permanent_dialogs = '''
    SELECT toplevels
    FROM closing_state
    WHERE toplevels != 'tk'                
'''

update_color_scheme_null = '''
    UPDATE format 
    SET (bg, highlight_bg, table_head_bg, fg) = 
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

update_finding_age = '''
    UPDATE finding 
    SET age = ? 
    WHERE finding_id = ?
'''

update_finding_nested_places = '''
    UPDATE finding 
    SET nested_places_id = ? 
    WHERE finding_id = ?
'''

update_finding_particulars = '''
    UPDATE finding 
    SET particulars = ? 
    WHERE finding_id = ?
'''

update_findings_notes = '''
    UPDATE findings_notes 
    SET order_subtopic = ? 
    WHERE finding_id = ?
        AND note_id = ? 
'''

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
    SET (bg, highlight_bg, table_head_bg, fg) = (?,?,?,?) 
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







