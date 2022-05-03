# gedcom_import.py

import sqlite3
from re import sub
from gedcom_tags import all_tags
from query_strings_gedcom import insert_person, insert_name, update_name
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
    iD = line[1]
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
            records_dict[k][iD] = subrecords            
    return j


def parse_line(person_id, line):
    n = line[0]
    tag = line[1]
    if len(line) == 3:
        name = line[2]
    if n == 1:
        if tag == 'NAME':
            add_person(person_id, name)

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
    else:
        cur.execute(update_name, (name, sorter))
        conn.commit()

def input_persons():
    for k,v in records_dict.items():
        if k == "INDI":
            record = v
            for kk, vv in record.items():
                person_id = kk
                person_data = vv
                for line in person_data:
                    parse_line(person_id, line)
             
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

if __name__ == "__main__":
    # _fixed has had custom tags manually deleted
    import_gedcom("D:/treebard_gps/app/python/todd_boyett_connections_fixed.ged")
    # import_gedcom("D:/treebard_gps/app/python/todd_boyett_connections.ged")
    # import_gedcom("D:/treebard_gps/app/python/robertson_rathbun_family_tree_export_by_gb.ged")
    validate_lines()
    delineate_records()
    input_persons()


cur.close()
conn.close()



# DO LIST:
