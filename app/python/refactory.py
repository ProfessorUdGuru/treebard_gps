# refactory.py

from re import sub
import dev_tools as dt
from dev_tools import looky, seeline



# line 97 self.subs: {'EVEN', 'NOTE', 'TIME', 'BIRT', 'SOUR', 'OCCU', 'SEX', 'CAUS', 'TITL', 'CHAN', 'DATE', 'DEAT', 'PAGE', 'RELI', 'TYPE', 'NAME', 'HUSB', 'WIFE', 'AGE', 'FAMC', 'CHIL', 'RESI', 'BURI', 'CONC', 'PLAC', 'FAMS'}
current_file = "d:/treebard_gps/app/python/test.dtb"
# ZERO_LEVEL_TAGS = ("FAM", "INDI", "OBJE", "NOTE", "REPO", "SOUR", "SUBM")
# MISSING_PK_TAGS = (
    # 'EVEN', 'NOTE', 'OCCU', 'DEAT', 'PAGE', 'RELI', 'NAME', 'RESI', 'BURI', 'PLAC')

class GedcomImporter():
    def __init__(self, import_file):
        self.lines = []
        self.export = []
        self.current_record = None
        self.head = []
        self.citations_vault = set()
        self.name_id = 1
        self.citation_id = 0
        self.person_id = None
        self.source_id = None

        self.read_gedcom(import_file)

        for idx, line in enumerate(self.lines):
            n, tag, data = line              

        self.parse_lines()

        print("line", looky(seeline()).lineno, "self.export:", self.export)
        print("line", looky(seeline()).lineno, "self.citations_vault:", self.citations_vault)

    def read_gedcom(self, file):
        """ The `encoding` parameter in `open()` strips `ï»¿` from the front of the 
            first line.
        """
        in_head = True
        f = open(file, "r", encoding="utf-8-sig")

        for line in f.readlines(): 
            line = line.rstrip("\n")
            line = line.split(" ", 2)
            if len(line) < 3:
                line.append(None)
            line[0] = int(line[0])

            if in_head is False:
                self.lines.append(line)
            elif line[1] == "HEAD":
                self.head.append(line)
            elif line[0] == 0:
                in_head = False
                self.lines.append(line)
            else:
                self.head.append(line)
        if self.lines[-1][1] == "TRLR":
            self.lines.pop()
        else:
            print("TRLR tag missing from end of file.")

    def parse_lines(self):
        for line in self.lines:
            pk = None
            data = None
            if line[0] == 0:
                pk, tag = line[1:]
                pk = int(sub("\D", "", pk))
                if tag == "INDI":
                    self.person_id = pk
                    self.export.append(["person", {}, {"person_id": pk}, {}])
                elif tag == "SOUR":
                    self.source_id = pk
                    self.export.append(["source", {}, {"source_id": pk}, {}])
                elif tag == "FAM":
                    pass
                elif tag == "OBJE":
                    pass
                elif tag == "NOTE":
                    pass
                elif tag == "REPO":
                    pass
                elif tag == "SUBM":
                    pass
            else:
                tag, data = line[1:]
                if tag == "NAME":
                    if self.person_id != 1:
                        self.name_id += 1
                    name, sorter = self.sort_name(data)
                    self.export.append([
                        "name", {}, {
                            "name_id": self.name_id, "names": name, 
                            "sort_order": sorter, "person_id": self.person_id}, {}])
                elif tag == "SEX":
                    if data == "M":
                        data = "male"
                    elif data == "F":
                        data = "female"
                    self.export.append(
                        ["persons", {}, {}, 
                            {"gender": data, "person_id": self.person_id}])
                elif tag == "SOUR":
                    self.source_id = int(sub("\D", "", data))
                elif tag == "PAGE":
                    self.citations_vault.add((
                        "citation", "", 
                        (("citation_id", None), ("citations", data), 
                            ("source_id", self.source_id))))
                    # when vault is used, id will be added and links_links record added for each unique and for each not unique, links_links only will have a record added



# THIS ONLY DEALS WITH LINKING names to citations
    def make_new_citation(self, data):
        print("line", looky(seeline()).lineno, "making_new:")
        self.citation_id += 1
        self.export.append([
            "citation", "insert", 
            {'citation_id': self.citation_id, 
            'citations': data, 'source_id': self.source_id}])
        self.export.append([
            "links_links", "insert",
            {"name_id": self.name_id, "citation_id": self.citation_id}])

    def update_citation(self):
        print("line", looky(seeline()).lineno, "updating:")
        self.export.append([
            "links_links", "insert",
            {"name_id": self.name_id, "citation_id": self.citation_id}])






    def add_name(self, n, data, idx):
        name, sorter = self.sort_name(data)
        name_id = self.name_id
        self.name_id += 1
        self.instrux[idx]["name_id"] = name_id


        self.export.append(
            [{"name_id": name_id}, {"names": name, "sort_order": sorter}, self.person_id])




   

    def add_citation(self, ref, data, idx):
        # print("line", looky(seeline()).lineno, "ref, data, idx:", ref, data, idx)
        if ref.get("source_id"):
            source_id = ref["source_id"]
        if ref.get("citation_id") is None:
            citation_id = self.citation_id
            self.citation_id += 1
        else:
            citation_id = ref["citation_id"]
        self.export.append([{"citation_id": citation_id}, {"citations": data}, ref])
        self.instrux[idx]["citation_id"] = citation_id
# CITATION NOT GOING IN RIGHT
# IT SHD GO IN ONCE AND THEN THE FK SHD BE USED IN LINKS_LINKS
    def save_source(self, ref, data, idx):
        if ref.get("name_id"):
            name_id = ref["name_id"]
        else:
            return
        fk = int(sub("\D", "", data))
        # print("line", looky(seeline()).lineno, "fk:", fk)
        # print("line", looky(seeline()).lineno, "name_id:", name_id)
        self.instrux[idx]["source_id"] = fk
        self.instrux[idx]["name_id"] = name_id  

    def sort_name(self, data):
        name_list = data.split()
        for i in name_list:
            if i.startswith("/"):
                idx = name_list.index(i)
                x = name_list.pop(idx).strip("/")
                sorter = list(name_list)
                sorter.insert(0, "{},".format(x))
                sorter = " ".join(sorter).strip()
        name_list.insert(idx, x)
        name = " ".join(name_list)
        return name, sorter

if __name__ == "__main__":

    test_tree = "d:/treebard_gps/etc/todd_boyett_connections_fixed.ged"

    GedcomImporter(test_tree)




