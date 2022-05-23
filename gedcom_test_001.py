# gedcom_test_001.py

import sqlite3
from re import sub
import dev_tools as dt
from dev_tools import looky, seeline



current_file = "d:/treebard_gps/app/python/test.db"

ZERO_LEVEL_TAGS = ("HEAD", "TRLR", "FAM", "INDI", "OBJE", "NOTE", "REPO", "SOUR", "SUBM")
ELEMS2Y = ("BIRT", "DEAT", "CHR", "MARR")

def define_range():
    nums = []
    for n in range(1, 100):
        nums.append(str(n))
    return tuple(nums)

one_99 = define_range()

class GedcomImporter():
    def __init__(self, import_file):
        # current_file = get_current_file()[0]
        self.exceptions_dict = {}
        self.persons = {}
        self.families = {}
        self.sources = {}
        self.past_head = False
        self.this_level = 0
        self.prior_level = 0
        self.curr_id = None
        self.ident = None
        self.zero_tag = None
        self.branch = []
        self.conn = sqlite3.connect(current_file)
        self.cur = self.conn.cursor()
        self.read_gedcom(import_file)
        self.cur.close()
        self.conn.close()

        print("line", looky(seeline()).lineno, "self.persons:", self.persons)
        print("line", looky(seeline()).lineno, "self.families:", self.families)
        print("line", looky(seeline()).lineno, "self.sources:", self.sources)

    def read_gedcom(self, file):
        """ The `encoding` parameter in `open()` strips `ï»¿` from the front of the 
            first line.
        """
        f = open(file, "r", encoding="utf-8-sig")

        for line in f.readlines(): 
            line = line.rstrip("\n")
            print("line", looky(seeline()).lineno, "line:", line)
            self.prior_level = self.this_level
            self.this_level = int(line[0])
            if line.startswith("0"):
                if line.endswith(("HEAD", "TRLR")):
                    continue
                self.past_head = True
                self.start_new_record(line)
            elif line.startswith(one_99):
                if self.past_head is False:
                    continue
                self.nest_in_existing_record(line)
            else:
                print("line", looky(seeline()).lineno, "not handled", line)
            print("line", looky(seeline()).lineno, "self.prior_level:", self.prior_level)
            print("line", looky(seeline()).lineno, "self.this_level:", self.this_level)

        f.close()
        print("line", looky(seeline()).lineno, "self.branch:", self.branch)

    def start_new_record(self, line):
        line = line.split(" ", 2)
        self.ident = line[1]
        self.curr_id = int(sub("\D", "", self.ident))
        self.zero_tag = line[2]
        if self.zero_tag == "INDI":
            self.persons[self.ident] = {}
        elif self.zero_tag == "FAM":
            self.families[self.ident] = {}
        elif self.zero_tag == "SOUR":
            self.sources[self.ident] = {}

    def nest_in_existing_record(self, line):
        data = None

        line = line.split(" ", 2)
        n = line[0]
        tag = line[1]
        if len(line) == 2:
            line.append(None)
        data = line[2]

        if n == "1":
            self.next_level = {data: {}}
            self.prior_value = {tag: [self.next_level]}            
            self.branch = self.prior_value

        elif self.this_level == self.prior_level:
            pass

        elif self.this_level < self.prior_level:
            pass

        elif self.this_level > self.prior_level:
            print("line", looky(seeline()).lineno, "self.branch:", self.branch)
            print("line", looky(seeline()).lineno, "self.next_level:", self.next_level)
        
            





    
