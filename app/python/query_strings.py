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

delete_claim_person = '''
    DELETE FROM claim
    WHERE person_id = ?
'''

delete_claims_roles_person = '''
    DELETE FROM claims_roles
    WHERE person_id = ?
'''

delete_color_scheme = '''
    DELETE FROM color_scheme 
    WHERE color_scheme_id = ?
'''

delete_date_format_all = '''DELETE FROM date_format'''
   
delete_finding = '''
    DELETE FROM finding
    WHERE finding_id = ?    
'''

delete_finding_person = '''
    DELETE FROM finding
    WHERE person_id = ?
'''

delete_finding_places = '''
    DELETE FROM finding_places
    WHERE finding_id = ?
'''

delete_findings_notes_linked = '''
    DELETE FROM findings_notes
    WHERE findings_notes_id = ?
'''

delete_findings_notes_finding = '''
    DELETE FROM findings_notes
    WHERE finding_id = ?
'''

delete_findings_persons = '''
    DELETE FROM findings_persons
    WHERE finding_id = ?
'''

delete_findings_roles_finding = '''
    DELETE FROM findings_roles
    WHERE finding_id = ?
''' 

delete_findings_role = '''
    DELETE FROM findings_roles 
    WHERE findings_roles_id = ?
'''

delete_findings_roles_person = '''
    DELETE FROM findings_roles
    WHERE person_id = ?
'''

delete_images_elements_person = '''
    DELETE FROM images_elements
    WHERE person_id = ?
'''

delete_links_links_name = '''
    DELETE FROM links_links
    WHERE name_id = ?
'''

delete_links_links_person = '''
    DELETE FROM links_links
    WHERE person_id = ?
'''

delete_name_person = '''
    DELETE FROM name
    WHERE person_id = ?
'''

delete_person = '''
    DELETE FROM person
    WHERE person_id = ?
'''

delete_persons_persons = '''
    DELETE FROM persons_persons
    WHERE persons_persons_id = ?
'''

insert_color_scheme = '''
    INSERT INTO color_scheme 
    VALUES (null, ?, ?, ?, ?, 0, 0)
'''

insert_date_format_default = '''
    INSERT INTO date_format 
    VALUES (
        1, 'dmy', 'abt', 'est', 'cal', 'bef/aft', 'BCE/CE', 
        'OS/NS', 'from_to', 'btwn_&')
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

insert_finding_birth_new_person = '''
    INSERT INTO finding 
    VALUES (null, '-0000-00-00-------', '', '0', ?, 1, '0,0,0')
'''

insert_finding_new_couple = '''
    INSERT INTO finding (finding_id, event_type_id)
    VALUES (?, ?)
'''

insert_findings_notes_new = '''
    INSERT INTO findings_notes 
    VALUES (null, ?, ?, 0)
'''

insert_findings_persons_new_couple = '''
    INSERT INTO findings_persons (
        finding_id, age1, kin_type_id1, age2, kin_type_id2, persons_persons_id)
    VALUES (?, ?, 128, ?, 129, ?)
'''

insert_findings_persons_new_father = '''
    INSERT INTO findings_persons (finding_id, age1, kin_type_id1, age2, kin_type_id2, persons_persons_id)
    VALUES (?, '', 2, '', null, ?)
'''

insert_findings_persons_new_mother = '''
    INSERT INTO findings_persons (finding_id, age1, kin_type_id1, age2, kin_type_id2, persons_persons_id)
    VALUES (?, '', null, '', 1, ?)
'''

insert_findings_persons_null_couple = '''
    INSERT INTO findings_persons
    VALUES (null, ?, '', ?, '', ?, ?)
'''

select_findings_persons_ppid = '''
    SELECT persons_persons_id
    FROM findings_persons
    WHERE findings_persons_id = ?
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

insert_findings_roles = '''
    INSERT INTO findings_roles 
    VALUES (null, ?, ?, ?)
'''

insert_image_new = '''
    INSERT INTO image
    VALUES (null, ?, '')
'''

insert_images_elements = '''
    INSERT INTO images_elements (image_id, main_image, person_id) 
    VALUES (?, 1, ?) 
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

insert_persons_persons = '''
    INSERT INTO persons_persons (person_id1, person_id2)
    VALUES (?, ?)
'''

insert_persons_persons_null = '''
    INSERT INTO persons_persons
    VALUES (null, null, null)
'''

insert_persons_persons_father = '''
    INSERT INTO persons_persons (person_id1)
    VALUES (?)
