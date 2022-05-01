# gedcom_import.py

from re import sub
from gedcom_tags import all_tags
import dev_tools as dt
from dev_tools import looky, seeline
from gedcom_tags import all_tags





head = []
record_lines = []
line_lists = []
# tags which can occur at level 0
ZERO_LEVEL_TAGS = ("FAM", "INDI", "OBJE", "NOTE", "REPO", "SOUR", "SUBM")
records_dict = {}
for tag0 in ZERO_LEVEL_TAGS:
    records_dict[tag0] = []
print("line", looky(seeline()).lineno, "records_dict:", records_dict)
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
        record_lines.append(line_text)
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
        if tag0 == "HEAD":
            continue
        elif line[0] == 0 and len(line) > 2:
            tag0 = line[2]
            h = add_subrecords(line, h, tag0)
        else:
            pass
    print("line", looky(seeline()).lineno, "records_dict:", records_dict)

            
            
      
def add_subrecords(line, h, tag0):
    subrecords = []
    j = h + 1
    for lst in line_lists[j:-1]:
        if lst[0] > 0:
            subrecords.append(lst)
            j += 1
        else:
            break
    # print("line", looky(seeline()).lineno, "j:", j)
    records_dict[tag0].append(subrecords)
    return j




    # tags = []
    # custom_tags = []
    # f = open(file, "r", encoding='utf-8-sig')
    # for line_text in f.readlines():
        # lst = line_text.split(" ", 2)
        # lst[0] = int(lst[0])
        # if lst[0] == 0:
            # record_lists.append([line_text])
        # record_lines.append(line_text)
        # line_lists.append(lst)
    # g = -1
    # for lst in line_lists:
        # if lst[0] != 0:
            # record_lists[g].append(lst)
        # else:
            # g += 1

# def make_unique_tag_lists():
    # for lst in line_lists:
        # elem_1 = lst[1]
        # if elem_1.startswith("@") is False:
            # if elem_1.startswith("_"):
                # custom_tags.append(elem_1.rstrip("\n"))
            # else:
                # tags.append(elem_1.rstrip("\n"))
        # else:
            # if lst[2].startswith("_"):
                # custom_tags.append(lst[2].rstrip("\n"))
            # else:
                # tags.append(lst[2].rstrip("\n"))
    # tags = list(set(tags))
    # custom_tags = list(set(custom_tags))
    # print("line", looky(seeline()).lineno, "tags:", tags)
    # print("line", looky(seeline()).lineno, "custom_tags:", custom_tags)
# line 50 tags: ['CONC', 'DATE', 'BAPM', 'NCHI', 'PLAC', 'NAME', 'STAE', 'SOUR', 'RESI', 'TIME', 'WILL', 'VERS', 'RELI', 'NATU', 'SSN', 'OCCU', 'GEDC', 'ADDR', 'BIRT', 'HUSB', 'PROB', 'CHIL', 'NMR', 'DSCR', 'MARL', 'CONF', 'CHAN', 'FAMS', 'PAGE', 'PUBL', 'TYPE', 'AUTH', 'MARR', 'HEAD', 'FILE', 'FORM', 'FAM', 'NICK', 'TRLR', 'CHAR', 'CONT', 'DEAT', 'DIV', 'BURI', 'CORP', 'NOTE', 'INDI', 'IMMI', 'CENS', 'WIFE', 'SEX', 'FAMC', 'EVEN', 'TITL']
# line 51 custom_tags: ['_ADDR', '_FLAG', '_PREF', '_PUBLISHER', '_TYPE', '_LEVEL', '_NAME', '_QUAL', '_PUBDATE', '_DETAIL']

elements_dict = {"FAM": "family_id", "INDI": "person_id", "SOUR": "source_id"}

def get_id_type(tag):
    if tag in ("FAM", "INDI", "SOUR"):
        element = elements_dict[tag]
    return element

# def parse_idents():
    # r = 1
    # for lst in record_lists[1:-1]:
        # iD = lst[0]
        # iD = iD.split()
        # lst[0] = [int(iD[0]), int(sub("\D", "", iD[1])), get_id_type(iD[2].rstrip("\n"))]
        # r += 1

# def parse_sublevels():
    
    # for lst in record_lists[1:-1]:
        
        # for line in lst:
            # new = line[0]
            # prior = new - 1
            # if new == 0:
                # continue
            # elif new != prior:
                # continue
            # elif new == prior:
                # print("line", looky(seeline()).lineno, "go back a level:")
            
        
            
            
            
            
        
                

    



if __name__ == "__main__":
    import_gedcom("D:/treebard_gps/app/python/robertson_rathbun_family_tree_export_by_gb.ged")
    validate_lines()
    delineate_records()






# DO LIST:

# detect notes w/out ids and add a pointer like this: `1 NOTE @N0466@` and an identifier like this: 
''