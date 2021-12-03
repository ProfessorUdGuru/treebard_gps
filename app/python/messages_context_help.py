# messages_context_help.py

from widgets import LabelH3
import dev_tools as dt

'''
    This module is used to store strings used as messages 
    in right-click context help menus.
'''

# Custom messages used in one place:

# rcm_widgets = (
    # self.test1, 
    # self.tester_widgets['Date Input I'], 
    # self.tester_widgets['Date Input II'],
    # self.tester_widgets['Date Input III'], 
    # self.pref_lab, self.general, 
    # dates.date_pref_combos['General'], 
    # dates.date_pref_combos['Estimated'], 
    # dates.date_pref_combos['Approximate'], 
    # dates.date_pref_combos['Calculated'], 
    # dates.date_pref_combos['Before/After'], 
    # dates.date_pref_combos['Epoch'], 
    # dates.date_pref_combos['Julian/Gregorian'],
    # dates.date_pref_combos['From...To...'], 
    # dates.date_pref_combos['Between...And...'], 
    # self.submit, 
    # self.revert)
date_prefs_help_msg = (
    ('The date entry demo section at the top of the Date Preferences '
    'tab allows you to test various ways of inputting and displaying '
    'dates. Nothing you enter here will affect your tree, but the '
    'three input fields are exact working models of every date input '
    'field in Treebard. For more info, right-click for context help in '
    'each of the three input fields.', 
    'Date Settings Tab: Date Entry Demo'),

    ('Here\'s a list of '
    'ways that date qualifiers can be input and displayed:\n\n'
    "separators: [space, dash, slash, asterisk or underscore]\n\n"
    'estimated dates: ["est", "est.", "est\'d"]\n\n'
    'approximate dates: ["abt", "about", "circa", "ca", "ca.", "approx."]\n\n'
    'calculated dates: ["cal", "calc", "calc.", "cal.", "calc\'d"]'
    'before dates: ["bef", "bef.", "before"]\n\n'
    'after dates: ["aft", "aft.", "after"]\n\n'
    'before current era: ["BCE", "BC", "B.C.E.", "B.C."]\n\n'
    'current era: ["CE", "AD", "C.E.", "A.D."]\n\n'
    'Julian calendar: ["OS", "O.S.", "old style", "Old Style"]\n\n'
    'Gregorian calendar: ["NS", "N.S.", "new style", "New Style"]'
    "January: ['ja', 'ja.', 'jan', 'jan.', 'january']\n\n"
    "February: ['f', 'f.', 'fe', 'fe.', 'feb', 'feb.', 'february']\n\n"
    "March: ['mar', 'mar.', 'march']\n\n"
    "April: ['ap', 'ap.', 'apr', 'apr.', 'april']\n\n"
    "May: ['may', 'MAY', 'mAy', 'maY', 'May']\n\n"
    "June: ['jun', 'jun.', 'june']\n\n"
    "July: ['jul', 'jul.', 'july']\n\n"
    "August: ['au', 'au.', 'aug', 'aug.', 'august']\n\n"
    "September: ['s', 's.', 'sep', 'sep.', 'sept', 'sept.', 'september'\n\n"
    "October: ['oc', 'oc.', 'oct', 'oct.', 'october']\n\n"
    "November: ['no', 'no.', 'nov', 'nov.', 'november']\n\n"
    "December: ['d', 'd.', 'de', 'de.', 'dec', 'dec.', 'december']\n\n"
    "All month input is case insensitive, as shown above for May.",
    'Date Settings Tab: Date Input Fields (1 of 3)'),

    ('Treebard date input is unusually free. You can input date parts such as year, month, and day in '
    'any order that they occur to you. You could even input every date in a '
    'different style, but each date will still be displayed according to '
    'your preferred display format. To separate the parts of a date from each other, you can use spaces, slashes, dashes, asterisks, or underscores. So a date input as "bc 3040*f*19/to_1888-01-no_abt" will display something like "from Feb 19, 3040 BC to abt Nov 1, 1888" depending on your display format preferences. This is an absurd example, but the point is that you can stay focused on your genealogy instead of fishing with your mouse for the right month or year on one of those calendar widgets, when most people would rather type a few characters and keep going.\n\n'
    'For example, "March" pops into your head, or "1888". Whatever. '
    'Just type "mar" into the field. The next thing that occurs to you '
    'may be that it\'s an estimated or approximate date, a calculated '
    'date, or even "B.C." Doesn\'t matter, just type "est" or "abt" or '
    '"cal" or "bc" next, in any order.\n\nFor the fourth month, instead of typing "4" you can type "April", "Apr", '
    '"Ap., "Ap," or "ap".  While some countries might display "April 19, 1884" as "19-04-1884", others would display it as "04-19-1884". Treebard is all about sharing trees, so '
    'to avoid ambiguity in international exchange of trees, Treebard doesn\'t allow months to be displayed as numbers. Then to avoid confusion and bloated code, Treebard doesn\'t allow months to be input as numbers either. Most users will appreciate the simplicity of this approach, since typing "d" for "December" is easier than typing "12" anyway. To make it even easier, all month inputs are case insensitive. I you wanted to type "mArCh", that would not be a problem. It will be displayed as "March", "Mar" or "Mar.", depending on your stored preferences.\n\nWhen inputting years with less than four digits, such as the year 33 AD, add preceding zeroes, i.e. "0033". '
    'If you forget, Treebard will ask for clarification on a date like 10 mar 19 '
    'wherein either 10 or 19 could be the year. Other than that--and because '
    'you can\'t type "12" for December--this date input system is almost '
    'completely free of extra dialogs other than error messages. There are messages when you make an obvious mistake, because Treebard doesn\'t allow bad dates to be entered into a database.\n\n'
    'For an estimated date, type any of the abbreviations for "estimated" that Treebard will let you select as a display preference, that is, anything in this list: "est, est. est\'d" For a list of all allowed abbreviations, '
    'see post 1 of 3 in this series. For a '
    'calculated date, type "cal", etc. To display a date like '
    '"Before 1824", just type "1824 bef" or "bef 1824", either way. For '
    '"after 1242 B.C." you could type "bc 1242 aft" with the parts in ' 
    'any order and Treebard will display the date the way you want it '
    'displayed, for example "aft. 1242 BCE" if that\'s how you\'ve set your '
    'preferences.\n\n'
    'There are two kinds of compound date: range and span. A range refers to a range of time '
    'between two dates, such as "between 19 Sep 1899 and Aug 1902". To enter a range, enter the two dates any way you want with the word '
    '"and" between them. If you enter "1885 and 19 bc", Treebard will '
    'display "Between 19 BC and 1885 AD" in whatever display format you\'ve '
    'chosen. A span is used when something is known to have occurred throughout that time span such '
    'as a career "from 1920 to 1945". To enter a span, input two dates '
    'with the word "to" between them.\n\n', 
    'Date Settings Tab: Date Input Fields (2 of 3)'),

    ('In order to make Treebard trees truly portable and sharable, '
    'display styles for dates are limited to styles which are '
    'unambiguous to anyone including plain folks like me with little education. For example, my personal favorite way to display dates is the ISO format (1200-12-14 for December 14, 1200), but this format might be unfamiliar to some users so I dropped it.\n\n'
    'Treebard has no option for displaying bad dates, in fact '
    'Treebard refuses to store them. For example, "March 10" is a '
    'bad date because there is no year. In case you have a hint '
    'like that, notes or the Particulars column of the Events Table are a good place to store them. In '
    'this way, every stored date can be used in calculations such '
    'as subtracting one date from another to find out how old someone '
    'was when something happened.\n\nTreebard deletes bad date input '
    'and tells you why, so you can retype the date the right way.', 
    'Date Settings Tab: Date Input Fields (3 of 3)'),

    ('Ten different choices can be made in regards to how you want '
    'Treebard to display dates. Display style has nothing to do '
    'with how a date is entered. By making choices in the bottom '
    'part of the Date Preferences tab and then inputting sample data in '
    'the three input fields at the top of the Date Preferences tab, '
    'you can sample how dates of different types will be displayed without affecting the data in your tree.', 
    'Date Settings Tab: Date Display Preferences'),

    ('Treebard has its own defaults which you can use by ignoring '
    'the options on the Date Display Preferences tab. You can '
    'change options at any time '
    'or revert to Treebard\'s defaults if you want. Changes will '
    'be reflected in how dates display next time you reload the '
    'program. Changing date display styles does not affect your tree '
    'in any way since all dates are stored in a single consistent '
    'format to make the program work more efficiently. The display format '
    'you choose will apply to all your trees application-wide.', 
    'Date Settings Tab: Date Display Preferences'),

    ('While you can enter dates in any way you like, Treebard only '
    'allows dates to display in ways that are unambiguous. In this '
    'way, users can share their trees with confidence that their '
    'dates will not be misread by people from other parts of the '
    'world.\n\nThe only way Treebard will display dates is using spelled-out '
    'or partially spelled-out months such as "Jan", "Jan." or '
    '"January". If '
    'display like "10-1-1888" were allowed, in some countries this '
    'would be interpreted as Oct. 1, 1888 while in other countries '
    'it would mean Jan. 10, 1888. We originally planned to allow dates to be entered this way, but in an attempt to keep Treebard code simple and free of bloat, that functionality was removed.', 
    'Date Settings Tab: General Date Display'),

    ('Estimated and approximated dates could be used in distinct ways. '
    'What follows is Treebard\'s suggestion on how this could be done.\n\n'
    'Sometimes the user wants to enter a date when he doesn\'t have '
    'one, for example to get an event to appear in the right order in '
    'the events table. (In Treebard, an undated event is treated as an attribute and won\'t appear in the events table at all.) Suppose a source states that someone '
    'attended school through '
    'the 5th grade. We can guess that his school career ended around '
    'age 11 and enter a guess in place of a known date that we don\'t '
    'have. Making a distinction between estimated dates and '
    'approximate dates can mark the date as a pure guess (estimated) '
    'or a sourced guess (approximate). So in this case, the date '
    'arrived at for the end of his schooling should be an approximate '
    'date--not estimated--because a source document such as census states '
    'that the person quit school after grade 5. It\'s not quite a guess, '
    'because there\'s a source: the census. But it\'s still a guess, because he could have graduated grade 5 at the age of 14 or whatever.\n\nHowever, in the case where '
    'a date is desired but there is no source other than possibly '
    'common sense, an estimated date could be used. For example, we '
    'might normally assume, even with no source, that a woman got '
    'married sometime after the age of 13. The range "btwn est 1883 '
    'and est 1893" would indicate that the date was just a guess, while '
    'causing the marriage event to fall reasonably close to where '
    'it belongs within the events table.', 
    'Date Settings Tab: Estimated Date Prefix'),

    ('In Treebard\'s opinion, the difference between estimated dates '
    'and approximate dates is that estimated dates have no source; '
    'they\'re just a reasonable '
    'guess by the researcher based on the facts of life. On the other '
    'hand, an approximate date should have some sort of source to back '
    'it up.', 
    'Date Settings Tab: Approximate Date Prefix'),

    ('Calculated dates are not literally from a source but are '
    'calculated from data that is from a source, such as an age or '
    'another date listed on a source document.\n\nYou can use ' 
    'Treebard\'s Date Calculator (in the Tools menu) to subtract one date from another. '
    'This will give you an exact number of years, months and days '
    'to enter in an age field. Or if you have an age of any '
    'precision, the Date Calculator will give you a date of '
    'matching precision.', 
    'Date Settings Tab: Calculated Date Prefix'),

    ('Type the prefix "bef" or "aft" in a date field to indicate '
    'that you don\'t know the exact date when an event took place, '
    'but that evidence shows it must have taken place before or after '
    'some specific date. For example, if a census states that Mary '
    'was a widow in 1880, it can be deduced that her husband might '
    'have died "bef 1880". This is not proof, but her 1880 census '
    'can be used as evidence for the husband\'s "bef 1880" death date. '
    'In reality, she could be a single mother or her husband could be '
    'on vacation or practicing for divorce, so "before/after" dates '
    'help us mark the difference between evidenced dates and '
    'proven ones.', 
    'Date Settings Tab: Before/After Date Prefix'),

    ('Back in the stone ages when only the Christian religion existed, '
    'everyone was equally comfortable separating the major epochs of '
    'recorded history at the year when Jesus was thought to have been '
    'born. In modern times, "AD" for "Anno Domini" and "BC" for '
    '"before Christ" might not be everyone\'s cup of tea. They are '
    'not Treebard\'s defaults. \n\nIn '
    'practice, you should never have to type "ad" as you normally '
    'wouldn\'t want it displayed. Treebard adds it to years prior to '
    '1000 AD since we\'re used to seeing 4-digit dates. And if one '
    'date in a compound date is BC but the other is AD, Treebard will '
    'add the AD to '
    'the right date if you don\'t. Treebard always assumes that any '
    'date not marked "bc" is AD.\n\nFor the sake of honoring diverse '
    'religious traditions and political correctness, Treebard\'s '
    'default epoch markers are "CE" for "current era" and "BCE" '
    'for "before current era". The dividing line is still the same: '
    'the year that the Christian religion traditionally holds as the '
    'birth year of Jesus.', 
    'Date Settings Tab: Epoch Date Suffix'),

    ('Some programs display dual dates such as "1751/1752" to '
    'indicate that an event took place while the transition '
    'was going on from the Julian Calendar to the Gregorian '
    'calendar. Unfortunately, every country adopted the '
    'Gregorian calendar in a different year. So it would '
    'take a lot of stored per-country data for a computer '
    'program to know what span of time to display dual dates '
    'in, depending on what country the event took place in. '
    'And if my research was wrong or incomplete, I would be building '
    'mistaken data into Treebard. '
    'And then this data would rarely be used, and more rarely '
    'appreciated. And some countries have only recently made the '
    'transition.\n\nInstead of pretending that all events took '
    'place in the USA and then using the transition period '
    'pertinent to the USA, Treebard would like to avoid '
    'displaying ugly dual dates altogether. If you know '
    'you\'re entering a date that falls within a calendar '
    'transition period, just mark the input "ns" for new style date '
    '(Gregorian calendar) or "os" for old style date (Julian '
    'calendar).\n\nIn Treebard\'s opinion, most uneducated '
    'people in the olden days didn\'t know for sure when they ' 
    'were born or exactly how old they were. And in the olden days, '
    'most people couldn\'t read or write. This makes us wonder what good '
    'it does to use fastidiously precise date strictures for '
    'dates that are obviously imprecise if not downright sloppy maybe '
    '75% of the time, except for the royal families who could afford '
    'a scribe to follow them around and record the exact date of '
    'their every move.', 
    'Date Settings Tab: Julian/Gregorian Date Suffix'),

    ('A span is a compound date such as "from July 1845 to Jan. 1850" '
    'which denotes a specific known period of time. Enter date spans '
    'with the word "to" between the two dates. Example: input such as "4 19 1888 to 3-20-1887" '
    'will display as "from March 20, 1887 to April 19, 1888" in '
    'whatever format you\'ve selected for date display.', 
    'Date Settings Tab: Span Compound Date'),

    ('A range is a compound date such as "between July 1845 and Jan. '
    '1850" which denotes a known period of time during which an event '
    'took place, when the exact date of the event is not known. Enter '
    'date ranges with the word "and" between the two dates. Example: input such as "4 19 1888 '
    'and 3-20-1887" will display as "between March 20, 1887 and April '
    '19, 1888" in whatever format you\'ve selected for date display.', 
    'Date Settings Tab: Range Compound Date'),

    ('When you\'ve selected one or more date display format changes, '
    'click the SUBMIT '
    'button to store the changes. Changes made to your '
    'date format settings have no effect on Treebard defaults, '
    'which can be reverted to at '
    'any time. You can change formats as often as you like. Changes '
    'take effect next time you restart the program. Display formats '
    'have nothing to do with how dates are entered or how they are '
    'stored, so you don\'t need to consider anything except how you '
    'want dates to look when displayed.', 
    'Date Settings Tab: SUBMIT Button'),

    ('To return to Treebard\'s out-of-the-box default date display '
    'settings, click the REVERT button. Date display settings ' 
    'specific to your currently open tree will be deleted forever '
    'But the dates will be unaffected. ' 
    'Date display settings for all your trees will change accordingly. ', 
    'Date Settings Tab: REVERT Button'))