'''

insert_persons_persons_mother = '''
    INSERT INTO persons_persons (person_id2)
    VALUES (?)
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
    SELECT color_scheme_id, bg, highlight_bg, head_bg, fg, built_in, hidden
    FROM color_scheme
'''

select_all_color_schemes_hidden = '''
    SELECT color_scheme_id, bg, highlight_bg, head_bg, fg, built_in, hidden
    FROM color_scheme
    WHERE hidden = 1
'''

select_all_color_schemes_unhidden = '''
    SELECT color_scheme_id, bg, highlight_bg, head_bg, fg, built_in, hidden
    FROM color_scheme
    WHERE hidden = 0
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

select_all_person_images = '''
    SELECT DISTINCT images, caption, main_image
    FROM images_elements
        JOIN person
            ON images_elements.person_id = person.person_id
        JOIN image
            ON image.image_id = images_elements.image_id 
    WHERE images_elements.person_id = ?
'''

select_all_place_ids = '''
    SELECT place_id
    FROM place
'''

select_all_place_images = '''
    SELECT images, caption, main_image, places
    FROM images_elements
        JOIN place
            ON images_elements.place_id = place.place_id 
        JOIN current
            ON current.place_id = place.place_id
        JOIN image
            ON image.image_id = images_elements.image_id 
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
    SELECT images, caption, main_image, sources, citations
    FROM images_elements
        JOIN source
            ON citation.source_id = source.source_id
        JOIN citation
            ON images_elements.citation_id = citation.citation_id
        JOIN current
            ON current.citation_id = citation.citation_id
        JOIN image
            ON image.image_id = images_elements.image_id 
'''

select_closing_state_openpic = '''
    SELECT openpic
    FROM closing_state
    WHERE closing_state_id = 1
'''

select_closing_state_recent_files = '''
    SELECT recent_files
    FROM closing_state
    WHERE closing_state_id = 1
'''

select_closing_state_prior_tree = '''
    SELECT prior_tree 
    FROM closing_state 
    WHERE closing_state_id = 1
'''

select_color_scheme_by_id = '''
    SELECT bg, highlight_bg, head_bg, fg
    FROM color_scheme
    WHERE color_scheme_id = ?
'''

select_color_scheme_current_id = '''
    SELECT color_scheme_id
    FROM current
    WHERE current_id = 1
'''

select_count_finding_id_sources = '''
    SELECT COUNT(finding_id) 
        FROM claims_findings 
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
    SELECT current.person_id, names 
    FROM name 
    JOIN person 
        ON person.person_id = name.person_id 
    JOIN current 
        ON person.person_id = current.person_id
'''

select_current_person_id = '''
    SELECT person_id 
    FROM current 
    WHERE current_id = 1'''

select_current_person_image = '''
    SELECT images 
    FROM image 
        JOIN images_elements 
            ON image.image_id = images_elements.image_id 
    WHERE main_image = 1 
        AND images_elements.person_id = ?
'''

select_default_date_format = '''
    SELECT default_date_formats, default_abt, default_est, default_cal,
        default_bef_aft, default_bc_ad, default_os_ns, default_span, 
        default_range
    FROM default_date_format
    WHERE default_date_format_id = 1
'''

select_closing_state_tree_is_open = '''
    SELECT tree_is_open
    FROM closing_state
    WHERE closing_state_id = 1
'''

select_date_format = '''
    SELECT date_formats, abt, est, cal, bef_aft, bc_ad, os_ns, span, range
    FROM date_format
    WHERE date_format_id = 1
'''

select_date_finding = '''
    SELECT date
    FROM finding
    WHERE finding_id = ?
'''

select_default_formats = '''
    SELECT 
        default_bg,
        default_highlight_bg,
        default_head_bg, 
        default_fg,
        default_output_font,
        default_input_font, 
        default_font_size            
    FROM default_format
    WHERE default_format_id = 1
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

select_event_type_by_finding = '''
    SELECT event_types
    FROM event_type
    JOIN finding
        ON finding.event_type_id = event_type.event_type_id
    WHERE finding_id = ?
'''

select_event_type_id = '''
    SELECT event_type_id, couple
    FROM event_type
    WHERE event_types = ?
'''

select_event_type_id_only = '''
    SELECT event_type_id
    FROM event_type
    WHERE event_types = ?
'''

select_event_type_string = '''
    SELECT event_types
    FROM event_type
    WHERE event_type_id = ?
'''

select_event_type_via_event_string = '''
    SELECT event_type_id
    FROM event_type
    WHERE event_types = ?
'''

select_finding_date = '''
    SELECT date
    FROM finding
    WHERE finding_id = ?
'''

select_finding_date_and_sorter = '''
    SELECT date, date_sorter
    FROM finding
    WHERE finding_id = ?
'''

select_finding_details = '''
    SELECT finding_id, date, event_types
    FROM finding
    JOIN event_type
        ON finding.event_type_id = event_type.event_type_id
    WHERE finding_id = ?
'''

select_finding_event_type = '''
    SELECT event_type_id
    FROM finding
    WHERE finding_id = ?
'''

select_finding_id_adoption = '''
    SELECT finding_id 
    FROM finding
    WHERE event_type_id = 83
        AND person_id = ?
'''

select_finding_id_birth = '''
    SELECT finding_id 
    FROM finding
    WHERE event_type_id = 1
        AND person_id = ?
'''

select_finding_id_death = '''
    SELECT finding_id 
    FROM finding
    WHERE event_type_id = 4
        AND person_id = ?
'''

select_finding_id_fosterage = '''
    SELECT finding_id 
    FROM finding
    WHERE event_type_id = 95
        AND person_id = ?
'''

select_finding_id_guardianship = '''
    SELECT finding_id 
    FROM finding
    WHERE event_type_id = 48
        AND person_id = ?
'''

select_finding_ids_age1_alt_parents = '''
    SELECT finding_id, age1
    FROM person
    JOIN persons_persons
        ON persons_persons.person_id1 = person.person_id
    JOIN findings_persons
        ON findings_persons.persons_persons_id = persons_persons.persons_persons_id
    WHERE person_id1 = ?
        AND kin_type_id1 in (1, 2, 110, 111, 112, 120, 121, 122, 130, 131)
'''

select_finding_ids_age2_alt_parents = '''
    SELECT finding_id, age2
    FROM person  
    JOIN persons_persons
        ON persons_persons.person_id2 = person.person_id
    JOIN findings_persons
        ON findings_persons.persons_persons_id = persons_persons.persons_persons_id
    WHERE person_id2 = ?
        AND kin_type_id2 in (1, 2, 110, 111, 112, 120, 121, 122, 130, 131)
'''

select_finding_ids_age1_parents = '''
    SELECT finding_id, age1
    FROM person
    JOIN persons_persons
        ON persons_persons.person_id1 = person.person_id
    JOIN findings_persons
        ON findings_persons.persons_persons_id = persons_persons.persons_persons_id
    WHERE person_id1 = ?
        AND kin_type_id1 in (1, 2)
'''

select_finding_ids_age2_parents = '''
    SELECT finding_id, age2
    FROM person  
    JOIN persons_persons
        ON persons_persons.person_id2 = person.person_id
    JOIN findings_persons
        ON findings_persons.persons_persons_id = persons_persons.persons_persons_id
    WHERE person_id2 = ?
        AND kin_type_id2 in (1, 2)
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
    SELECT persons_persons.person_id1, age1, a.kin_types,
        persons_persons.person_id2, age2, b.kin_types
    FROM persons_persons
    JOIN findings_persons
        ON findings_persons.persons_persons_id = persons_persons.persons_persons_id
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

select_findings_details_offspring_alt_parentage = '''
    SELECT date, date_sorter, particulars, finding_places_id
    FROM finding
    JOIN finding_places
        ON finding_places.finding_id = finding.finding_id
    WHERE person_id = ?
        AND event_type_id IN (1, 48, 83, 95)
        AND finding.finding_id = ?
'''

select_findings_for_person = '''
    SELECT event_types
    FROM finding
    JOIN event_type
        ON finding.event_type_id = event_type.event_type_id
    WHERE person_id = ?
'''

select_findings_notes_order = '''
    SELECT topic_order, findings_notes_id
    FROM findings_notes
    WHERE finding_id = ?
'''

select_findings_persons_age = '''
    SELECT age
    FROM findings_persons
    WHERE person_id = ?
        AND finding_id = ?
'''

select_findings_persons_alt_parents = '''
    SELECT person_id1, age1, kin_type_id1, person_id2, age2, kin_type_id2
    FROM findings_persons
    JOIN persons_persons
        ON persons_persons.persons_persons_id = findings_persons.persons_persons_id
    WHERE finding_id = ?
'''

