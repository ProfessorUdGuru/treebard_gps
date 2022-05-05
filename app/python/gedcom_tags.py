# gedcom_tags
# https://wiki-en.genealogy.net/GEDCOM-Tags


all_tags = (
    "ABBR", "ADDR", "ADR1", "ADR2", "ADOP", "AFN", "AGE", "AGNC", 
    "ALIA", "ANCE", "ANCI", "ANUL", "ASSO", "AUTH", "BAPL", "BAPM",
    "BARM", "BASM", "BIRT", "BLES", "BLOB", "BURI", "CALN", "CAST", 
    "CAUS", "CENS", "CHAN", "CHAR", "CHIL", "CHR", "CHRA", "CITY",
    "CONC", "CONF", "CONL", "CONT", "COPR", "CORP", "CREM", "CTRY",
    "DATA", "DATE", "DEAT", "DESC", "DESI", "DEST", "DIV", "DIVF",
    "DSCR", "EDUC", "EMAIL", "EMIG", "ENDL", "ENGA", "EVEN", "FACT",
    "FAM", "FAMC", "FAMF", "FAMS", "FAX", "FCOM", "FILE", "FONE",
    "FORM", "GEDC", "GIVN", "GRAD", "HEAD", "HUSB", "IDNO", "IMMI",
    "INDI", "LANG", "LATI", "LEGA", "LONG", "MAP", "MARB", "MARC", 
    "MARL", "MARR", "MARS",  "MEDI", "NAME",  "NATI", "NATU", "NCHI", 
    "NICK", "NMR", "NOTE", "NPFX", "NSFX",  "OBJE", "OCCU", "ORDI",
    "ORDN", "PAGE", "PEDI", "PHON", "PLAC", "POST", "PROB", "PROP",
    "PUBL", "QUAY", "REFN", "RELA", "RELI", "REPO", "RESI", "RESN",
    "RETI", "RFN", "RIN",  "ROLE", "ROMN", "SEX", "SLGC", "SLGS",
    "SOUR", "SPFX", "SSN", "STAE", "STAT", "SUBM", "SUBN", "SURN",
    "TEMP", "TEXT", "TIME",  "TITL", "TRLR", "TYPE", "VERS", "WIFE",
    "WWW", "WILL")

no_fam_tag_sources = "The GEDCOM `FAM` tag is used during import to Treebard only to determine relationships of persons within the family. Chances are that if you linked a source to a family in the genealogy software that wrote the imported GEDCOM, you could look at the source again now and manually link it in Treebard to only those persons in the family that are actually elucidated by the source. But it's also probable that you originally linked the source to something other than a family unit when originally inputing the source, and then the software decided to add it to a family unit that was created by the software to match the expectations of GEDCOM's structure. If you know you didn't link sources to family units in the original, then there is nothing for you to do, since the software that created the GEDCOM probably did not delete your original link when creating the family unit expected by GEDCOM."