# rcm_widgets = (
    # self.note_header, self.note.text, self.toc_head, self.linker, radframe, 
    # self.order)
notes_dlg_help_msg = (
    ('Type the name of a topic i.e. title for this note. For example, if the event was a wedding, there could be notes with topics such as "Uncle Buck--Incident at Reception", "Change of Venue at Last Minute" and "Ringbearer Got Lost"', 
    'Notes Dialog: Note Topic'),
    ("Type or paste text of any length. The Particulars column in the events table can hold one short note, whereas this notes field can be used for any amount of detail. On the Events Table, in the row pertaining to a given event, the button in the Notes column will read '...' if any notes exist for that event. Clicking a blank button will open the Notes Dialog so the first note can be created. There's no SUBMIT button in the dialog since all changes made are saved automatically as soon as they're made.", 
    "Notes Dialog: Note Input"),
    ("All notes need a topic which is unique throughout the current tree. This is part of the feature which allows any note to be linked to more than one entity so that copy/pasting and duplicate storing of notes is unnecessary. The left panel is a table of contents listing note topics linked to this event or other element. Clicking a topic in the left panel of the notes dialog opens that note for reading or editing.",
    "Notes Dialog: Table of Contents"),
    ("Each note can be linked to any number of elements. If you open the Note Dialog by clicking a button in the Notes row of the Events Table, the notes you create in that dialog will be automatically linked to the event corresponding to the row that the Note button was in. The LINK TO... button in the Notes Dialog opens a dialog wherein you can link the current note to any other element in the tree, such as a person, place, citation, image, to-do item, chart, report, etc.",
    "Notes Dialog: Link Current Note to Other Elements"),
    ("All notes in Treebard are shared by default when you share your tree. But if you click the Private radio button, the current note will be forever unsharable until you remove this restriction by clicking the Public radiobutton. Changes take effect immediately.",
    "Notes Dialog: Select Public or Private"),
    ("Topics within the Table of Contents can be reordered in the dialog that opens when you click this button. To traverse the topics in the dialog without changing their order, use the Tab key to move forward or Shift+Tab to move backward. When the topic you want to change is in focus, use the Arrow keys to move the topic up or down in the Table of Contents.",
    "Notes Dialog: Re-Order Table of Contents"),
)