select_findings_persons_birth = '''
    SELECT findings_persons_id, persons_persons_id
    FROM findings_persons
    WHERE finding_id = ?
'''

select_findings_persons_id_kin_type1 = '''
    SELECT findings_persons_id
    FROM findings_persons
    WHERE finding_id = ?
'''

select_findings_persons_id = '''
    SELECT findings_persons_id
    FROM findings_persons
    WHERE finding_id = ?
'''

select_findings_persons_id_kin_type2 = '''
    SELECT findings_persons_id
    FROM findings_persons
    WHERE finding_id = ?
'''


select_findings_persons_person_id = '''
    SELECT a.person_id1, b.person_id2, a.persons_persons_id
    FROM findings_persons
    JOIN persons_persons as a
        ON a.person_id1 = person.person_id
    JOIN persons_persons as b
        ON b.person_id2 = person.person_id
    WHERE finding_id = ?
'''

select_findings_persons_parents = '''
    SELECT a.person_id1, b.person_id2
    JOIN persons_persons as a
        ON a.person_id1 = person.person_id
    JOIN persons_persons as b
        ON b.person_id2 = person.person_id
    FROM findings_persons
    WHERE finding_id = ?
'''

select_findings_persons_ppid = '''
    SELECT persons_persons_id 
    FROM findings_persons
    WHERE findings_persons_id = ?
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

select_default_format_font_size = '''
    SELECT default_font_size
    FROM default_format
    WHERE default_format_id = 1
'''

select_format_font_size = '''
    SELECT font_size, default_font_size
    FROM format
    WHERE format_id = 1
'''

select_format_font_scheme = '''
    SELECT output_font, font_size, default_output_font, default_font_size
    FROM format
    WHERE format_id = 1
'''

select_image_id = '''
    SELECT image_id FROM image WHERE images = ?
'''

select_images_elements_main_image = '''
    SELECT images
    FROM images_elements
        JOIN person
            ON images_elements.person_id = person.person_id 
        JOIN image
            ON image.image_id = images_elements.image_id 
    WHERE images_elements.main_image = 1
        AND images_elements.person_id = ?
'''

select_kin_type_alt_parent = '''
    SELECT kin_types, kin_type_id
    FROM kin_type
    WHERE kin_code = 'B'
        AND kin_type_id NOT IN (1, 2, 3, 26, 27, 28)
'''

select_kin_type_string = '''
    SELECT kin_types FROM kin_type WHERE kin_type_id = ?
'''

select_kin_types_finding = '''
    SELECT kin_types
    FROM kin_type
    JOIN findings_persons
        ON kin_type.kin_type_id = findings_persons.kin_type_id1
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

select_name_person = '''
    SELECT name_id
    FROM name
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

select_notes_linked = '''
    SELECT findings_notes_id
    FROM findings_notes
    JOIN note
        ON note.note_id = findings_notes.note_id
    WHERE topic = ?
        AND finding_id = ?
'''

select_notes_per_finding = '''
    SELECT topic, notes
    FROM note 
    JOIN findings_notes
        ON findings_notes.note_id = note.note_id
    WHERE finding_id = ?
    ORDER BY topic_order
'''

select_note_id = '''
    SELECT note_id
    FROM note
    WHERE topic = ?
'''

select_note_privacy = '''
    SELECT private
    FROM note
    WHERE topic = ?
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

select_opening_settings_on_load = '''
    SELECT 
        default_bg,
        default_highlight_bg,
        default_head_bg, 
        default_fg,
        default_output_font,
        default_input_font, 
        default_font_size            
    FROM default_format
    WHERE default_format_id = 1
'''

select_person = '''
    SELECT person_id 
    FROM finding
    WHERE finding_id = ?
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
        AND finding.event_type_id = 1 
'''

select_person_death_date = '''
    SELECT date
    FROM person
    JOIN finding
        ON finding.person_id = person.person_id
    JOIN event_type
        ON finding.event_type_id = event_type.event_type_id 
    WHERE finding.person_id = ?
    AND finding.event_type_id = 4 
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

select_person_id_alt_parentage = '''
    SELECT person_id 
    FROM finding
    WHERE finding_id = ?
        AND event_type_id in (110, 111, 112, 120, 121, 122, 130, 131)
'''

select_person_id_gender = '''
    SELECT gender 
    FROM person
    WHERE person_id = ?
'''

select_person_id_finding = '''
    SELECT person_id 
    FROM finding
    WHERE finding_id = ?
