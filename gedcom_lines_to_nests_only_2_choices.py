# gedcom_lines_to_nests_only_2_choices

# Convert text lines to nested dict with nesting depth shown in lines

import dev_tools as dt
from dev_tools import looky, seeline




current_file = "d:/treebard_gps/app/python/test.db"

class GedcomImporter():
    def __init__(self, import_file):
        self.lines = []
        self.prior_n = 0
        self.most_recent_n = {}
        self.read_gedcom(import_file)
        self.parse_lines()
        print("line", looky(seeline()).lineno, "self.most_recent_n:", self.most_recent_n)

    def read_gedcom(self, file):
        """ The `encoding` parameter in `open()` strips `ï»¿` from the front of the 
            first line.
        """
        f = open(file, "r", encoding="utf-8-sig")

        for line in f.readlines(): 
            line = line.rstrip("\n")
            line = line.split(" ", 2)
            if len(line) < 3:
                line.append(None)
            line[0] = int(line[0])
            self.lines.append(line)
          
    def parse_lines(self):
        for idx, line in enumerate(self.lines):
            n, tag, data = line
            self.most_recent_n[n] = idx
            if n == 0:
                self.start_new_record(n, tag, data, idx)
            else:
                self.build_on_branch(n, tag, data, idx)

            self.prior_n = n

    def start_new_record(self, n, tag, data, idx):
        print("line", looky(seeline()).lineno, "n, tag, data, idx:", n, tag, data, idx)

    def build_on_branch(self, n, tag, data, idx):
        print("line", looky(seeline()).lineno, "n, tag, data, idx:", n, tag, data, idx)
        build_here = self.most_recent_n[n-1]
        print("line", looky(seeline()).lineno, "build_here:", build_here)
        

text_file = '''
0 12 PERSON
1 NAME Andy
2 SOURCE newspaper
3 CITE pg 2
1 NAME Andrew
2 SOURCE hearsay
2 ADDRESS 29 E. 10th
0 94 PERSON
1 NAME Darla
2 TYPE aka
2 SOURCE yearbook
3 CITE chap. 5
0 3 COMPANY
1 NAME Ajax
2 ADDRESS 4 South Drive
3 SOURCE Yellow Pages
4 CITE pg 120
0 19 COMPANY
1 NAME Ace
1 TYPE mfg
1 ADDRESS 14th Ave
1 SOURCE Thomas Reg.
2 CITE vol 3 pg 1112
'''

if __name__ == "__main__":

    test_tree = "d:/treebard_gps/app/python/text_file.ged"
    GedcomImporter(test_tree)



'''
The nested dict approach is wrong. Making a dict for everything is the equivalent of making a database, but instead of making a    SQL database, I'm trying to make a NOSQL database which is harder then the eventual goal of making a SQL database. The only right way is to create a class which parses a single record of GEDCOM. The instance vars are used to keep track of what branch I'm in. The depth of each branch is found first. If the depth is < 2, the data goes straight into the db, but there will be almost no UPDATE queries. Then the branch is saved to a small list of lists and that is used to input to db. instance vars are blanked out and the next branch is done. When zero comes back, a new instance.
'''



'''
Each line's leading digit indicates the nesting depth in a dict, so a zero will be the outer key. When a line number increases in the next line, the nesting deepens in the current nest. When line number decreases, a prior nest is indicated for further nesting. When line number is zero, a new outer dict is started. Line numbers can increase only by one, but can decrease by any amount. If the allowed level wasn't up to 99, this might be a lot easier.

The text file below is a simplified representation of a format called GEDCOM invented in 1984 and still being used by genealogists trying to transfer data between software products that can't communicate with each other due to differing data storage structures. There must be an easy way to do this but I've been trying things for two weeks and found nothing that doesn't get real tricky real fast. The end result will be to insert the data into the target software's database, but SQL is easy compared to getting these lines into a usable form. I know how to parse strings but how to use the leading line numbers to indicate nesting level, and switch to the right previous branch when new level < prior level?

In my intended dict, every value except for level 1 is a list of dicts to accomodate multiple values, so that repeated keys don't overwrite the values.

There are a few Python GEDCOM parsers available online for inspection, but a bump in a useful direction from a live human would be appreciated.
'''