# rcm_widgets = (self.name_input, self.name_type_input.entry, 
        # self.gender_input.entry, self.image_input.entry, 
        # autosort, self.order_frm)
person_add_help_msg = (
    ("If you came to this dialog by way of an input where you've already entered the name of a person that is new to the tree, the name you entered will have already filled into the input field automatically. Otherwise, you can enter any name you want into the field if it's blank or change what was auto-filled. This is the full name as seen in your source, complete with the correct capitalization and spelling, the way you want to see it stored and displayed. Please do not use ALL CAPS unless the name is correctly written that way in real life. This is a device left over from the days of the typewriter, when methods for differentiating among data were extremely limited. That being said, Treebard will not try to stop you, but if you enter a surname with ALL CAPS, it will be displayed that way everywhere.", 
    'New Person Dialog: Full Name Input'),
    ("Treebard classifies all names by type. You should try to provide a birth name if you have one, but if a name is not actually the person's birth name, you should select the right type here. The birth name is what will be displayed on the Person Tab, but if there's no birth name entered, Treebard will try to use the next best thing if any other name type has been entered, and will denote the name by type so it will not be mistaken for a birth name. The autofill entry at the top of the program for changing the current person's name accepts any name that has been stored in the database, including nicknames, identification numbers etc. Please consider not using words such as 'unknown' when a name is not known. It's better to use some sort of punctuation such as '_________' or '?', and you can experiment with leaving part of a name blank since Treebard will think 'unknown' is a person's name and behave accordingly.\n\nUnlike other software, Treebard does not provide fields for First Name, Middle Name, and Last Name. These categories don't apply to all cases, even in the countries where this basic scheme is typically used. Some people have two or more 'middle names'. Then there are countries such as Iceland and China where the typical scheme used in the USA is completely irrelevant. It's correct to input the full name as a full name, in the order in which it is normally displayed. Don't put the surname first unless the person lived in a country where surnames are written first. As for how a name will be alphabetized, see the AUTOSORT button for that.\n\nAnother reason Treebard doesn't try to track First, Middle and Last names is that it makes the code impossible to write, due to the vast abundance of cases where this scheme does not apply. Treebard likes its code to be as slim and efficient as possible.", 
    'New Person Dialog: Name Type Input'),
    ("Treebard is not in the political correctness business, but we do recognize that others will have certain preferences, and we have no argument with that. Unfortunately, any attempt to please everybody in these tumultuous times of gender flexibility will lead only to embarrassment for all concerned. So we have settled on the following policy.\n\nChildren have a female mother and a male father. The parents are never assumed to be married. Anyone of any gender can adopt a child with a partner of any gender, or marry anyone of any gender. Treebard performs no code logic based on gender except to decide who the biological parents of a child are. We will provide the following gender categories: female, male, unknown, and other. Persons input without a gender designation will be designated 'unknown' gender by default.", 
    'New Person Dialog: Gender Input'),
    ("Each person should have a main image. If there's only one image provided, it will automatically be designated the main image. Treebard suggests that each person in a tree could be provided with a vintage photo of a place where that person lived, if there are no photos of the person available. Old photos of every place in the world are available online. Otherwise, Treebard has old drawings and photos of vintage cameras which are used by default if you don't provide an image for a person. You can actually select which one of these default images to use, if you like them, or you can provide your own default images and use them, or you can elect to use no image when none is available. The main image is the one that shows in a tabbed widget on the top right side of the Person Tab. If no image is available, the Do List Tab will automatically be shown, but if any image is available including one of Treebard's default images, the Images Tab will be shown by default.", 
    'New Person Dialog: Main Image Input'),
    ("The right way to alphabetize some names varies from culture to culture. For example, a surname like 'van Dyke' will be alphabetized by 'V' in the Netherlands but by 'D' in the USA. Most genealogy software ignores this sort of distinction.\n\nTreebard uniquely recognizes the need for a feature whereby the tree author can tell the program exactly how to alphabetize a name. Instead of pretending that the whole world follows the typical western tradition of First, Middle, Last Name, Treebard lets you enter a Full Name as a single string of characters, in the order that the name parts are normally used. But when it comes to how the name should be alphabetized, Treebard can only guess using the typical western format. This order (last, first, middle) will automatically fill into the Name Ordering widgets to the right of the AUTOSORT button. If you change the contents of the Full Name input, you can click the AUTOSORT button to change what's shown in the sorting area. If the right order is shown, just Tab on to the OK button. Otherwise, refer to the context help topic for the sorting area.", 
    'New Person Dialog: AUTOSORT button'),
    ("If the Name Ordering widgets don't display the correct order for alphabetizing a name, the ordering area can be entered using the Arrow keys when either the AUTOSORT or OK button is in focus. Once focus is in the ordering area, use Tab to move forward without changing order or Shift+Tab to move backward. To change the order of a name part, when the name part is in focus, use the Arrow keys.", 
    'New Person Dialog: Name Ordering'))

