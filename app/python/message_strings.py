# message_strings.py (import as ms)

from widgets import LabelH3
import dev_tools as dt

'''
    This module is used to store strings used as messages 
    in right-click context help menus.
'''

# Custom messages used in one place:

# rcm_widgets = ( # in DatePrefsWidgets class in root module
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
dates_prefs_msg = (
    ('The Date Entry Demo section at the top of the Date Preferences '
    'tab allows you to test various ways of inputting and displaying '
    'dates. Nothing you enter here will affect your tree, but the '
    'three input fields are exact working models of every date input '
    'field in Treebard.\n\n'
    'For more info, right-click for context help in each of the three '
    'input fields.', 
    'Date Entry Demo'),

    ('Treebard date input is extremely free. You can input date parts in '
    'any order that they occur to you. You can input every date in a '
    'different style but each date will still be displayed according to '
    'your preferred display format.\n\n'
    'For example, "March" pops into your head, or "1888". Whatever. '
    'Just type it into the field. The next thing that occurs to you '
    'may be that it\'s an estimated or approximate date, a calculated '
    'date, or even B.C. Doesn\'t matter, just type "est" or "abt" or '
    '"cal" or "bc" next, in any order. You can type "April", "Apr", '
    '"Ap., "Ap," "ap", or even "apricot" if you want. As long as it '
    'starts with "ap", Treebard will know it\'s April and not August. '
    'If you prefer you can type "4" or "04". Treebard doesn\'t care.\n\n'
    'While date style entry and order is extremely free, abbreviation '
    'style for date prefixes and suffixes is limited to what\'s easiest '
    'to remember: type the simplest, lower-case version of the suffix '
    'or prefix, like this: for an estimated date, type "est". For a '
    'calculated date, type "cal", etc. To display a date like '
    '"Before 1824", just type "1824 bef" or "bef 1824", either way. For '
    '"after 1242 B.C." you could type "bc 1242 aft" with the parts in ' 
    'any order and Treebard will display the date the way you want it '
    'displayed.\n\n'
    'To enter a range--a compound date referring to a range of time '
    'between two dates--enter two dates any way you want with the word '
    '"and" between them. If you enter "1885 and 19 bc", Treebard will '
    'display "Between 19 BC and 1885 AD" in whatever display format you '
    'choose. A span is a compound date that refers to an event or '
    'attribute known to have occurred throughout that time span such '
    'as a career "from 1920 to 1945". To enter a span, input two dates '
    'with the word "to" between them. If you don\'t know one of the '
    'dates, enter a question mark in place of that date. If you '
    'don\'t know either of the dates, sorry!', 
    'Date Input Fields (1 of 3)'),

    ('If you input a date such as "10 1 1888" that could be either '
    'Oct 1 1888 or Jan 10 1888, Treebard will open a dialog so you '
    'can clarify which date part is month and which is year. For '
    'example, if you input "1 2 3 bc", Treebard will ask which is '
    'year, which is month, and which is day. This dialog is filled '
    'out for you to the extent that Treebard is able to figure it '
    'out and you can fill in the rest. In order to see this dialog '
    'less often, enter months as "ja, f, mar, ap, may, jun, jul, au, '
    's, oc, no, d" instead of using numbers. If you input years that '
    'have fewer than four digits, add preceding zeroes, for example: '
    '"0034" for 34 AD instead of "34". Another trick is to add a comma '
    'after the number that represents the day, as in "June 12, 1902". ' 
    'Except that you can also type "12, jun 1902" and Treebard will have '
    'no problem with that either. So you could type "4, 4 0004" and '
    'Treebard won\'t have to ask for clarification.\n\nThere\'s one '
    'restriction you should know about. Most people will want to use '
    'spaces to separate date parts as in "feb 14 1818". This is the '
    'easiest way to do it. But if you want, instead of using spaces '
    'to separate date parts, you can use dots (.), '
    'asterisks (*), forward slashes (/), or dashes (-) as '
    'separators. The restriction is that if you add a suffix and/or '
    'prefix, you have to type it like this: "bc-f-14-1818-est" with '
    'only one consistent separator. Not like this: "bc f-14-1818 est". '
    'Whatever separator you use in any given date entry, use it '
    'throughout the whole input.\n\nHowever there is an exception '
    'to the restriction on separators. When typing a compound date '
    'with the two dates separated by "and" or "to", only spaces can '
    'separate the "and" or "to" from the dates on either side.\n\n'
    'The nine dropdown selectors on the Date Preferences tab give '
    'you the ability to decide how all your dates will look. '
    'For example, you can see "est" displayed in front of an '
    'estimated date or you can see "est\'d", etc. These preferences '
    'will be covered further down in this tutorial. The way you input '
    'a date has nothing to do with how it will be displayed.', 
    'Date Input Fields (2 of 3)'),

    ('In order to make Treebard trees truly portable and sharable, '
    'display styles for dates are limited to styles which are '
    'unambiguous, although you can enter a date any way you want. '
    'Treebard has no option for displaying bad dates, in fact '
    'Treebard refuses to store them. For example, "March 10" is a '
    'bad date because there is no year. In case you have a hint '
    'like that, note fields are the right place to store them. In '
    'this way, every stored date can be used in calculations such '
    'as subtracting one date from another to find out how old someone '
    'was when something happened.\n\nTreebard deletes bad date input '
    'and tells you why so you can retype the date the right way.', 
    'Date Input Fields (3 of 3)'),

    ('Ten different choices can be made in regards to how you want '
    'Treebard to display dates. Display style has nothing to do '
    'with how a date is entered. By making choices in the bottom '
    'part of the Date Preferences tab and then inputting sample data in '
    'the three input fields at the top of the Date Preferences tab, '
    'you can see how dates of different types will be displayed.', 
    'Date Display Preferences'),

    ('Treebard has its own defaults which you can use by ignoring '
    'the options on the Date Display Preferences tab. You can '
    'change options at any time '
    'or revert to Treebard\'s defaults if you want. Changes will '
    'be reflected in how dates display next time you reload the '
    'program. Changing date display styles does not affect your tree '
    'in any way since all dates are stored in a single consistent '
    'format to make the program work more efficiently.\n\nThe two '
    'radio buttons labeled "This Tree" and '
    '"All Trees" let you set your own defaults individually for '
    'the current tree or set defaults that will apply to all your '
    'trees. Once you set defaults that apply to all your trees, you '
    'can still change date display settings for any single tree '
    'by opening that tree and using this tool with "This Tree" '
    'checked.\n\nTreebard\'s own out-of-the-box defaults never '
    'change so you can always revert to them. Doing so erases '
    'all your previous changes.', 
    'Where Date Display Preferences Apply'),

    ('While you can enter dates in any way you like, Treebard only '
    'allows dates to display in ways that are unambiguous. In this '
    'way, users can share their trees with confidence that their '
    'dates will not be misread by people from other parts of the '
    'world.\n\nThe best way to display dates is using spelled-out '
    'or partially spelled-out months such as "Jan", "Jan." or '
    '"January". If you prefer to use numbers for months, the '
    'so-called ISO format is used, in which larger date parts come '
    'first. For example, "1888-01-10" is always Jan. 10, 1888 and has '
    'no other interpration since the year appears first, followed '
    'by month, then day, in every case.\n\nOn the other hand, if '
    'display like "10-1-1888" were allowed, in some countries this '
    'would be interpreted as Oct. 1, 1888 while in other countries '
    'it would mean Jan. 10, 1888. So you can enter dates that way '
    'if you like, but there is no option to display them that way.', 
    'General Date Display'),

    ('Estimated and approximated dates could be used in distinct ways. '
    'What follows is Treebard\'s suggestion on how this could be done.\n\n'
    'Sometimes the user wants to enter a date when he doesn\'t have '
    'one, for example to get an event to appear in the right order in '
    'the events table. Suppose a source states that someone '
    'attended school through '
    'the 5th grade. We can guess that his school career ended around '
    'age 11 and enter a guess in place of a known date that we don\'t '
    'have. Making a distinction between estimated dates and '
    'approximate dates can mark the date as a pure guess (estimated) '
    'or a sourced guess (approximate). So in this case, the date '
    'arrived at for the end of his schooling should be an approximate '
    'date--not estimated--because a source document such as census states '
    'that the person quit school after grade 5. It\'s not quite a guess, '
    'because there\'s a source: the census.\n\nHowever, in the case where '
    'a date is desired but there is no source other than possibly '
    'common sense, an estimated date would be used. For example, we '
    'might normally assume, even with no source, that a woman got '
    'married sometime after the age of 13. The range "btwn est 1883 '
    'and est 1893" would indicate that the date was just a guess, while '
    'causing the marriage event to fall reasonably close to where '
    'it belongs within the events table.', 
    'Estimated Date Prefix'),

    ('In Treebard\'s opinion, the difference between estimated dates '
    'and approximate dates is that estimated dates have no source; '
    'they\'re just a reasonable '
    'guess by the researcher based on the facts of life. On the other '
    'hand, an approximate date should have some sort of source to back '
    'it up.', 
    'Approximate Date Prefix'),

    ('Calculated dates are not literally from a source but are '
    'calculated from data that is from a source, such as an age or '
    'another date listed on a source document.\n\nYou can use ' 
    'Treebard\'s Date Calculator to subtract one date from another. '
    'This will give you an exact number of years, months and days '
    'to enter in an age field. Or if you have an age of any '
    'precision, the Date Calculator will give you a date of '
    'matching precision.', 
    'Calculated Date Prefix'),

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
    'Before/After Date Prefix'),

    ('Back in the stone ages when only the Christian religion existed, '
    'everyone was equally comfortable separating the major epochs of '
    'recorded history at the year when Jesus was thought to have been '
    'born. In modern times, "AD" for "Anno Domini" and "BC" for '
    '"before Christ" might not be everyone\'s cup of tea. They are '
    'not Treebard\'s defaults. But the easiest input markers to remember '
    'are still "bc" and "ad" so that\'s what we use for input.\n\nIn '
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
    'the year that the Christian church traditionally holds as the '
    'birth year of Jesus.', 
    'Epoch Date Suffix'),

    ('Some programs display dual dates such as "1751/1752" to '
    'indicate that an event took place while the transition '
    'was going on from the Julian Calendar to the Gregorian '
    'calendar. Unfortunately, every country adopted the '
    'Gregorian calendar in a different year. So it would '
    'take a lot of stored per-country data for a computer '
    'program to know what span of time to display dual dates '
    'in, depending on what country the event took place in. '
    'And then this data would rarely be used, and more rarely '
    'appreciated. Some countries have only recently made the '
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
    'most people were uneducated. This makes us wonder what good '
    'it does to use fastidiously precise date strictures for '
    'dates that are obviously imprecise if not downright sloppy maybe '
    '75% of the time, except for the royal families who could afford '
    'a scribe to follow them around and record the exact date of '
    'their every move.', 
    'Julian/Gregorian Date Suffix'),

    ('A span is a compound date such as "from July 1845 to Jan. 1850" '
    'which denotes a specific known period of time. Enter date spans '
    'with the word "to" between the two dates. The word "to" should '
    'have a space on each side of it even if a different separator '
    'such as slash, dash, asterisk or dot is being used within the '
    'dates themselves. Example: input such as "4 19 1888 to 3-20-1887" '
    'will display as "from March 20, 1887 to April 19, 1888" in '
    'whatever format you\'ve selected for date display. If you don\'t '
    'know one of the dates, enter something like "? to 1492" or "1537 '
    'to ?" and Treebard will know what to do.', 
    'Span Compound Date'),

    ('A range is a compound date such as "between July 1845 and Jan. '
    '1850" which denotes a known period of time during which an event '
    'took place, when the exact date of the event is not known. Enter '
    'date ranges with the word "and" between the two dates. The word '
    '"and" should have a space on each side of it even if a different ' 
    'separator such as slash, dash, asterisk or dot is being used '
    'within the dates themselves. Example: input such as "4 19 1888 '
    'and 3-20-1887" will display as "between March 20, 1887 and April '
    '19, 1888" in whatever format you\'ve selected for date display.', 
    'Range Compound Date'),

    ('When you\'ve selected one or more date display format changes '
    'and told Treebard whether the changes should apply to '
    'the currently open tree or to all your trees, click the Submit '
    'button to store the changes. Changes made to only the current '
    'tree have no effect on Treebard defaults or your own '
    'application-wide defaults. Changes made to your '
    'application-wide defaults have no effect on Treebard defaults, '
    'which are still stored untouched and can be reverted to at '
    'any time. You can change formats as often as you like. Changes '
    'take effect next time you restart the program. Display formats '
    'have nothing to do with how dates are entered or how they are '
    'stored so you don\'t need to consider anything except how you '
    'want dates to look when displayed.', 
    'Submit Button'),

    ('To return to Treebard\'s out-of-the-box default date display '
    'settings, click the Revert button. Date display settings ' 
    'specific to your currently open tree will be deleted forever. ' 
    'Date display settings for other trees will not be affected. '
    'For example, in Tree A you can use Treebard\'s default '
    'date display settings; in Trees B and C you can use your '
    'own default date display settings; in Tree D you can use '
    'custom date display formats that apply only to '
    'that tree; and in Tree E you can use a different custom date '
    'display format that only applies to that tree. Changes made '
    'while Tree X is open have no effect on Tree Y unless both are '
    'using your "user-wide" defaults, in which case changes made '
    'to user-wide defaults will have equal effect in both trees.', 
    'Revert Button'))

