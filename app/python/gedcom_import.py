# gedcom_import.py

import sqlite3
from re import sub
from gedcom_tags import all_tags
from query_strings_gedcom import (
    insert_person, insert_name, update_name, 
    insert_source, delete_person_all, delete_name_all, delete_finding_all, 
    delete_source_all, update_gender_default_person, update_name_default_person,
    insert_finding_default_person, insert_finding_birth, 
)
import dev_tools as dt
from dev_tools import looky, seeline
from gedcom_tags import all_tags





conn = sqlite3.connect("d:/treebard_gps/data/gedcom_import_001/gedcom_import_001.tbd")
cur = conn.cursor()

head = []
trlr = []
line_lists = []
# tags which can occur at level 0
ZERO_LEVEL_TAGS = ("HEAD", "TRLR", "FAM", "INDI", "OBJE", "NOTE", "REPO", "SOUR", "SUBM")
records_dict = {}
for tag0 in ZERO_LEVEL_TAGS:
    records_dict[tag0] = {}
# tags whose lines should always have exactly 2 elements
ELEMS2 = ("HEAD", "GEDC", "PLAC")
# tags whose lines should have only 2 elements, unless the 3rd element is "Y":
ELEMS2Y = ("BIRT", "DEAT", "CHR", "MARR")

def import_gedcom(file):
    """ The `encoding` parameter in `open()` strips `ï»¿` from the front of the 
        first line.
    """

    f = open(file, "r", encoding='utf-8-sig')
    for line_text in f.readlines():
        lst = line_text.strip("\n").split(" ", 2)
        lst[0] = int(lst[0])
        line_lists.append(lst)

def validate_lines():
    """ Add a 4th element to bad lines. """
    for line in line_lists:
        length = len(line)
        tag = line[1]
        if length > 3:
            line.append("too_long")
        elif length > 2:
            if tag in ELEMS2Y:
                if line[2] != "Y":
                    line.append("too_long_y")

def delineate_records():
    tag0 = None
    h = 0
    for line in line_lists:
        if line[0] == 0:
            if line[1] in ("HEAD", "TRLR"):
                tag0 = line[1]
                h = add_subrecords(line, h, tag0)
            elif len(line) > 2:
                tag0 = line[2]
                h = add_subrecords(line, h, tag0)
            else:
                print("line", looky(seeline()).lineno, "case not handled:")
        else:
            pass
    # print("line", looky(seeline()).lineno, "records_dict:", records_dict)
      
def add_subrecords(line, h, tag0):
    copy = records_dict
    pk = line[1]
    subrecords = []
    j = h + 1
    for lst in line_lists[j:]:
        if lst[0] > 0:
            subrecords.append(lst)
            j += 1
        else:
            break
    for k,v in copy.items():
        if k == tag0:
            records_dict[k][pk] = subrecords            
    return j

def input_persons():
    for k,v in records_dict.items():
        if k != "INDI":
            continue
        record = v
        for kk, vv in record.items():
            person_id = kk
            person_data = vv
            z = 0
            for line in person_data:
                parse_line(person_id, line, z)
                z += 1

def input_sources():
    for k,v in records_dict.items():
        if k != "SOUR":
            continue
        record = v
        for kk, vv in record.items():
            source_id = kk
            source_data = vv
            z = 0
            for line in source_data:
                parse_line(source_id, line, z)
                z += 1

def input_families():
    for k,v in records_dict.items():
        if k != "FAM":
            continue
        record = v
        for kk, vv in record.items():
            family_id = kk
            family_data = vv
            z = 0
            for line in family_data:
                parse_line(family_id, line, z)
                z += 1


def parse_line(pk, line, z):
    n = line[0]
    tag = line[1]
    if len(line) == 3:
        data = line[2]
    if n == 1:
        if tag == "NAME":
            add_person(pk, data)
        elif tag == "TITL":
            add_source(pk, data)
        # elif tag in ("HUSB", "WIFE", "CHILD", "SOUR"):
            # add_family(pk, fk)
        parse_next_line(pk, z)

def parse_next_line(person_id, z):
    # print("line", looky(seeline()).lineno, "person_id:", person_id)
    # print("line", looky(seeline()).lineno, "z:", z)
    pass

def add_family(pk, fk):
    pass

def add_source(source_id, title):
    source_id = int(sub("\D", "", source_id))
    cur.execute(insert_source, (source_id, title))
    conn.commit()    

def add_person(person_id, name):
    person_id = int(sub("\D", "", person_id))
    name_list = name.split()
    for i in name_list:
        if i.startswith("/"):
            idx = name_list.index(i)
            x = name_list.pop(idx).strip("/")
            sorter = list(name_list)
            sorter.insert(0, "{},".format(x))
            sorter = " ".join(sorter).strip()
    if person_id != 1:    
        cur.execute(insert_person, (person_id,))
        conn.commit()
        cur.execute(insert_name, (person_id, name, sorter))
        conn.commit()
        cur.execute(insert_finding_birth, (person_id,))
        conn.commit()
    else:
        cur.execute(update_name, (name, sorter))
        conn.commit()
             