# rcm_widgets = (
    # self.person_entry, person_change, person_search, 
    # self.top_pic_button, self.findings_table.event_input, 
    # self.findings_table.add_event_button, self.att.event_input, 
    # self.att.add_event_button, self.fontpicker.output_sample, 
    # self.fontpicker.font_size, self.fontpicker.cbo.entry, 
    # self.fontpicker.apply_button, colorizer.hscroll, 
    # colorizer.try_button, colorizer.copy_button, 
    # colorizer.apply_button, colorizer.new_button, 
    # colorizer.entries_combos[0], colorizer.entries_combos[1], 
    # colorizer.entries_combos[2], colorizer.entries_combos[3], 
    # colorizer.domain_tips[0], colorizer.domain_tips[1], 
    # colorizer.domain_tips[2], colorizer.domain_tips[3], 
    # self.findings_table.headers[0], self.findings_table.headers[1], 
    # self.findings_table.headers[2], self.findings_table.headers[3], 
    # self.findings_table.headers[4], self.findings_table.headers[5], 
    # self.findings_table.headers[6], self.findings_table.headers[7], 
    # self.att.headers[0], self.att.headers[1], self.att.headers[2], 
    # self.att.headers[3], self.att.headers[4], self.att.headers[5], 
    # self.att.headers[6], self.att.headers[7])
	