# rcm_widgets = (self.subtopic_input.ent, self.note_input.text) # in notes.py
note_dlg_msg = (
    ('Type the name of a subtopic i.e. title for this note as a subcategory of this event. For example, if the event was a wedding, there could be notes with subtitles such as "Uncle Buck--Incident at Reception", "Change of Venue at Last Minute" and "Ringbearer Got Lost"', 'Event Note Subtopic'),
    ('Type or paste text of any length. The Particulars column in the events table can hold one very short note, and notes field can be used for more detail. On the events table, in the row pertaining to a given event, the button in the Notes column will read \'...\' if any notes exist for that event. Clicking a blank button will open the notes dialog anyway so the first note(s) can be created. All notes need a subtitle. This is part of the feature which allows any note to be linked to more than one entity so that duplication of notes is not necessary. The left panel is a table of contents listing note subtitles linked to this event or other entity. Clicking a subtitle in the left panel of the notes dialog opens that note for reading or editing. There\'s a dialog you can open to reorder the note subtitles as they appear in the left panel. Above the left panel you can tell a new note where to appear, either above or below the note you\'ve selected in the left panel.', 'Event Note Input'))

# rcm_widgets = (self,) # in pedigree_chart.py
pedigree_person_tab_msg = (
    ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. '
    'Cras ac arcu quis justo maximus ultrices ac dignissim risus. '
    'In vitae facilisis nisl, eu pretium magna. Cras eros lacus, '
    'elementum nec odio vitae, dignissim vulputate diam. '
    'Pellentesque eget nulla semper, rhoncus leo tristique, '
    'hendrerit ligula. Vestibulum feugiat mattis aliquet. Nunc et '
    'diam sed quam aliquam elementum sit amet ac dui. Aliquam '
    'convallis mi nec elit rutrum luctus. Vestibulum sed erat '
    'vitae est faucibus ullamcorper. Curabitur lacinia non arcu '
    'vitae varius.', 
    'title 1'),)

