# gedcom_import.py

from gedcom_tags import all_tags
import dev_tools as dt
from dev_tools import looky, seeline
from gedcom_tags import all_tags




record_lists = []
record_lines = []
line_lists = []

def import_gedcom(file):
    """ The `encoding` parameter strips `ï»¿` from the front of the first line.
    """
    tags = []
    custom_tags = []
    f = open(file, "r", encoding='utf-8-sig')
    for line_text in f.readlines():
        lst = line_text.split(" ", 2)
        lst[0] = int(lst[0])
        if lst[0] == 0:
            record_lists.append([line_text])
        record_lines.append(line_text)
        line_lists.append(lst)
    g = -1
    for lst in line_lists:
        if lst[0] != 0:
            record_lists[g].append(lst)
        else:
            g += 1
    # print("line", looky(seeline()).lineno, "record_lists:", record_lists)

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
    print("line", looky(seeline()).lineno, "tags:", tags)
    print("line", looky(seeline()).lineno, "custom_tags:", custom_tags)
# line 50 tags: ['CONC', 'DATE', 'BAPM', 'NCHI', 'PLAC', 'NAME', 'STAE', 'SOUR', 'RESI', 'TIME', 'WILL', 'VERS', 'RELI', 'NATU', 'SSN', 'OCCU', 'GEDC', 'ADDR', 'BIRT', 'HUSB', 'PROB', 'CHIL', 'NMR', 'DSCR', 'MARL', 'CONF', 'CHAN', 'FAMS', 'PAGE', 'PUBL', 'TYPE', 'AUTH', 'MARR', 'HEAD', 'FILE', 'FORM', 'FAM', 'NICK', 'TRLR', 'CHAR', 'CONT', 'DEAT', 'DIV', 'BURI', 'CORP', 'NOTE', 'INDI', 'IMMI', 'CENS', 'WIFE', 'SEX', 'FAMC', 'EVEN', 'TITL']
# line 51 custom_tags: ['_ADDR', '_FLAG', '_PREF', '_PUBLISHER', '_TYPE', '_LEVEL', '_NAME', '_QUAL', '_PUBDATE', '_DETAIL']


    



if __name__ == "__main__":
    import_gedcom("D:/treebard_gps/app/python/robertson_rathbun_family_tree_export_by_gb.ged")






# DO LIST:
'''
['0 @I4@ INDI\n', 
	[1, 'NAME', 'David /Todd/\n'], 
		[2, 'SOUR', '@S2@\n'], 
			[3, 'PAGE', '10 September 1962, page 2, Samuel F. Todd obituary\n'], 
	[1, 'SEX', 'M\n'], 
	[1, 'RESI\n'], 
		[2, 'DATE', '1962\n'], 
		[2, 'PLAC', 'Meridian, Lauderdale County, Mississippi\n'], 
		[2, 'SOUR', '@S2@\n'], 
			[3, 'PAGE', '10 September 1962, page 2, Samuel F. Todd obituary\n'], 
	[1, 'RESI\n'], 
		[2, 'DATE', '1962\n'], 
		[2, 'PLAC', 'Gulfport, Harrison County, Mississippi\n'], 
		[2, 'SOUR', '@S2@\n'], 
			[3, 'PAGE', '26 June 1962, page 2, obituary, "Mrs. Lora Grace Smith"\n'], 
	[1, 'RESI\n'], 
		[2, 'DATE', '1985\n'], 
		[2, 'PLAC', 'Gulfport, Harrison County, Mississippi\n'], 
		[2, 'SOUR', '@S3@\n'], 
			[3, 'PAGE', '"MRS. NORA NAOMI TODD", obituary, date and place of publication unknown\n'], 
		[2, 'SOUR', '@S4@\n'], 
			[3, 'PAGE', 'findagrave member no. 48611078\n'], 
	[1, 'FAMC', '@F2@\n'], 
	[1, 'SOUR', '@S2@\n'], 
		[2, 'PAGE', '10 September 1962, page 2, Samuel F. Todd obituary\n'], 
	[1, 'CHAN\n'], 
		[2, 'DATE', '17 AUG 2015\n'], 
			[3, 'TIME', '20:56:36\n']], 
































'''