main_help_msg = (
    ("lorem ipsum",
        "Person Tab: Change Current Person Name Input"),
    ("lorem ipsum",
        "Person Tab: Change Current Person OK Button"),
    ("lorem ipsum",
        "Person Tab: Person Search Button"),
    ("lorem ipsum",
        "Person Tab: Current Person Main Image"),
    ("lorem ipsum",
        "Person Tab: New Event or Attribute Input"),
    ("lorem ipsum",
        "Person Tab: New Event or Attribute OK Button"),
    ("lorem ipsum",
        "Person Tab: New Event or Attribute Input"),
    ("lorem ipsum",
        "Person Tab: New Event or Attribute OK Button"),
    ("lorem ipsum",
        "Font Preferences Tab: Sample Output"),
    ("lorem ipsum",
        "Font Preferences Tab: Font Size Input"),
    ("lorem ipsum",
        "Font Preferences Tab: Font Family Input"),
    ("lorem ipsum",
        "Font Preferences Tab: APPLY Button"),
    ("lorem ipsumddd",
        "Color Scheme Tab: New Color Scheme Area"),
    ("lorem ipsum",
        "Color Scheme Tab: TRY Button"),
    ("lorem ipsum",
        "Color Scheme Tab: COPY Button"),
    ("lorem ipsum",
        "Color Scheme Tab: APPLY Button"),
    ("lorem ipsum",
        "Color Scheme Tab: New Color Scheme Button"),
    ("lorem ipsum",
        "Color Scheme Tab: Background Color 1 Input"),
    ("lorem ipsum",
        "Color Scheme Tab: Background Color 2 Input"),
    ("lorem ipsum",
        "Color Scheme Tab: Background Color 3 Input"),
    ("lorem ipsum",
        "Color Scheme Tab: Font Color Input"),
    ("lorem ipsum1",
        "Color Scheme Tab: Background Color 1 Domain"),
    ("lorem ipsum2",
        "Color Scheme Tab: Background Color 2 Domain"),
    ("lorem ipsum3",
        "Color Scheme Tab: Background Color 3 Domain"),
    ("lorem ipsum4",
        "Color Scheme Tab: Font Color Domain"),
    ("lorem ipsum",
        "Events Table: Event Type Column"),
    ("lorem ipsum",
        "Events Table: Date Column"),
    ("lorem ipsum",
        "Events Table: Place Column"),
    ("lorem ipsum",
        "Events Table: Particulars Column"),
    ("lorem ipsum",
        "Events Table: Age Column"),
    ("lorem ipsum",
        "Events Table: Roles Column"),
    ("lorem ipsum",
        "Events Table: Notes Column"),
    ("lorem ipsum",
        "Events Table: Sources Column"),
    ("lorem ipsum",
        "Attributes Table: Event Type Column"),
    ("lorem ipsum",
        "Attributes Table: Date Column"),
    ("lorem ipsum",
        "Attributes Table: Place Column"),
    ("lorem ipsum",
        "Attributes Table: Particulars Column"),
    ("lorem ipsum",
        "Attributes Table: Age Column"),
    ("lorem ipsum",
        "Attributes Table: Roles Column"),
    ("lorem ipsum",
        "Attributes Table: Notes Column"),
    ("lorem ipsum",
        "Attributes Table: Sources Column"),

)