# rcm_widgets = (self.name_input.input, self.name_type_input.input) # in root module
person_add_msg = (
    ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. '
    'Cras ac arcu quis justo maximus ultrices ac dignissim risus. '
    'In vitae facilisis nisl, eu pretium magna. Cras eros lacus, '
    'elementum nec odio vitae, dignissim vulputate diam. '
    'Pellentesque eget nulla semper, rhoncus leo tristique, '
    'hendrerit ligula. Vestibulum feugiat mattis aliquet. Nunc et '
    'diam sed quam aliquam elementum sit amet ac dui. Aliquam '
    'convallis mi nec elit rutrum luctus. Vestibulum sed erat '
    'vitae est faucibus ullamcorper. Curabitur lacinia non arcu '
    'vitae varius.', 
    'title 1'),
    ('Maecenas quis elit eleifend, lobortis turpis at, iaculi ' 
    'odio. Phasellus congue, urna sit amet posuere luctus, '
    'mauris risus tincidunt sapien, vulputate scelerisque '
    'ipsum libero at neque. Nunc accumsan pellentesque nulla, '
    'a ultricies ex convallis sit amet. Etiam ut sollicitudin '
    'felis, sit amet dictum lacus. Mauris sed mattis diam. '
    'Pellentesque eu malesuada ipsum, vitae sagittis nisl. '
    'Morbi a mi vitae nunc varius ullamcorper in ut urna. '
    'Maecenas auctor ultrices orci. Donec facilisis a '
    'tortor pellentesque venenatis. Curabitur pulvinar '
    'bibendum sem, id eleifend lorem sodales nec. Mauris '
    'eget scelerisque libero. Lorem ipsum dolor sit amet, '
    'consectetur adipiscing elit. Integer vel tellus nec '
    'orci finibus ornare. Praesent pellentesque aliquet augue, '
    'nec feugiat augue posuere a.', 
    'title 2'))

