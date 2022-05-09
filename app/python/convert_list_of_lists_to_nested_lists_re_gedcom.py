# convert_list_of_lists_to_nested_lists_re_gedcom


from re import sub
import dev_tools as dt
from dev_tools import looky, seeline



fam_records = [
    [[1, 'HUSB', '@I5@'], [1, 'WIFE', '@I6@'], [1, 'CHIL', '@I4@'], [1, 'CHIL', '@I7@'], [1, 'CHIL', '@I8@'], [1, 'CHIL', '@I9@'], [1, 'CHIL', '@I10@'], [1, 'CHIL', '@I11@'], [1, 'CHIL', '@I13@'], [1, 'CHIL', '@I29@'], [1, 'CHIL', '@I33@'], [1, 'SOUR', '@S2@'], [2, 'PAGE', '10 September 1962, page 2, Samuel F. Todd obituary'], [1, 'CHAN'], [2, 'DATE', '17 AUG 2015'], [3, 'TIME', '20:57:54']],
 
	[[1, 'HUSB', '@I12@'], [1, 'WIFE', '@I11@'], [1, 'SOUR', '@S2@'], [2, 'PAGE', '10 September 1962, page 2, Samuel F. Todd obituary'], [1, 'CHAN'], [2, 'DATE', '17 AUG 2015'], [3, 'TIME', '18:21:23']]] 

# model = [[], None, None]
# goal = [[4, 7, 8, 9, 10, 11, 13, 29, 33], 5, 6]

def parse_foreign_keys():
    families = []
    for record in fam_records:
        model = [[], None, None]
        for lst in record:
            tag = lst[1]
            if tag not in ('HUSB', 'WIFE', 'CHIL'):
                continue
            fk = int(sub("\D", "", lst[2]))
            if tag == 'HUSB':
                model[1] = fk
            elif tag == 'WIFE':
                model[2] = fk
            elif tag == 'CHIL':
                model[0].append(fk)
        families.append(model)
    return families

families = parse_foreign_keys()

print("line", looky(seeline()).lineno, "families:", families)
# line 39 families: [[[4, 7, 8, 9, 10, 11, 13, 29, 33], 5, 6], [[], 12, 11]]

