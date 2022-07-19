# error_messages.py

from tkinter import StringVar, IntVar
import dev_tools as dt
from dev_tools import looky, seeline





places_err = (
    "A place cannot contain itself.\n\nSelect a "
        "chain of places that are nested inside each other.",
)

main_msg = (
    "To create a new person in a person autofill field, type a plus sign after the "
        "name of the new person. If you type the plus sign within the name, it will "
        "be moved automatically to the end of the name. ",
)

findings_msg = (
    "The same person was used twice.",
    "A second person must be entered for a couple event.",
    "Offspring events can't be changed to other event types. You "
        "can delete the conclusion and make a new conclusion.",
    "A couple event can't be changed to a non-couple event, or "
        "vice-versa. For example, a marriage can be changed to "
        "a wedding but a death can't be changed to a divorce. "
        "Delete unwanted events and create new ones to "
        "replace them if they're incompatible in this way. To "
        "delete a conclusion, delete the event type in the first column.",
    "A conclusion is about to be deleted. This can't be undone. For "
        "couple events, the conclusion will be deleted for both partners. To "
        "delete only one of the partners from a couple event, delete the "
        "partner's name from the family table instead. To delete an offspring "
        "event, delete the child's name from the current person's family table. "
        "To delete a birth event, make the deletable person the current person "
        "and delete the person from the tree.",
    "Each person has one birth and one death event. To add more "
        "hypothetical birth or death events, add them as assertions "
        "instead of conclusions. The events table is for conclusions, "
        "but assertions can be added freely by clicking the SOURCES "
        "button at the end of the birth or death conclusion row or by "
        "going directly to the assertions tab if you prefer to make "
        "no conclusions at this time.",
    "A non-offspring event can't be changed to an offspring event. "
        "You can delete the conclusion and make a new conclusion.",
    "Offspring events can't be created directly. Create a new person "
        "and give them parents, and the parents' offspring events "
        "will be created automatically.",
    "The event type doesn't exist. Create a new event type in the Types "
        "tab, and try again.",
    "Birth events are created automatically when a new person is added to the "
        "tree. To delete a birth event, delete the person from the tree.",
)

persons_msg = (
    "This name already exists in the tree. To create a "
        "new person by the same name, click OK. The "
        "two persons can be merged later if desired.",
    "The name type doesn't exist. Create it in the Types Tab and try again.",
    "There's no record of the person ID entered.",
)

notes_msg = (
    "Any note can be linked to any number of entities.",
    "The current note can be linked to any number of other elements "
        "inclucing persons, places, assertions, conclusions, citations, "
        "names, sources, projects, do list items, contacts, images, etc. "
        "For each link, select an element type, then fill in the name of the "
        "element. Pressing OK will save the link input, leaving the dialog "
        "open for further link inputs till DONE is pressed.",
    "Type a unique subtopic name for the new note.",
    "Each subtopic can be used once in a tree.",
    "Blank notes are OK but not blank note titles.",
    "The selected note will be unlinked from the current event or attribute "
        "only. To permanently delete the note and its topic listing and all "
        "its links, press CANCEL and delete the note in the Links tab.",
    "The selected note will be deleted and will no longer be linked to any "
        "tree element that it's currently linked to. To prevent permanent "
        "loss of this text, you might prefer to (1) unlink it from elements "
        "selectively in the Links tab, or (2) change its setting to 'private' "
        "so it won't be shared. To proceed with permanent deletion, press OK.",
)

dates_msg = (
    "One of the words 'and' or 'to' can be used once in a compound date. "
        "Input should be like 'feb 27 1885 to 1886' for 'from 27 Feb 1885 to 1886' "
        "or '1884 and mar 1885' for 'between 1884 and March 1885'.",
    "One month is allowed per date. For compound dates, the two dates have to be "
        "separated by 'and' or 'to'.",
    "For compound dates connected by 'and' or 'to', two months are possible. For "
        "single dates there can only be one month.",
    "If no month is input, no day can be input. The date will be deleted and the "
        "event will be moved to the Attributes Table. To return the event to the "
        "Events Table, give it a valid date. Numerical date input is not "
        "possible.",
    "Each part of a compound date can have one prefix and one suffix. Each single "
        "date can have one prefix and one suffix. Prefixes include est, abt, bef, aft, "
        "and cal. Suffixes include AD, BC, CE, BCE, NS and OS.",
    "One date includes only one year.",
    "Date input included too many numerical terms. Input months as text, for "
        "example: feb for February, jul for July, may for May, etc.",
    "Each single date can include a maximum of five terms. Each compound date can "
        "include five terms in each part plus a link ('and' or 'to) between the two "
        "parts. The parts within a date can be in any order, for example 'nov 1885 14 "
        "est bc' for 'estimated 14 Nov 1885 BC'.",
    "Day and year are input as numbers. Months are input as abbreviated text "
        "such as mar, sep, dec. The date input seems to be lacking numerical input.",
    "A compound date should include two distinct and complete single dates "
        "separated by 'and' or 'to'. Treebard translates input separated by 'and' into "
        "a range such as 'between 1885 and 1886'. Compound dates separated by 'to' are "
        "translated into a span such as 'from 1912 to Feb 1915'. The input was for two "
        "identical dates. ",
    "That month doesn't have that many days. In leap years, February has 29 days. "
        "Leap years are evenly divisible by 4.",
    "Type the year as a four-digit number. For example, the year 33 should be "
        "typed as 0033.",
    "A 4-digit year must be entered. For years prior to the year 1000, add "
        "leading zeroes. For example, for the year 12 AD or the year 12 BC, "
        "type '0012' without the quotation marks. Or for the year 108, type "
        "'0108'.",
    "All years should have four digits, e.g. '1894', '0033', '0925'. The year "
        "'9999' is maximum in either the CE or BCE era (AD or BC). The date "
        "been deleted and the event has been moved to the Attributes Table. "
        "To return the event to the Events Table, give it a valid date.",
)

# fonts_msg = (
    # "Press ALT+P then CTRL+S to resize the scrollbar after changing fonts.",
# )

opening_msg = (
    "The requested file has been moved, deleted or renamed outside "
        "of Treebard's controls. To use the file, restore it to its original "
        "folder and name. Any file changes should be made from within Treebard "
        "using Treebard's tools.",
    "Treebard will use your title as the tree's display title. "
        "Treebard will save 'Marge M. Smith Family Tree' as a database file at `{current "
        "drive}/treebard_gps/data/marge_m_smith_family_tree/marge_m_smith_family_tree.tbd`",
    "This feature is not complete. Please visit https://treebard.proboards.com if "
        "you would like to assist or advise regarding development of this feature.",
)

colorizer_msg = (
    "The color scheme already exists. Change at least one color to make a new "
        "color scheme.",
    "The color scheme already exists, but is hidden. To unhide it, go to the "
        "Types Tab. To use it as a model for a new color scheme, change at least "
        "one color.",
)

families_msg = (
    "",
    main_msg[0],
    # "To create a new person in a person autofill field, type a plus sign after the "
        # "name of the new person. If you type the plus sign within the name, it will "
        # "be moved automatically to the end of the name. ",
    # "To change an existing parent, delete the parent and tab out, then add a "
        # "parent to the blank field.",
)

roles_msg = (
    families_msg[1],
)