'''

select_person_ids_kin_types = '''
    SELECT person_id1, a.kin_types, person_id2, b.kin_types
    FROM findings_persons
    JOIN persons_persons
        ON findings_persons.persons_persons_id = persons_persons.persons_persons_id
    JOIN kin_type as a
        ON a.kin_type_id = findings_persons.kin_type_id1
    JOIN kin_type as b
        ON b.kin_type_id = findings_persons.kin_type_id2
    WHERE finding_id = ?
'''

select_person_ids_kin_types_include_nulls = '''
    SELECT person_id1, a.kin_types, person_id2, b.kin_types
    FROM findings_persons
    LEFT JOIN persons_persons
        ON findings_persons.persons_persons_id = persons_persons.persons_persons_id
    LEFT JOIN kin_type as a
        ON a.kin_type_id = findings_persons.kin_type_id1
    LEFT JOIN kin_type as b
        ON b.kin_type_id = findings_persons.kin_type_id2
    WHERE finding_id = ?
'''

select_persons_persons = '''
    SELECT person_id1, person_id2
    FROM persons_persons
    WHERE persons_persons_id = ?
'''

select_persons_persons_ma_id1 = '''   
    SELECT person_id1
    FROM person
    JOIN persons_persons
        ON persons_persons.person_id1 = person.person_id    
    JOIN findings_persons
        ON findings_persons.persons_persons_id = persons_persons.persons_persons_id
    WHERE kin_type_id1 = 1
        AND finding_id = ?
'''

select_persons_persons_ma_id2 = '''   
    SELECT person_id2
    FROM person
    JOIN persons_persons
        ON persons_persons.person_id1 = person.person_id    
    JOIN findings_persons
        ON findings_persons.persons_persons_id = persons_persons.persons_persons_id
    WHERE kin_type_id2 = 1
        AND finding_id = ?
'''

select_persons_persons_pa_id1 = '''   
    SELECT person_id1
    FROM person
    JOIN persons_persons
        ON persons_persons.person_id1 = person.person_id    
    JOIN findings_persons
        ON findings_persons.persons_persons_id = persons_persons.persons_persons_id
    WHERE kin_type_id1 = 1
        AND finding_id = ?
'''

select_persons_persons_pa_id2 = '''   
    SELECT person_id2
    FROM person
    JOIN persons_persons
        ON persons_persons.person_id1 = person.person_id    
    JOIN findings_persons
        ON findings_persons.persons_persons_id = persons_persons.persons_persons_id
    WHERE kin_type_id2 = 1
        AND finding_id = ?
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

select_app_setting_openpic_dir = '''
    SELECT openpic_dir, default_openpic_dir
    FROM app_setting
    WHERE app_setting_id = 1
'''

update_claims_persons_1_null = '''
    UPDATE claims_persons
    SET person_id1 = null
    WHERE person_id1 = ?
'''

update_claims_persons_2_null = '''
    UPDATE claims_persons
    SET person_id2 = null
    WHERE person_id2 = ?
'''

update_closing_state_openpic = '''
    UPDATE closing_state
    SET openpic = ?
    WHERE closing_state_id = 1
'''

update_closing_state_recent_files = '''
    UPDATE closing_state
    SET recent_files = ?
    WHERE closing_state_id = 1
'''

update_closing_state_tree = '''
    UPDATE closing_state 
    SET prior_tree = ? 
    WHERE closing_state_id = 1
'''

update_closing_state_tree_is_closed = '''
    UPDATE closing_state
    SET tree_is_open = 0
    WHERE closing_state_id = 1
'''

update_closing_state_tree_is_open = '''
    UPDATE closing_state
    SET tree_is_open = 1
    WHERE closing_state_id = 1
'''

update_color_scheme_hide = '''
    UPDATE color_scheme
    SET hidden = 1
    WHERE color_scheme_id = ?
'''

update_current_person = '''
    UPDATE current
    SET person_id = ?
    WHERE current_id = 1
'''

update_date_format_abt = '''
    UPDATE date_format 
    SET abt = ? 
    WHERE date_format_id = 1
'''

update_date_format_befaft = '''
    UPDATE date_format 
    SET bef_aft = ? 
    WHERE date_format_id = 1
'''

update_date_format_cal = '''
    UPDATE date_format 
    SET cal = ? 
    WHERE date_format_id = 1
'''

update_date_format_date_formats = '''
    UPDATE date_format 
    SET date_formats = ? 
    WHERE date_format_id = 1
'''

