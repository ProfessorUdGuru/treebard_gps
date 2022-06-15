# links.py

'''
    The elements of genealogy are those things which get their own database table, for the most part, and are endowed with unique ID numbers. The 
    element category names are listed in the constant `ELEMENTS`. The most 
    key elements such as persons, places, events, notes, images and others 
    will be referenced in one or more specialized junction tables or foreign 
    key tables. More straightforward elements can all be lumped together in 
    one junction table in the database called `links_links`. The two plurals 
    in the table name indicate that it's a many-to-many table. For example, a 
    to-do can be linked to any number of projects and a project can be linked 
    to any number of to-dos. In order to do this, a separate row in a database table is used for each link. So in links_links, generally there will be only two values besides the ID, and these values will be foreign keys, i.e. references to primary keys or ID numbers from primary tables.

    There are also tables that store one-to-many relationships, such as 
    `finding_places` which associates one finding (conclusion: event or 
    attribute) with a whole nested hierarchy of places. Elements with 
    one-to-one relationships can be stored together in a general table, 
    as values or as foreign keys referencing a primary key in a primary 
    table. 

    Primary tables exist for each of the elements so that each unique member 
    of each element category will have its own primary key or unique ID number
    within that category. To link two elements together, they get their own 
    row in links_links or another junction table, and the other columns in the
    table will all be null except for links_links_id, a primary key which might
    never be used.

    Some special elements exist which have two sets of names because I didn't 
    want to type long words. Conclusions and assertions are basic design 
    elements which exist separate from each other, but conclusions can 
    optionally be based on assertions while assertions must be based on 
    citations which must be based on sources. Sources can be linked to 
    repositories optionally. Conclusions are separated into events and 
    attributes in the GUI depending on whether or not the element is 
    officially associated with a date (event) or not (attribute). Attributes 
    can become events by having a date added and events can be changed to
    attributes by having the date removed or added optionally to a 
    `particulars` or `note` column where it won't be officially recognized as 
    a date. In the code, conclusions are called `findings` and assertions are
    called `claims`.

    Some elements are pre-loaded with types in primary type tables, while some
    are completely open-ended so aren't linked to types, such as projects and to-dos which can be linked to each other and anything else, but are not linked to any underlying primary type table. Type tables never have a foreign key in them, but their primary key is always used as a foreign key in other tables. Primary type tables underlie many somewhat primary tables such as the finding table which stores events and attributes as findings (conclusions). It includes an event_type_id column for foreign keys. The findings_persons table includes foreign key references to finding table IDs and kin type IDs (or "relationships" as they're called in ELEMENTS.)

    Event types are used equally for conclusions and assertions (findings and claims.)

    There's such a thing as splitting hairs too much. Treebard doesn't track
    jurisdiction types such as "county", "parish", "township", "city", etc. as it 
    would be nearly impossible to do it well but adds nothing to the research. 
    I could think of no reason to classify sources by type. Is it a census or a gravestone? Isn't it obvious? But I might re-think this when I start working
    on that part of the design. I think it would be silly to have types for citations. Is it a page number or a line number or a chapter number? Just say say it, that's what citations are. "Volume 5, Chapter 7, page 162".

    On the other hand, while the word "county" is part of the place name in Ireland and the US, in England it's just "Leicester", not "Leicester County". So jurisdicational categories would add some detail, but I don't think they would add detail that should be used to perform logic operations. A column could be added to the place table for jurisdiction, but it would just be a detail to display, not the basis for Treebard to draw any conclusions. Similarly, gender exists as a category but in our modern times we can no longer get away with using gender to assign spousal terminology. The user has to be given free reign to assign his own descriptions to a relationship, so relationships (called "kin" in the code) are one category that the user can add new members to as he sees fit. 

    Treebard recognizes three genders: male, female and unknown. If another is added for the purpose of political correctness, it would be something non-descript such as "other" so as to not take sides or tie the design to the political arguments popular in 2021. We recognize biologically-imposed categories but don't use gender to enforce anything except the roles of biologal mother and father in regards to offspring.
'''

ELEMENTS = (
    "persons", "places", "assertions", "conclusions", "citations", "names", "sources", "projects", "to-dos", "contacts", "images", "notes", "repositories", "reports", "charts", "media", "relationships", "roles")