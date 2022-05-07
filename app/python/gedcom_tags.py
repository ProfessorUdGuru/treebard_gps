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

no_fam_tag_sources = "The GEDCOM `FAM` tag is used during import to Treebard only to determine relationships of persons within the family. If you had linked a source only to a family, you should link it in Treebard to those family members elucidated by the source. If you didn't link the source to a family unit, then your software must have decided to add a link to a family unit that was created by the software itself to match GEDCOM's structure. If you know you didn't link sources to family units in the original, then ignore these links, since Treebard doesn't create redundant family IDs on top of the individual and relationship data which already exist in the database."