# rcm_widgets = (self.top_pic_button,) # in root module
persons_tab_msg = (
    ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. '
    'Cras ac arcu quis justo maximus ultrices ac dignissim risus. '
    'In vitae facilisis nisl, eu pretium magna. Cras eros lacus, '
    'elementum nec odio vitae, dignissim vulputate diam. '
    'Pellentesque eget nulla semper, rhoncus leo tristique, '
    'hendrerit ligula. Vestibulum feugiat mattis aliquet. Nunc et '
    'diam sed quam aliquam elementum sit amet ac dui. Aliquam '
    'convallis mi nec elit rutrum luctus. Vestibulum sed erat '
    'vitae est faucibus ullamcorper. Curabitur lacinia non arcu '
    'vitae varius.', 
    'Main Image for Current Person'),)

# rcm_widgets = (
    # self.role_type_input, self.person_input, self.add_butt, 
    # self.done_butt, self.close_butt) # in root module
role_dlg_msg = (
    ('Type or select the role type for a new role. A role type can be anything you want. For example, at a wedding event there\'s a bride and groom who are primary participants in the event. Don\'t input them here. But many other roles exist such as bible bearer, ring bearer, flower girl, best man, religious official, usher, witness, candle-lighter, photographer or anything you want. In a document describing an event, many names might be mentioned that you might want to research further, or record in case they end up being related to the family or the family\'s story in some way. Role types can\'t be blank, but you can select \'other\' or \'unknown\'. For example, a group photo from a wedding has names listed on the back, but you don\'t know who some of the people are. Just input the names and select \'unknown\' role type. They\'ll be added to the database same as anyone else, so if the name pops up again, you won\'t have to go searching for it in notes. Built-in role types can\'t be deleted but they can be hidden in the Types Settings Tab in Preferences. Custom role types can be deleted or hidden.', 'New Role: Role Type Input'),

    ('For a role you don\'t always know the names of the people involved, but maybe you want to research it. You can enter roles with no names, or known names with \'other\' or \'unknown\' selected as the role type. You can create new people here. If you add a role with a new person, a dialog will open so you can specify the new person\'s name type such as birth name or nickname; gender if known; image if any; and preferred sort order for alphabetization. If you input a name that already exists in the database, another dialog will ask whether you intended to create a new person by the same name. This will help prevent duplicate persons which would have to be merged later if not caught when trying to input them. You can input as many John Smiths as you want, since each person entered has a unique ID in the database. Later if you find that two persons in the database are really the same person, the two can be merged so that your work doesn\'t have to be done over. If you know the name of someone who participated in an event but you don\'t know what role they played, you can still input the name and select \'other\' or \'unknown\' as the role type.', 'New Role: Person Input'),

    ('Use the ADD button to add a role if you\'ll be adding more than one role, so the dialog doesn\'t close. The new roles will instantly be added to the roles table and you\'ll be able to edit or delete them at any time.', 
    'ADD Button'),

    ('Use the DONE button to close the roles dialog if you\'re only going to create one new role. If nothing is in the inputs, the dialog will close harmlessly.', 
    'DONE Button'),

    ('Use the CLOSE button to close the roles dialog if you\'re not adding any more new roles. Even if you\'ve typed all or part of a new role, what you typed will be ignored. Roles you already entered will not be affected. They can be deleted or edited with the EDIT buttons in the roles table rows.', 
    'CLOSE Button'))

# rcm_widgets = (self.search_input.ent, self.search_dlg_heading) # Search class in root module
search_person_msg = (
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
    'Person Search Table'))

# Messages used generically by all the widgets made in a loop:

# roles dialog editx buttons in root module
gen_edit_role_rows = (
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





    
    

    