# rcm_widgets = (
    # self.role_type_input, self.person_input, self.add_butt, 
    # self.done_butt, self.close_butt, self.role_type_input.entry)
roles_dlg_help_msg = (
    ('Type or select the role type for a new role. A role type can be anything you want. For example, at a wedding event there\'s a bride and groom who are primary participants in the event. Don\'t input them here. But many other roles exist such as bible bearer, ring bearer, flower girl, best man, religious official, usher, witness, candle-lighter, photographer or anything you want. In a document describing an event, many names might be mentioned that you might want to research further, or record in case they end up being related to the family or the family\'s story in some way. Role types can\'t be blank, but you can select \'other\' or \'unknown\'. For example, a group photo from a wedding has names listed on the back, but you don\'t know who some of the people are. Just input the names and select \'unknown\' role type. They\'ll be added to the database same as anyone else, so if the name pops up again, you won\'t have to go searching for it in notes. Built-in role types can\'t be deleted but they can be hidden in the Types Settings Tab in Preferences. Custom role types can be deleted or hidden.', 'New Role: Role Type Input'),

    ('For a role you don\'t always know the names of the people involved, but maybe you want to research it. You can enter roles with no names, or known names with \'other\' or \'unknown\' selected as the role type. You can create new people here. If you add a role with a new person, a dialog will open so you can specify the new person\'s name type such as birth name or nickname; gender if known; image if any; and preferred sort order for alphabetization. If you input a name that already exists in the database, another dialog will ask whether you intended to create a new person by the same name. This will help prevent duplicate persons which would have to be merged later if not caught when trying to input them. You can input as many John Smiths as you want, since each person entered has a unique ID in the database. Later if you find that two persons in the database are really the same person, the two can be merged so that your work doesn\'t have to be done over. If you know the name of someone who participated in an event but you don\'t know what role they played, you can still input the name and select \'other\' or \'unknown\' as the role type.', 'New Role: Person Input'),

    ('Use the ADD button to add a role if you\'ll be adding more than one role, so the dialog doesn\'t close. The new roles will instantly be added to the roles table and you\'ll be able to edit or delete them at any time.', 
    'ADD Button'),

    ('Use the DONE button to close the roles dialog if you\'re only going to create one new role. If nothing is in the inputs, the dialog will close harmlessly.', 
    'DONE Button'),

    ('Use the CLOSE button to close the roles dialog if you\'re not adding any more new roles. Even if you\'ve typed all or part of a new role, what you typed will be ignored. Roles you already entered will not be affected. They can be deleted or edited with the EDIT buttons in the roles table rows.', 
    'CLOSE Button'),

    ("Lorem ipsum",
    "Role Type Input"))