def make_unique_tag_lists():
    for lst in line_lists:
        elem_1 = lst[1]
        if elem_1.startswith("@") is False:
            if elem_1.startswith("_"):
                custom_tags.append(elem_1.rstrip("\n"))
            else:
                tags.append(elem_1.rstrip("\n"))
        else:
            if lst[2].startswith("_"):
                custom_tags.append(lst[2].rstrip("\n"))
            else:
                tags.append(lst[2].rstrip("\n"))
    tags = list(set(tags))
    custom_tags = list(set(custom_tags))
# line 50 tags: ['CONC', 'DATE', 'BAPM', 'NCHI', 'PLAC', 'NAME', 'STAE', 'SOUR', 'RESI', 'TIME', 'WILL', 'VERS', 'RELI', 'NATU', 'SSN', 'OCCU', 'GEDC', 'ADDR', 'BIRT', 'HUSB', 'PROB', 'CHIL', 'NMR', 'DSCR', 'MARL', 'CONF', 'CHAN', 'FAMS', 'PAGE', 'PUBL', 'TYPE', 'AUTH', 'MARR', 'HEAD', 'FILE', 'FORM', 'FAM', 'NICK', 'TRLR', 'CHAR', 'CONT', 'DEAT', 'DIV', 'BURI', 'CORP', 'NOTE', 'INDI', 'IMMI', 'CENS', 'WIFE', 'SEX', 'FAMC', 'EVEN', 'TITL']
# line 51 custom_tags: ['_ADDR', '_FLAG', '_PREF', '_PUBLISHER', '_TYPE', '_LEVEL', '_NAME', '_QUAL', '_PUBDATE', '_DETAIL']

elements_dict = {"FAM": "family_id", "INDI": "person_id", "SOUR": "source_id"}

def get_id_type(tag):
    if tag in ("FAM", "INDI", "SOUR"):
        element = elements_dict[tag]
    return element 

def reset_tree():
    cur.execute(update_gender_default_person)
    conn.commit()
    cur.execute(delete_name_all)
    conn.commit()
    cur.execute(update_name_default_person)
    conn.commit()
    cur.execute(delete_finding_all)
    conn.commit()
    cur.execute(insert_finding_default_person)
    conn.commit()
    cur.execute(delete_source_all)
    conn.commit()
    cur.execute(delete_person_all)
    conn.commit()
    

if __name__ == "__main__":
    # # # reset_tree() # DO NOT DELETE AND DO NOT RUN ACCIDENTALLY, ALL DATA WILL BE DELETED***********
    # `_fixed` has had custom tags manually deleted
    import_gedcom("D:/treebard_gps/app/python/todd_boyett_connections_fixed.ged")
    # import_gedcom("D:/treebard_gps/app/python/todd_boyett_connections.ged")
    # import_gedcom("D:/treebard_gps/app/python/robertson_rathbun_family_tree_export_by_gb.ged")
    validate_lines()
    delineate_records()
    # input_persons() # DO NOT DELETE **********************
    # input_sources() # DO NOT DELETE **********************
    # input_families() # DO NOT DELETE **********************


cur.close()
conn.close()



# DO LIST:
# COMMIT TO REPO AND START NEW BRANCH. 
# First get FAM, INDI & SOUR level 1 creation lines into the db then the ones in INDI that I forgot, before trying to get level 2+ in, because these levels will include FK refs that won't be valid till the data is in. FAMC and FAMS have to check whether the FK has already been put in and if so they can be ignored. MAKE/POST GEDCOM VIDEO SEE DO LIST. Add a `changed` table to db and a module to the app, or put the code in utes.py. Then write input_changed(). The only right time to handle subordinate lines is nested inside the for loops that handle the level 1 tags see parse_next_line
# the UNIQUE constraint for sources col in db is prob wrong, get rid of it everywhere
# After it becomes possible to input subordinate lines, change to a larger db that has SUBM, NOTE etc level 0 tags
# Replace switch statements with dicts
# Fix the names input code to handle multiple names. Put alt names back in that I stripped out earlier (see Jimmy, Grace, Lora in unfixed .ged file). From the docs:
# ! Multiple Names:
    # GEDCOM 5.x requires listing different names in different NAME structures, with the preferred
    # instance first, followed by less preferred names. However, Personal Ancestral File and other products
    # that only handle one name may use only the last instance of a name from a GEDCOM transmission.
    # This causes the preferred name to be dropped when more than one name is present. The same thing
    # often happens with other multiple-instance tags when only one instance was expected by the receiving
    # system.