# line 41 self.persons: {'@I2@': {'FAMC': ['@F2@'], 'FAMS': ['@F1@'], 'SEX': ['M']}, '@I3@': {'FAMC': ['@F2@'], 'FAMS': ['@F1@'], 'SEX': ['F']}, '@I4@': {'RESI': {}, 'PLAC': ['Gulfport, Harrison County, Mississippi'], 'SOUR': ['@S2@']}, '@I5@': {'BIRT': {}, 'PLAC': ['Salem Methodist Church Cemetery, Quitman, Clarke County, Mississippi'], 'SOUR': ['@S2@'], 'FAMS': ['@F5@']}, '@I6@': {'RESI': {}, 'PLAC': ['Salem Cemetery'], 'SOUR': ['@S2@'], 'AGE': ['79y'], 'FAMS': ['@F2@']}, '@I7@': {'EVEN': {}, 'DATE': ['1962'], 'PLAC': ['San Diego, California'], 'SOUR': ['@S2@']}, '@I8@': {'RESI': {}, 'PLAC': ['Gulfport, Harrison County, Mississippi'], 'SOUR': ['@S2@']}, '@I9@': {'RESI': {}, 'PLAC': ['Gulfport, Harrison County, Mississippi'], 'SOUR': ['@S2@']}, '@I10@': {'RESI': {}, 'PLAC': ['Gulfport, Harrison County, Mississippi'], 'SOUR': ['@S2@']}, '@I11@': {'RESI': {}, 'PLAC': ['Belle Glade, Palm Beach County, Florida'], 'SOUR': ['@S2@'], 'FAMS': ['@F3@']}, '@I12@': {'FAMS': ['@F3@'], 'SOUR': ['@S2@']}, '@I13@': {'RESI': {}, 'PLAC': ['Bessemer, Jefferson County, Alabama'], 'SOUR': ['@S2@'], 'FAMS': ['@F4@']}, '@I14@': {'FAMS': ['@F4@'], 'SOUR': ['@S2@']}, '@I15@': {'FAMS': ['@F5@'], 'SOUR': ['@S2@']}, '@I16@': {'RESI': {}, 'PLAC': ['Moss, Jasper County, Mississippi'], 'SOUR': ['@S2@'], 'FAMS': ['@F6@']}, '@I17@': {'FAMS': ['@F6@'], 'SOUR': ['@S3@']}, '@I18@': {'OCCU': ['wood dealer'], 'SOUR': ['@S4@'], 'CAUS': ['a fellow struck him with an axe while he was walking home'], 'CHAN': {}}, '@I20@': {'RESI': {}, 'PLAC': ['Meridian, Lauderdale County, Mississippi'], 'SOUR': ['@S3@'], 'FAMS': ['@F8@']}, '@I21@': {'FAMS': ['@F8@'], 'SOUR': ['@S3@']}, '@I22@': {'RESI': {}, 'PLAC': ['Quitman, Clarke County, Mississippi'], 'SOUR': ['@S3@'], 'FAMS': ['@F9@']}, '@I23@': {'FAMS': ['@F9@'], 'SOUR': ['@S3@']}, '@I24@': {'FAMS': ['@F7@'], 'SOUR': ['@S4@']}, '@I25@': {'FAMC': ['@F7@'], 'SOUR': ['@S4@']}, '@I26@': {'FAMC': ['@F7@'], 'SOUR': ['@S4@']}, '@I27@': {'FAMC': ['@F7@'], 'SOUR': ['@S4@']}, '@I28@': {'FAMC': ['@F7@'], 'SOUR': ['@S4@']}, '@I29@': {'BIRT': {}, 'PLAC': ['Salem Methodist Church Cemetery, Quitman, Clarke County, Mississippi'], 'SOUR': ['@S5@'], 'FAMS': ['@F10@']}, '@I30@': {'FAMS': ['@F10@'], 'SOUR': ['@S2@']}, '@I31@': {'RESI': {}, 'PLAC': ['Montrose, Jasper County, Mississippi'], 'SOUR': ['@S2@']}, '@I32@': {'RESI': {}, 'PLAC': ['Montrose, Jasper County, Mississippi'], 'SOUR': ['@S2@']}, '@I33@': {'RESI': {}, 'PLAC': ['Detroit, Michigan'], 'SOUR': ['@S2@']}}

# line 42 self.families: {'@F1@': {}, '@F2@': {}, '@F3@': {}, '@F4@': {}, '@F5@': {}, '@F6@': {}, '@F7@': {}, '@F8@': {}, '@F9@': {}, '@F10@': {}}

# line 43 self.sources: {'@S2@': {}, '@S3@': {}, '@S4@': {}, '@S5@': {}}


if __name__ == "__main__":

    test_tree = "d:/treebard_gps/etc/todd_boyett_connections_fixed.ged"

    def reset_tree():
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(update_gender_default_person)
        conn.commit()
        cur.execute(delete_name_all)
        conn.commit()
        cur.execute(insert_name_default_person)
        conn.commit()
        cur.execute(delete_finding_all)
        conn.commit()
        cur.execute(insert_finding_default_person)
        conn.commit()
        cur.execute(delete_source_all)
        conn.commit()
        cur.execute(delete_person_all)
        conn.commit()
        cur.execute(delete_places_places_all)
        conn.commit()
        cur.execute(delete_place_all)
        conn.commit()
        cur.close()
        conn.close()

    # reset_tree()
    GedcomImporter(test_tree)