# rcm_widgets = (self.search_input, self.search_dlg_heading, self.search_table)
search_person_help_msg = (
    ('This person search tool is especially helpful if you know only '
    'part of the name you\'re looking for. Also, if there\'s more than '
    'one person with an identical name, the other way to select a '
    'person--the autofill person select field--won\'t work for '
    'duplicate names unless you know the ID. This search dialog '
    'will help you '
    'differentiate among several people with similar names by '
    'showing birth and death dates and parent names for each '
    'person. Just type any part of any name, ID number, nickname, '
    'a.k.a., etc. and the search table will fill with matching '
    'names. Tab out of the input field to the table and navigate '
    'up and down using the Tab or Ctrl+Tab keys or the Up/Down arrow ' 
    'keys. You can select a new current person but you don\'t have '
    'to. The search tool is also an easy way to look up a name '
    'or ID number you need.', 
    'Person Search Input'),

    ('After tabbing into the search results table, you can '
    'navigate up and down the table with Tab or Ctrl+Tab keys, or '
    'Up/Down arrow keys. To choose a new current person, press '
    'Enter or Spacebar when the person you want is highlighted, '
    'or double-click any row whether it\'s highlighted or not. '
    'The table can be sorted '
    'ascendingly or descendingly by single clicks of the column '
    'heads. If you typed "lou" and '
    '"Fred Jenkins" pops up, what\'s going on? Point at the name '
    'and a nametip will pop up giving the needed information: '
    '"Nickname: Louie", along with any other names, ID numbers, '
    'nicknames, pseudonyms, married names, mis-spellings, and any '
    'other name information you\'ve entered for Fred Jenkins. ', 
    'Person Search Table'), 

    ("lorem ipsum", "title")
)

