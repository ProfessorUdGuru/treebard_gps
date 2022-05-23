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

baseless_fams_tags = "The GEDCOM 'FAMS' tag was used in the imported .ged file to indicate couples even though no event or child supported the status of the couple as a couple. Treebard has created an undated marriage event for these couples which you can change to a different event type if you like. You can delete the event, and this will not delete the individuals from the tree, but the couple will no longer be displayed as a couple. It might be better to change the marriage event to a cohabitation event, for example. You can also change the kin type of the two persons by double-clicking the 'spouse' label in the family table where the current person's partners are shown. These event IDs are subordinate to these person IDs:"

no_fam_tag_sources = "The GEDCOM `FAM` tag is used during import to Treebard only to determine\nrelationships of persons within the family. If you had linked a source only\nto a family, you should link it in Treebard to those family members elucidated\nby the source. If you didn't link the source to a family unit, then your\nsoftware must have decided to add a link to a family unit that was created by\nthe software itself to match GEDCOM's structure. If you know you hadn't linked\nsources to family units in the original, then ignore these links, since\nTreebard doesn't create redundant family IDs on top of the individual and\nrelationship data which already exist in the database. These source IDs are\nsubordinate to these family IDs:"

unmatched_famc_tags = "These individuals from the imported tree have to be entered into Treebard by\ncreating new persons. These family IDs are subordinate to these person IDs:"

rant1 = "Please ask your genealogy software vendor to assist in the replacement of the\ninadequate GEDCOM standard by 1) making their data-storage structure publicly\navailable so other vendors can interface with it directly, thus potentially\nbeing able to import all of the source vendor's data accurately, and\n2) participating in a cooperative effort to create a universal SQLite database\nmodel which all vendors can use as their native data structure while retaining\ntheir corporate individuality by way of their distinct user interfaces."