update_date_format_epoch = '''
    UPDATE date_format 
    SET bc_ad = ? 
    WHERE date_format_id = 1
'''

update_date_format_est = '''
    UPDATE date_format 
    SET est = ? 
    WHERE date_format_id = 1
'''

update_date_format_julegreg = '''
    UPDATE date_format 
    SET os_ns = ? 
    WHERE date_format_id = 1
'''

update_date_format_range = '''
    UPDATE date_format 
    SET range = ? 
    WHERE date_format_id = 1
'''

update_date_format_span = '''
    UPDATE date_format 
    SET span = ? 
    WHERE date_format_id = 1
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

update_finding_places_new_event = '''
    UPDATE finding_places
    SET (nest0, nest1, nest2, nest3, nest4, nest5, nest6, nest7, nest8) =
        ({})
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

update_findings_notes_order = '''
    UPDATE findings_notes
    SET topic_order = ?
    WHERE findings_notes_id = ?
'''

update_findings_persons_age1 = '''
    UPDATE findings_persons
    SET age1 = ?
    WHERE finding_id = ?
        AND persons_persons_id = ?
'''

update_findings_persons_age2 = '''
    UPDATE findings_persons
    SET age2 = ?
    WHERE finding_id = ?
        AND persons_persons_id = ?
'''

update_findings_persons_age1_blank = '''
    UPDATE findings_persons
    SET age1 = ""
    WHERE findings_persons_id = ?
'''

update_findings_persons_age2_blank = '''
    UPDATE findings_persons
    SET age2 = ""
    WHERE findings_persons_id = ?
'''

update_findings_persons_finding = '''
    UPDATE findings_persons
    SET finding_id = ?
    WHERE findings_persons_id = ?
'''

update_findings_persons_kin_type1 = '''
    UPDATE findings_persons
    SET kin_type_id1 = ?
    WHERE findings_persons_id = ?
'''

update_findings_persons_kin_type2 = '''
    UPDATE findings_persons
    SET kin_type_id2 = ?
    WHERE findings_persons_id = ?
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

update_current_color_scheme = '''
    UPDATE current  
    SET color_scheme_id = ?
    WHERE current_id = 1
'''

update_current_color_scheme_default = '''
    UPDATE current  
    SET color_scheme_id = 1
    WHERE current_id = 1
'''

update_format_font = '''
    UPDATE format
    SET (output_font, font_size) = (?, ?)
    WHERE format_id = 1
'''

update_images_elements_zero = '''
    UPDATE images_elements 
    SET main_image = 0 
    WHERE main_image = 1 
        AND images_elements.person_id = ?
'''

update_images_elements_one = '''
    UPDATE images_elements 
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

update_note_edit = '''
    UPDATE note 
    SET notes = ?
    WHERE topic = ?
'''

update_note_privacy = '''
    UPDATE note
    SET private = ?
    WHERE topic = ?
'''

update_note_topic = '''
    UPDATE note
    SET topic = ?
    WHERE topic = ?
'''

update_persons_persons_1 = '''
    UPDATE persons_persons
    SET person_id1 = ?
    WHERE persons_persons_id = ?
'''

update_persons_persons_1_null = '''
    UPDATE persons_persons
    SET person_id1 = null
    WHERE person_id1 = ?
'''

update_persons_persons_1_null_by_id = '''
    UPDATE persons_persons
    SET person_id1 = null
    WHERE persons_persons_id = ?
'''

update_persons_persons_2 = '''
    UPDATE persons_persons
    SET person_id2 = ?
    WHERE persons_persons_id = ?
'''

update_persons_persons_2_null = '''
    UPDATE persons_persons
    SET person_id2 = null
    WHERE person_id2 = ?
'''

update_persons_persons_2_null_by_id = '''
    UPDATE persons_persons
    SET person_id2 = null
    WHERE persons_persons_id = ?
'''

update_persons_persons1_by_finding = '''
    UPDATE persons_persons
    SET person_id1 = ?
    WHERE persons_persons_id = (
        SELECT persons_persons_id
        FROM findings_persons
        WHERE finding_id = ?)
'''

update_persons_persons2_by_finding = '''
    UPDATE persons_persons
    SET person_id2 = ?
    WHERE persons_persons_id = (
        SELECT persons_persons_id
        FROM findings_persons
        WHERE finding_id = ?)
'''

update_place_hint = '''
    UPDATE place 
    SET hint = ?
    WHERE place_id = ?
'''