# rcm_widgets = (
    # self.date_input, self.place_input, self.particulars_input, 
    # self.age1_input)
new_event_dlg_help_msg = (
    ("lorem ipsum",
        "New Event Dialog: Date Input"),
    ("lorem ipsum",
        "New Event Dialog: Place Input"),
    ("lorem ipsum",
        "New Event Dialog: Particulars Input"),
    ("lorem ipsum",
        "New Event Dialog: Age Input")
)

# rcm_widgets = (
    # self.radios["parent"], self.radios["sibling"], 
    # self.radios["partner"], self.radios["child"])
new_kin_type_dlg_help_msg = (
    ("lorem ipsum",
        "New Kin Type Dialog: Parent Select"),
    ("lorem ipsum",
        "New Kin Type Dialog: Sibling Select"),
    ("lorem ipsum",
        "New Kin Type Dialog: Partner Select"),
    ("lorem ipsum",
        "New Kin Type Dialog: Child Select")
)

# rcm_widgets = (
    # self.thumbstrip, self.pic_canvas, self.prevbutt, self.nextbutt, 
    # self.b1)
gallery_help_msg = (    
    ("lorem ipsum",
        "Image Gallery: Thumbnails Strip"),
    ("lorem ipsum",
        "Image Gallery: Viewport"),
    ("lorem ipsum",
        "Image Gallery: PREVIOUS Button"),
    ("lorem ipsum",
        "Image Gallery: NEXT Button"),
    ("lorem ipsum",
        "Image Gallery: EDIT Button")
)

# rcm_widgets = (opener, new, importgedcom, opensample, cancel, self.picbutton)
opening_dlg_help_msg = (
    ("lorem ipsum",
        "Opening Dialog: OPEN TREE Button"),
    ("lorem ipsum",
        "Opening Dialog: NEW TREE Button"),
    ("lorem ipsum",
        "Opening Dialog: IMPORT GEDCOM Button"),
    ("lorem ipsum",
        "Opening Dialog: OPEN SAMPLE TREE Button"),
    ("lorem ipsum",
        "Opening Dialog: CANCEL Button"),
    ("lorem ipsum",
        "Opening Dialog: OPEN PRIOR TREE Button")
)

# rcm_widgets = (lab, rad, editx)
places_dlg_help_msg = (
    ("lorem ipsum",
        "New Place Dialog: Place Name Output"),
    ("lorem ipsum",
        "New Place Dialog: Place Name Select"),
    ("lorem ipsum",
        "New Place Dialog: Duplicate Place Name Hint EDIT Button")
)

# rcm_widgets = ()
links_dlg_msg = ()






























# Messages used generically by all the widgets made in a loop.
#   This has only been used in one place but could be extended.

# roles dialog editx buttons
role_edit_help_msg = (
        'Clicking the Edit button will open a row of edit inputs. '
        'You can use them to delete a role or to change the role '
        'type or role person for the row you clicked. You can also '
        'create a new role type--anything you want--or a new person. '
        'If you input a new person, a dialog will open so you can '
        'select gender, sort order for alphabetization, image, and '
        'name type. The person in a role can be blank. For example, '
        'in a "rescue" event type, Aunt Maude\'s life was saved by '
        'a passing tourist. To add an anonymous or unknown role '
        'person, just leave the person field blank. Role types '
        'cannot be blank, but you can select \'other\' or \'unknown\' '
        'from the dropdown list. Built-in role types can\'t be deleted, '
        'but they can be hidden in the Types Settings tab in Preferences. '
        'Custom role types can be deleted or hidden unless they\'re '
        'being used in the tree.', 
        'Edit Existing Role Button')





    
    

    

