# messages_context_help.py

from widgets import LabelH3
import dev_tools as dt

'''
    This module is used to store strings used as messages 
    in right-click context help menus.
'''

# CUSTOM MESSAGES USED IN ONE PLACE:

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
    # self.att.event_input,self.fontpicker.output_sample, 
    # self.fontpicker.font_size, self.fontpicker.cbo.entry, 
    # self.fontpicker.apply_button, 
    # colorizer.header, colorizer.current_display, 
    # colorizer.copy_button, colorizer.apply_button,
    # colorizer.add_button, colorizer.bg1, colorizer.fg1,
    # self.findings_table.headers[0], self.findings_table.headers[1], 
    # self.findings_table.headers[2], self.findings_table.headers[3], 
    # self.findings_table.headers[4], self.findings_table.headers[5], 
    # self.findings_table.headers[6], self.findings_table.headers[7], 
    # self.date_options.tester_head,  
    # self.date_options.date_test['Date Input I'], 
    # self.date_options.date_test['Date Input II'],
    # self.date_options.date_test['Date Input III'], 
    # self.date_options.pref_head,
    # self.date_options.prefcombos['General'].entry, 
    # self.date_options.prefcombos['Estimated'].entry, 
    # self.date_options.prefcombos['Approximate'].entry, 
    # self.date_options.prefcombos['Calculated'].entry, 
    # self.date_options.prefcombos['Before/After'].entry, 
    # self.date_options.prefcombos['Epoch'].entry, 
    # self.date_options.prefcombos['Julian/Gregorian'].entry, 
    # self.date_options.prefcombos['From...To...'].entry, 
    # self.date_options.prefcombos['Between...And...'].entry, 
    # self.date_options.submit, self.date_options.revert)
	
main_help_msg = (
    ("Use this field to change the current person (the person whose information is displayed in the Person Tab) to a person who exists in the tree or to a new person who you want to add to the tree. When you start typing, Treebard will try to guess which person you want based on what you type as well as what you selected last time you typed in a person autofill input. If Treebard guesses right, click the OK button. If you type a name that Treebard doesn't recognize, nothing will happen so Tab past the OK button to the button that says 'Find or Create a Person'. The Person Search Dialog will open, and you can use it to search for the person you tried to enter, if you forgot how their name was spelled for example. For more information, see the context help under the Search Dialog. If the person whose name you typed is new to the tree, Tab on to the Add New Person button. For more information on this dialog, see the context help there.\n\nIn the case of a name which occurs more than once in the tree, let's say you have three people named 'Moira Harding' in your tree, with ID numbers 5735, 5739 and 5740. The one with the lowest ID number will fill in, unless one of the others has been used more recently, in which case that one will fill in. If you know which one you want, just change the ID number to the one you want, but chances are you might not know. Just Tab past the OK button and open the Search Dialog. Here you will see the same person filled in, and the search results table below will be empty. Delete the ID number, and all three Moiras will appear in the table, each with their own row. In the row will also appear any birth or death dates, and names of father and mother, if you've entered this information already. In this way you'll be able to tell which Moira you were after. Just click her name and she will become the new current person. If you're still not sure, you can point the mouse at the names or ID numbers, and more information will appear in a tooltip in the form of any alternate names, nicknames, etc. that you have entered for each Moira. This system allows you to enter several people by the same name without having to compromise the facts by entering them as 'John Smith son of George' or anything like that.\n\nIf you do happen to know a person's ID number, you can enter it into the Change Current Person Input following a '#' character and press OK to change the current person.\n\nIf you know any alternate names for the person who you want to make current, they will also fill into the input when you start typing them, and when the right nickname or other stored name fills in followed by '#' and the right ID number, press OK to change the current person.",
        "Person Tab: Change Current Person Name Input"),
    ("Pressing this button will change the current person, i.e. the person displayed on the Person Tab. If the person displayed in the input to the left of this button has an ID number also displayed, that's all that happens when the button is pressed, but if there's nothing like '#235' or whatever the ID number is, the New Person Dialog will open. So one way to make a new 'John Smith' if there's already a person by that name in the tree is to start typing 'John Smith', and when the existing John Smith fills in, just delete the ID number and '#', and press OK to open the New Person Dialog. Another trick is to ignore the name that fills in if you don't want to change to that current person. If you know the ID number of the person you want to change to, just change the ID number after the name that filled in, and press OK. The current person will change to the person that has that ID number.",
        "Person Tab: Change Current Person OK Button"),
    ("When typing into the main person entry input at the top of the application which is used to change the current person, you have to type a name or ID number exactly as stored in the database, but the Search Dialog works differently. To search a name, press the button that says 'Find or Create a Person'. If a name is already in the input to the left, that name will automatically fill into the input at the top of the Search Dialog, but you can change it or delete it and start over. For this input, you don't have to know the whole name, just some part of it, or some part of any alternative name the person has. For example, if the person has a prisoner number and you happen to remember it had a double 8 in it, just type a double 8, and the results table will display a row for the right person. This also works for Treebard person ID numbers, if you remember part of one of them. But usually this dialog will be used to find unknown ID numbers when you only remember part of a name or when there's more than one person with the same exact name but you don't know which one you want. The results table shows not only ID numbers and names, but also birth and death dates, as well as parents' names, if they exist in the database.",
        "Person Tab: Person Search Button"),
    ("The main image for each person is the one that is displayed on the Person Tab. If you click the image, a gallery will open to show the rest of the person's stored images, if any. In this gallery there is a radio button under each thumbnail image which, if selected, will change that person's main image to the selected image. If the person has no main image, and you don't want to provide default images or use the ones that come with Treebard, the images tab will not open by default; instead the Do List Tab will open by default.",
        "Person Tab: Current Person Main Image"),
    ("The Events Table on the Person Tab and the Attributes Table on the Attributes Tab are identically designed, but contain different information. If you enter an attribute, it will end up on the Attributes Table, even if you create it from the Person Tab, and vice versa. More information on how to tell the difference is given below. The New Events and Attributes Input fills in automatically with values from a list that includes both events and attributes. For more information on the New Events Dialog, open one and look at its help context topics.",
        "Person Tab: New Event or Attribute Input"),
    ("The Events Table on the Person Tab and the Attributes Table on the Attributes Tab are identical in every way. If you enter an attribute, it will end up on the Attributes Table, even if you create it from the Person Tab, and vice versa. More information on how to tell the difference is given below. The New Events and Attributes Input fills in automatically with values from a list that includes both events and attributes, since the line between these two elements is sometimes fuzzy, so at this initial point of selecting a type to input, it's appropriate to combine them.\n\nWhen you start typing a new event in the New Event or Attribute Input, it will autofill with the last event type used or the closest spelling, whichever comes first. When the correct event type has filled into the input, press the NEW EVENT OR ATTRIBUTE button to open the New Event Dialog. It will display the event type you selected and the current person's name and ID number. At the top of the dialog there will be inputs for date, place, particulars and age as pertaining to this person and this event. Any of these fields can be left blank. If you leave the date blank, the event will be displayed on the attributes table. If you fill in a date, the event will be displayed on the events table. See the final paragraph in this topic for more information on how to get the event to display in the right table. See the context help topics in the Date Preferences Tab for a lot more information.\n\nIf this event applies to only the current person (i.e. if it isn't a couple event such as 'marriage'), there's nothing more to do. The event will appear immediately, interfiled by date in the Events Table, or on the Attributes Tab if no date is input. But if the event is a couple event such as wedding, elopement, separation, etc., then another set of widgets will appear in the bottom half of the dialog. Here you will be able to input the name of the other person such as the spouse, if you know it. You will be required to enter a kin type such as 'husband' or 'wife' for each partner, whether you know the partner's name or not. If you want to create a kin type that's not already in Treebard, type anything you want here and a New Kin Type Dialog will open so you can specify that this is a Partner kin type vs. some other kind.\n\nBack on the topic of new events types: in Treebard when a man or woman becomes a parent biologically, that person experiences an 'offspring' event. This event is made automatically by the program when you create the child's birth event and give the child parents. If you try to create an offspring event in the New Event or Attribute Input, Treebard will notify you that this will be done automatically.\n\nTreebard is aware that separating events and attributes by whether or not the event is dated is not always perfectly accurate, but you have a lot of control over where an event or attributes appears. As an example, my grandparents all had gray hair when they were old, but my paternal grandmother also had gray hair when she was young. It would be interesting to note as an event that her hair turned gray 'about 1920 to 1930'. But for most people whose normal hair color was known, it would be silly to add a date to say when someone had a hair color; that would be a natural attribute. But take job vs. career for example. Either one could be on the events table by giving it a date, even if an estimated or approximate date. But to say someonen was a farmer by trade could go either way. If the statement is from a dated source, personally I would prefer to see it as a dated event, even though it is more like an attribute. But if you wanted, you could just add a date informally to the Particulars column, in which case, the attribute would be found on the Attributes Table. In spite of any shortcomings, Treebard feels that this is a better system than interfiling dated and undated events on a single table which then tries to sort itself by date and can't.",
        "Person Tab: New Event or Attribute Input"),
    ("When you change the font family selected in the bottom input, this text will change to the selected font so you can see what it looks like.",
        "Font Preferences Tab: Sample Output"),
    ("The Font Size Input changes the size of the main text display across the whole application. Only this one setting is needed. Treebard will change the larger and smaller fonts proportionately.",
        "Font Preferences Tab: Font Size Input"),
    ("The Font Family Input detects what fonts are installed on your computer and lets you choose from among them. Treebard uses two fonts: an input font and an output font. The input font is Dejavu Sans Mono and the default output font is Courier. You can change the output font to anything you want. Treebard has chosen to use a fixed-width or monospaced font for input widgets, which is why we don't have to use resizable columns in tables.",
        "Font Preferences Tab: Font Family Input"),
    ("The Font Preferences APPLY button will change the output font family and size, application-wide, to whatever you've chosen.",
        "Font Preferences Tab: APPLY Button"),
    ("There are several ways to try a color scheme before applying it. The color preferences tab is a preview area. If you click on one of the color swatches, the preview area will change colors so you can preview the color scheme. Or you can Tab through the swatches to see the selected swatch change, and the preview area change with it.\n\nBut the easiest way to preview many color samples quickly is to traverse the swatches with the arrow keys. The up and down arrows traverse within a column, while the left and right arrows traverse by row, and from row to row. While traversing with the arrow keys, the scrollbar won't be needed; the swatches area will autoscroll as needed.\n\nIn either case, no changes will be made to the application in general till you press APPLY.",
        "Color Scheme Tab: Preview and Traversal"),
    ("Click the currently applied color scheme ID to highlight its swatch. The highlight is bright green. This lets you see the swatch currently in effect, outlined in green and staying in one place, while arrowing around to preview other color schemes which will be outlined in orange.\n\nThis is especially useful if you want to adjust the currently applied color scheme, by letting you easily find out which swatch is applied. You can click the green-outlined swatch to preview it, then click the COPY COLOR SCHEME button. Its colors will fill into the four inputs, and from there you can easily adjust one or more colors and use the ADD COLOR SCHEME button to save the adjusted color scheme as a new color scheme.",
        "Color Scheme Tab: Current Color Scheme ID"),
    ("The COPY COLOR SCHEME button is used to copy an existing color scheme so you can adjust one or more parts of it and save it as a new color scheme. You can even delete the original color scheme by highlighting the swatch and pressing the Delete key. If you had created the original color scheme yourself, it will be deleted, but if it's a built-in scheme that came with Treebard, it will be hidden. Hidden color schemes can be unhidden on the Types Tab.\n\nTo copy a color scheme, highlight the corresponding swatch by arrowing to it, clicking on it or tabbing into it, then press the COPY COLOR SCHEME button. The color names for the four colors in the highlighted swatch will be automatically copied into the four inputs at the bottom of the Color Scheme Preferences Tab. Hex color names have to be 3 or 6 characters long and preceded by a '#' character.\n\nThere are a few ways to change any of the four colors: 1) replace any character in a hex name with a numeral or a letter from a to f; 2) type a valid color string such as 'blue' or 'steelblue'; 3) paste in a hex color name from a graphics program; 4) double-click in one of the four inputs to open a color picker and select any color you want.\n\nAs soon as there are four valid colors in the inputs, the new color scheme will be previewed automatically. When you get a combination you like, press the ADD COLOR SCHEME button to add a new swatch to your copy of Treebard.\n\nFor more information, review the context help topics for other buttons and fields in the Color Schemes Tab.",
        "Color Scheme Tab: COPY COLOR SCHEME Button"),
    ("The APPLY button should be used after first trying a color scheme and then creating a new color scheme based on what is previewed for your color choices. The trial scheme will be shown on the Color Scheme Preferences Tab only. To apply this scheme to the whole application instantly, click APPLY, Tab to the APPLY button and press the spacebar key when the APPLY button is in focus, or press the Enter/Return key to APPLY whatever swatch is current.",
        "Color Scheme Tab: APPLY Button"),
    ("The ADD COLOR SCHEME button at the bottom of the Color Scheme Preferences Tab will create a new swatch at the bottom of the swatch area. The new swatch will be based on hex color values which you can fill into the four inputs above the button, either by typing or pasting color values that you know, or by selecting a swatch and pressing the COPY COLOR SCHEME button, or by double-clicking in an input to open a color picker.\n\nTreebard uses a simple color scheme so anyone can create their own color scheme in seconds. If you want a dark theme, choose three relatively dark colors and in the bottom of the four inputs, enter a relatively light color for text. If you want a light theme, choose three relatively light colors and in the bottom input, enter a relatively dark color.\n\nThe top input is for the main background color. The second input is for a main highlight color, and the third is for a secondary highlight color. By arrowing from swatch to swatch, you can see how this works with existing color schemes.",
        "Color Scheme Tab: NEW COLOR SCHEME Button"),
    ("If you want a dark theme, choose three different relatively dark colors. I usually make this background color 1 the darkest, but it's up to you. By keeping the number of colors down, this system is fast and easy to use, and the results can be beautiful, simple, and easy to read.\n\nPrimary colors fatigue the eye faster than muddy or earthtone colors, but it's completely up to you; if you prefer a black background with hot pink highlights and bright yellow text, Treebard will not try to stop you. For light-colored themes, you're on your own. Treebard can show those too, but I can't look at them; it's like looking at bare lightbulbs and has the same effect on my eyes, besides using more power.\n\nFor inspiration you can browse online resources such as http://colorhunt.co where color lovers post thousands of color schemes, or you can browse websites taking screenshots from themes you like, paste them into your graphics program, and get the graphics program to tell you what the hex numbers for the colors are.",
        "Color Scheme Tab: Background Color 1 Input"),
    ("If you want a dark theme, choose a light font color. If you want a light theme, choose a dark font color. For a theme with medium backgrounds, choose whatever font color--light or dark--is easier to read against the background colors.",
        "Color Scheme Tab: Font Color Input"),
    ("This topic will introduce the Events Table and Attributes Table, which are located on the Persons Tab and Attributes Tab respectively, and are in most ways identically structured. For more information about the columns, consult the context help topics at the various column heads on either table. Both tables are in reference to the Current Person.\n\nThe events table is sorted by date, however even if dates are obviously wrong, birth will always be first, death will always be last except for burial and other after-death events which will be in order of date below the row for death. Everything else will appear strictly in order. In the case of range or span dates, the first date is the one that will be sorted on.\n\nThe plain text fields in the first five columns take in put directly, but respond differently, depending on that columns validation requirements. The Age and Particulars columns are not validated, you can put any text in these fields. The Places column is an autofill input which remembers the last place you input that starts with the characters you're typing and tries to fill in what you are probably trying to type. Date columns are easy to use, validated to disallow bad dates, and formatted according to your settings in the Date Preferences Tab.\n\nThe Event column accepts Event Types including those which are new to Treebard. Couple events can be changed to different couple events and generic (non-couple) events can be changed to other generic events. For example, a marriage can be changed to a wedding or a career can be changed to an occupation, but a divorce can't be changed to a death. In general, to change the text in a table cell, just change it, and your changes will be saved instantly. There is a SAVE menu item, as well as the usual CTRL+S that you expect, but all this does is to redraw the events table, since changes are saved automatically as soon as they're made, except in dialogs where there is an OK or SUBMIT button.\n\nThe last three columns contain buttons instead of plain text. The Roles and Notes columns have either plain buttons or buttons with three dots ('...') to indicate that Roles and Notes are linked to that event or attribute. To create roles and notes when none exist, just open the dialog by clicking the blank button in the row corresponding to the relevant event. The Sources column says how many citations--and thus how many assertions--are linked to the event which the row corresponds to.",
        "Events Table: Event Type Column"),
    ("Event types are of two basic kinds: events and attributes. For example: Grandma Robertson had prematurely gray hair, so I could record Hair Color as a dated event with a range date such as 'between 1920 and 1930' and with 'prematurely gray' in the Particulars column. But assuming that Grandpa had brown hair most of his life, this would naturally belong in the Attributes Table without a date, and I don't think it matters how many of his hairs turned gray in which year.\n\nSince the two tables are nearly identical, they are  easy to use. Instead of entering new rows directly into the tables, you enter them into the New Event Dialog and Treebard decides whether the event is an event or an attribute. It doesn't matter whether you input a new event into the New Event Input at the bottom of the Events Table or the one at the bottom of the Attributes Table, because they work identically.\n\nWhile Treebard's one and only criteria for deciding whether an event is an event or an attribute is whether or not it has an official date, we recognize that reality is not this simple. But Treebard needs a date-sorted table in the Persons Tab in order to tell a proper story of a human being, so undated events are not allowed here. It's up to you, but Treebard suggests adding estimated or approximate dates to events where the exact dates are unknown, in order to get them interfiled reasonably well by date on the events table. On the other hand, if you have a date for an attribute but really want that attribute on the attributes table, just put the date in the Particulars column or in a note, and on the Attributes Table it will stay. To move an attribute to the Events Table, give it a date. To move an event to the Attributes Table, remove the date from the Dates column.",
        "Events Table: Date Column"),
    ("Places are input as nestings of smaller places nested within larger places, with each place separated by a comma, as in 'Aspen, Pitkin County, Colorado, USA'. Commas within a single place name are not allowed. The place input will fill in automatically as soon as you start typing, and will preferentially fill in the last place you used that started with the typed letters instead of just selecting alphabetically. So if you are using the same place name over and over, no matter how long the nested place name is, you'll usually have to type only a few characters unless the place name is new to your copy of Treebard. Treebard doesn't come bogged down with place names since we think you should enter the places that are right for your needs and spelled the way you prefer to spell them. When entering a new place, you have to tell Treebard the proper spelling and capitalization by typing it that way the first time. After the place is already stored, you don't have to capitalize anything.\n\nIf a part of the nested place name already exists in the database but something else is not the same, a New & Duplicate Place Dialog will open so that a mistaken entry is not made. For example, if George was born in Paris, Texas but his wife was born in Paris, France, Treebard will not try to guess which Paris you're talking about when you try to input a second Paris besides the first one that's already been stored. In the dialog, a row will exist for every possibility that Treebard can think of, and you just select the right one for each part of the nested place. This might seem redundant but there's a good reason for it, besides the unique notion that mistaken place data should not be stored. We have used programs that let us treat Paris, Texas and Paris, France as the same place, and correcting the resulting mistakes had to be done laboriously and manually. Treebard feels that dealing with a New & Duplicate Places Dialog is a lot easier than making a lot of manual corrections.\n\nBut another good reason exists for going to all this trouble. In the real world, a city in the state of Texas, USA might have once been located in the Republic of Texas. Did Dallas get up and go somewhere? Not likely. In Treebard, a place can be nested in any number of parent places, and you can also optionally track the span of time during which each parent place was actually the nested place's parent. This feature exists almost nowhere else. The autofill feature was inspired by the place autofill in a program called Genbox, but has been improved, and extended so that person's names and some other elements will also fill in automatically.",
        "Events Table: Place Column"),
    ("The Particulars column is for very short notes. If more than a few words, you should use the Notes Dialog instead, since Treebard doesn't use resizable columns, so long inputs will make the interface larger than the screen. The Particulars column is particularly well-suited for additional input in event rows such as 'occupation', where you can type 'farmer' or in the case of an illness you could type 'typhoid fever' into the Particulars column. In an offspring event, which is created automatically for any person born whose parents are known, you could add the name of the child in the Particulars column, although this information is also available in a different table on the Person Tab. In the Attributes Table, the Particulars column is a good place to put a date if you want to prevent the attribute from displaying in the Events Table.",
        "Events Table: Particulars Column"),
    ("In the interest of not getting ahead of our sources, Treebard doesn't fill in calculated ages. All age input is yours to do. You can put any text you want in an Age cell, such as '89y, 9m, 14d'.",
        "Events Table: Age Column"),
    ("Roles are a key feature in Treebard which is mostly or completely missing from most genieware applications. How many times have you felt compelled to research the odd neighbor or boarder, with the sneaking suspicion that there is a story to be found that profoundly affected your family story. The differently-surnamed adjunct person could even turn out to be a relative. Treebard believes that we can't be serious about telling a story if we're not interested in the people who our ancestors were interested in, so Treebard provides a robust system for keeping track of these auxiliary folks. They are treated the same as any other person and are easily accessible in the Roles Dialog, searchable in the Person Search, etc. For more information, consult the context help topic for the Roles Dialog.",
        "Events Table: Roles Column"),
    ("Treebard lets you link the same note to any number of sources so that you don't have to copy, paste and store the same note more than once. Because of this extra attention to detail, we need a way to track notes that is meaningful to the genealogist (instead of ID numbers for example), so we have topic heading for each note. Each topic heading is unique throughout the whole tree, and the topic headings appear in a Table of Contents for the event or attribute that the note is linked to. For more information, see the context help topics for the Notes Dialog.",
        "Events Table: Notes Column"),
    ("The Sources button displays a number indicating how many assertions are linked to that event. An assertion is a claim made by a source. The Events and Attributes Tables are conclusions tables, so there should be a single conclusion recorded for each event; in fact, Treebard won't allow two birth or death events since this is physically impossible. But sources don't always agree, so Treebard provides another layer of data that mediates between the source and the conclusion, and that is the Assertion. If you click the SOURCES button, the Assertions Dialog will open. There you can view, create, and edit Sources, Citations, and Assertions. Since it is bad form to record two conclusions about the same event in the Events Table, Treebard provides Assertions where each Source could conceivably suggest its own separate conclusion. So let's say you have a residence event but different sources tell a different story about where the person lived at a particular time. You can record anything you want on the Events Table as a conclusion (except for multiple births or deaths for the same person). Then each source for that event can be linked to a separate assertion. The SOURCES button in the Events or Attributes Table will count the assertions linked to that event.",
        "Events Table: Sources Column"),

    ('The date entry demo section at the top of the Date Preferences '
    'tab allows you to test various ways of inputting and displaying '
    'dates. Nothing you enter here will affect your tree, but the '
    'three input fields are exact working models of every date input '
    'field in Treebard. For more info, right-click for context help in '
    'each of the three input fields.', 
    'Date Settings Tab: Date Entry Demo'),

    ('Here\'s a list of '
    'ways that date qualifiers and months can be input and displayed:\n\n'
    "separators: [space, dash, slash, asterisk or underscore]\n\n"
    'estimated dates: ["est", "est.", "est\'d"]\n\n'
    'approximate dates: ["abt", "about", "circa", "ca", "ca.", "approx."]\n\n'
    'calculated dates: ["cal", "calc", "calc.", "cal.", "calc\'d"]\n\n'
    'before dates: ["bef", "bef.", "before"]\n\n'
    'after dates: ["aft", "aft.", "after"]\n\n'
    'before current era: ["BCE", "BC", "B.C.E.", "B.C."]\n\n'
    'current era: ["CE", "AD", "C.E.", "A.D."]\n\n'
    'Julian calendar: ["OS", "O.S.", "old style", "Old Style"]\n\n'
    'Gregorian calendar: ["NS", "N.S.", "new style", "New Style"]\n\n'
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
    'to avoid ambiguity in international exchange of trees, Treebard doesn\'t allow months to be displayed as numbers. Then to avoid confusion and bloated code, Treebard doesn\'t allow months to be input as numbers either. Most folks will appreciate the simplicity of this approach, since typing "d" for "December" is easier than typing "12" anyway. To make it even easier, all month inputs are case insensitive. If you wanted to type "mArCh", that would not be a problem. It will be displayed as "March", "Mar" or "Mar.", depending on your stored preferences.\n\nWhen inputting years with less than four digits, such as the year 33 AD, add preceding zeroes, i.e. "0033". '
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
    'unambiguous to anyone including plain folks like me with little education. For example, my personal favorite way to display dates is the ISO format (1200-12-14 for December 14, 1200), but this format might be unfamiliar to some folks so I dropped it.\n\n'
    'Treebard has no option for displaying bad dates, in fact '
    'Treebard refuses to store them. For example, "March 10" is a '
    'bad date because there is no year. In case you have a hint '
    'like that, notes or the Particulars column of the Events Table are a good place to store them. In '
    'this way, every stored date can be used in calculations such '
    'as subtracting one date from another to find out how old someone '
    'was when something happened.\n\nTreebard deletes bad date input '
    'and tells you why, so you can retype the date the right way. If a '
    'mistake in editing a date on the Events Table makes the whole event '
    'disappear, it\'s because the bad date was deleted. This caused the '
    'event to move to the Attributes Table on the Attributes Tab. It can '
    'be resurrected as an event by finding it in the Attributes Table and '
    'giving it a good date.', 
    'Date Settings Tab: Date Input Fields (3 of 3)'),

    ('Nine different choices can be made in regards to how you want '
    'Treebard to display dates. Display style has nothing to do '
    'with how a date is entered. By making choices in the bottom '
    'part of the Date Preferences tab and then inputting sample data in '
    'the three input fields at the top of the Date Preferences tab, '
    'you can sample how dates of different types will be displayed without affecting the data in your tree.\n\nTreebard has its own defaults which you can use by ignoring '
    'the options on the Date Display Preferences tab. You can '
    'change options at any time '
    'or revert to Treebard\'s defaults if you want. Changes will '
    'be reflected in how dates display next time you reload the '
    'program.\n\nChanging date display styles does not affect your tree '
    'in any way since all dates are stored in a single consistent '
    'format to make the program work more efficiently. The display format '
    'you choose will apply to all your trees application-wide.', 
    'Date Settings Tab: Date Display Preferences'),

    ('While you can enter dates with a lot of freedom, Treebard only '
    'allows dates to display in ways that are unambiguous. In this '
    'way, genealogists can share their trees with confidence that their '
    'dates will not be misread by people from other parts of the '
    'world.\n\nThe only way Treebard will display dates is using spelled-out '
    'or partially spelled-out months such as "Jan", "Jan." or '
    '"January". If '
    'display like "10-1-1888" were allowed, in some countries this '
    'would be interpreted as Oct. 1, 1888 while in other countries '
    'it would mean Jan. 10, 1888. We originally planned to allow dates to be entered this way, but in an attempt to keep Treebard code simple and free of bloat, it was decided to not allow numerical date input either.', 
    'Date Settings Tab: General Date Display'),

    ('Estimated and approximated dates could be used in distinct ways. '
    'What follows is Treebard\'s suggestion on how this could be done.\n\n'
    'Sometimes the user wants to enter a date when he doesn\'t have '
    'one, for example to get an event to appear in the right order in '
    'the Events Table. (In Treebard, an undated event is treated as an attribute and won\'t appear in the Events Table at all.) Suppose a source states that someone '
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
    'it belongs within the Events Table.', 
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
    '1000 AD [remind me to do this] since we\'re used to seeing 4-digit dates. And if one '
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
    'click the SUBMIT PREFERENCES'
    'button to store the changes. Changes made to your '
    'date format settings have no effect on Treebard defaults, '
    'which can be reverted to at '
    'any time. You can change formats as often as you like. Changes '
    'take effect next time you restart the program, except for new edits and input which uses the new formatting immediately. Display formats '
    'have nothing to do with how dates are entered or how they are '
    'stored, so you don\'t need to consider anything except how you '
    'want dates to look when displayed.', 
    'Date Settings Tab: SUBMIT PREFERENCES Button'),

    ('To return to Treebard\'s out-of-the-box default date display '
    'settings, click the REVERT TO DEFAULT VALUES button. Date display settings ' 
    'specific to your currently open tree will be deleted '
    'but the dates will be unaffected. ' 
    'Date display settings for all your trees will change accordingly. ', 
    'Date Settings Tab: REVERT TO DEFAULT VALUES Button'))

# rcm_widgets = (
    # self.role_type_input.entry, self.person_input, self.add_butt, 
    # self.done_butt, self.close_butt)
roles_dlg_help_msg = (
    ('Type or select the role type for a new role. A role type can be anything except the primary participants in the event. For example, at a wedding event there\'s a bride and groom who are primary participants in the event. Don\'t input them here. But many other roles exist such as bible bearer, ring bearer, flower girl, best man, religious official, usher, witness, candle-lighter, photographer or anything you want. In a document describing an event, many names might be mentioned that you might want to research further, or record in case they end up being related to the family or the family\'s story in some way. Role types can\'t be blank, but you can select \'other\' or \'unknown\'. For example, a group photo from a wedding has names listed on the back, but you don\'t know who some of the people are. Just input the names and select \'unknown\' role type. They\'ll be added to the database same as anyone else, so if the name pops up again, you won\'t have to go searching for it in notes. Built-in role types can\'t be deleted but they can be hidden in the Types Settings Tab in Preferences. Custom role types can be deleted or hidden.', 'Roles Dialog: Role Type Input'),

    ('For a role you don\'t always know the names of the people involved, but maybe you want to research it. You can enter roles with no names, or known names with \'other\' or \'unknown\' selected as the role type. You can create new people here. If you add a role with a new person, a dialog will open so you can specify the new person\'s name type such as birth name or nickname; gender if known; image if any; and preferred sort order for alphabetization. If you input a name that already exists in the database, another dialog will ask whether you intended to create a new person by the same name. This will help prevent duplicate persons which would have to be merged later if not caught when trying to input them. You can input as many John Smiths as you want, since each person entered has a unique ID in the database. Later if you find that two persons in the database are really the same person, the two can be merged so that your work doesn\'t have to be done over. If you know the name of someone who participated in an event but you don\'t know what role they played, you can still input the name and select \'other\' or \'unknown\' as the role type.', 'Roles Dialog: Person Input'),

    ('Use the ADD button to add a role if you\'ll be adding more than one role, so the dialog doesn\'t close. The new roles will instantly be added to the roles table and you\'ll be able to edit or delete them at any time.', 
    'Roles Dialog: ADD Button'),

    ('Use the DONE button to close the roles dialog if you\'re only going to create one new role. If nothing is in the inputs, the dialog will close harmlessly.', 
    'Roles Dialog: DONE Button'),

    ('Use the CLOSE button to close the roles dialog if you\'re not adding any more new roles. Even if you\'ve typed all or part of a new role, what you typed will be ignored. Roles you already entered will not be affected. They can be deleted or edited with the EDIT buttons in the roles table rows.', 
    'Roles Dialog: CLOSE Button'))

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
    'Person Search Dialog: Person Search Input'),

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
    'Person Search Dialog: Person Search Table'), 

    ("lorem ipsum", "Person Search Dialog: title")
)

# rcm_widgets = (
    # self.date_input, self.place_input, self.particulars_input, 
    # self.age1_input, self.new_evt_msg)
new_event_dlg_help_msg = (
    ("Like the date inputs on the Events Table, you can input date parts in almost any order, use a variety of abbreviations for date qualifiers, etc. Unlike the Events Table cells, the date won't be formatted according to your preferences until the dialog closes. Then the date will be correctly formatted as it appears in the new row on the table. For more information on how to input dates, see the Dates Preferences Tab, where there are also some test input widgets where you can instantly see results of various date inputs without affecting your tree.\n\n",
        "New Event Dialog: Date Input"),
    ("Like the place inputs on the Events Table, this place input will fill in automatically with whatever places are spelled like what you're entering, beginning with the most recent places you've entered in the Events Table. When you tab out of the place input, if you've entered any place names that are new or duplicated, the New & Duplicate Places Dialog will open. See the context help topic at the Places column in the Events Table for more information.",
        "New Event Dialog: Place Input"),
    ("The Particulars Input in the New Event Dialog works the same as the Particulars column in the Events Table. This field is for very short notes or additional details. For example, in an 'educational level' attribute, you could type 'through grade 4' in the Particulars input. For larger notes, use the Notes Dialog which will be available in the new event or attribute row after you close the New Event Dialog.",
        "New Event Dialog: Particulars Input"),
    ("Age is input in any format such as '23', '23 yrs', '23y 10m 13d' etc. Treebard doesn't calculate ages.",
        "New Event Dialog: Age Input"),
    ("When you start typing a new event in the New Event or Attribute Input, it will autofill with the last event type used that begins with the characters you're typing. When the correct event type has filled into the input, press the NEW EVENT OR ATTRIBUTE button to open the New Event Dialog. It will display the event type you selected and the current person's name and ID number. At the top of the dialog there will be inputs for date, place, particulars and age as pertaining to this person and this event. Any of these fields can be left blank. If you leave the date blank, the event will be displayed on the attributes table. If you fill in a date, the event will be displayed on the events table. See the final paragraph in this topic for more information on how to get the event to display in the right table. See the context help topics in the Date Preferences Tab for a lot more information.\n\nIf this event applies to only the current person (i.e. if it isn't a couple event such as 'marriage'), there's nothing more to do, except to respond to a dialog which will open so you can tell Treebard whether or not the event is the sort of thing that would take place after the person's death, such as reading of the will or anything that would be expressed as 'posthumous _____'. Then the event will appear immediately, interfiled by date in the Events Table, or on the Attributes Tab if no date is input.\n\nBut if the event is a couple event such as wedding, elopement, separation, etc., then another set of widgets will appear in the bottom half of the dialog. Here you will be able to input the name and age of the other person such as the spouse, if you have this information. You will be required to enter a kin type such as 'husband' or 'wife' for each partner, whether you know the partner's name or not. If you want to create a kin type that's not already in Treebard, type anything you want in one of the kin type inputs, and a New Kin Type Dialog will open so you can specify that this is a Partner kin type vs. some other kind.\n\nIn Treebard, when a man or woman becomes a parent biologically, that person experiences an 'offspring' event. This event is created automatically by the program when you create the child's birth event and give the child parents. If you try to create an offspring event in the New Event or Attribute Input, Treebard will notify you that this will be done automatically.\n\nTreebard is aware that separating events and attributes by whether or not the event is dated is not always perfectly accurate, but you have a lot of control over where an event or attribute appears. As an example, my grandparents all had gray hair when they were old, but my paternal grandmother also had gray hair when she was young. It would be interesting to note as an event that her hair turned gray 'estimated 1920 to 1930'. But for most people whose normal hair color was known, it would be silly to add a date to say when someone had a hair color; that would be a natural attribute. But take job vs. career for example. Either one could be on the events table by giving it a date, even if an estimated or approximate date. But to say someone was a farmer by trade could go either way. If the statement is from a dated source, personally I would prefer to see it as a dated event, even though it is more like an attribute. But if you wanted, you could just add a date informally to the Particulars column, in which case, the event would be found on the Attributes Table. In spite of any shortcomings, Treebard feels that this is a better system than interfiling dated and undated events on a single table which then tries to sort itself by date and can't.",
        "New Event Dialog: General Information"))

# # rcm_widgets = (
    # # self.radios["parent"], self.radios["sibling"], 
    # # self.radios["partner"], self.radios["child"])
# new_kin_type_dlg_help_msg = (
    # ("This feature is not currently being used.",
        # "New Kin Type Dialog: Parent Select"),
    # ("This feature is not currently being used.",
        # "New Kin Type Dialog: Sibling Select"),
    # ("This item should be selected when creating a new kin type, if the kin type is a partner such as 'wife, husband, mistress, business partner' etc.",
        # "New Kin Type Dialog: Partner Select"),
    # ("This feature is not currently being used.",
        # "New Kin Type Dialog: Child Select"))

# rcm_widgets = (
    # self.pic_canvas, self.prevbutt, self.nextbutt, self.b1)
gallery_help_msg = (   
    ("Image galleries are available for persons, places and sources. The place images are viewable in the Places Tab and the source images are in the Sources Tab. The Person Gallery opens in a separate dialog when you click the image on the Person Tab. All the images linked to the Current Person will be shown as small thumbnails at the top of the gallery. In the Person Gallery, there will be a radiobutton under each thumbnail so the image represented by that thumbnail can be selected as the person's Main Image. In all the galleries, hovering over the thumbnail will show a tooltip displaying the image's filename. Clicking the thumbnail will display the full-size version in the Viewport.\n\nThe file name and full path of the image as well as a caption and the image's pixel dimensions, are shown in the far right panel of the gallery. The text of these labels can be placed in the clipboard so it can be pasted elsewhere.\n\nThe Viewport (large image) can be focused by clicking on it. When it's in focus, the image can be changed with the right or left Arrow keys. There are also buttons under the Viewport which can change the image.\n\nThe EDIT button will place a copy of the Viewport image in the Graphics Tab where certain basic operations can be performed such as cropping, resizing, renaming, copying, etc.\n\nThe size of the largest image stored for the current element will determine how large the viewport is, with the maximum size being some proportion of your screen size. If you don't like a large Viewport, don't link any large pictures to your Treebard elements. However, if the image doesn't fit in the viewport, it will still be shown at its normal resolution, and you can pan it in the Viewport by dragging it with the mouse.",
        "Image Gallery: Viewport"),
    ("The PREVIOUS Button shows the previous image in the Viewport. The order of the images is the same as shown in the Thumbnail Strip at the top of the Gallery. The Arrow keys on the keyboard can also be used to change the image in the Viewport, if the Viewport is in focus. The Viewport can be focused by clicking it with the mouse or tabbing into it.",
        "Image Gallery: PREVIOUS Button"),
    ("The NEXT Button shows the next image in the Viewport. The order of the images is the same as shown in the Thumbnail Strip at the top of the Gallery. The Arrow keys on the keyboard can also be used to change the image in the Viewport, if the Viewport is in focus. The Viewport can be focused by clicking it with the mouse or tabbing into it.",
        "Image Gallery: NEXT Button"),
    ("The image shown in the Viewport can be copied into the Graphics Tab by pressing the EDIT button. In the Graphics Tab, you'll be able to do some basic image manipulations such as cropping, renaming and resizine.",
        "Image Gallery: EDIT Button"))

# rcm_widgets = (opener, new, importgedcom, opensample, cancel, self.picbutton)
opening_dlg_help_msg = (
    ("Open an existing tree.",
        "Opening Dialog: OPEN TREE Button"),
    ("Create a new tree based on Treebard defaults, including places stored in your other trees.",
        "Opening Dialog: NEW TREE Button"),
    ("Create a new tree absed on Treebard defaults, places stored in your other trees with other data imported from a GEDCOM file which you can select from any place on your computer.",
        "Opening Dialog: IMPORT GEDCOM Button"),
    ("The Sample Tree will open. You can make any changes you want, and if you want, you can restore it to its original content.",
        "Opening Dialog: OPEN SAMPLE TREE Button"),
    ("Closing the Opening Dialog will allow Treebard File Menu and Tools Menu options to be used with no tree open.",
        "Opening Dialog: CANCEL Button"),
    ("Clicking the big image on the Opening Dialog will open the last tree you worked on. You can click the image with the mouse or tab into it to focus it, and press the Space Bar when the image is in focus. Treebard will not open any tree automatically when you load the application, for these reasons: 1) if the tree is very large, it could take a long time to open, and you'll have to wait for it to load completely and then close it; and 2) Sometimes a genealogist will have two or more trees that are similar, and we don't want to find ourselves working in the wrong tree by accident. So Treebard will only open a tree that you specifically select from your file system. If you do want to open the last tree you worked on, to speed this up, just click the big picture instead of using the OPEN button. To further speed this up, the Opening Dialog opens with the big image already in focus, so as soon as the dialog opens, you can just press the Space Bar to open the prior-used tree.",
        "Opening Dialog: OPEN PRIOR TREE Button")
)

places_dlg_help_msg = ()

links_dlg_help_msg = ()

# MESSAGES USED GENERICALLY BY ALL THE WIDGETS MADE IN A LOOP.

# roles dialog editx buttons
role_edit_help_msg = (
    'Clicking the Edit button will open a row of edit inputs. '
    'You can use them to delete a role or to change the role '
    'type or role person for the row you clicked. You can also '
    'create a new role type--anything you want--or a new person. '
    'If you input a new person, a New Person Dialog will open so you can '
    'select gender, sort order for alphabetization, image, and '
    'name type. Role types '
    'can\'t be blank, but you can select \'other\' or \'unknown\' '
    'from the dropdown list. Built-in role types can\'t be deleted, '
    'but they can be hidden in the Types Settings tab in Preferences. '
    'Custom role types can be deleted or hidden unless they\'re '
    'being used in the tree.', 
        'Roles Dialog: Edit Existing Role Button')

# places dialog nest label
places_dialog_label_help_msg = (
    "The New & Duplicate Places Dialog exists to keep your 'Paris, Texas' "
        "ancestors from being born in Paris, France; to prevent duplicate "
        "places being made if possible, and to allow you to nest the same "
        "city--such as Paris, Texas--in an alternative parent place--such as "
        "the Republic of Texas--at different periods of its history, without "
        "making you split it into two different cities in the same location. "
        "\n\nPlaces in Treebard are stored as single elements such as 'Paris' "
        "and as nested elements such as 'Paris, Texas' and 'Paris, Republic of "
        "Texas'. Texas in turn can be nested in a place called 'USA', and the "
        "result is a whole nesting such as 'Paris, Texas, USA'. When a new or "
        "potentially duplicate place name is entered, the dialog opens with a "
        "separate area for each nested place where you can accept Treebard's "
        "guesses about each place or change the pre-selected option to the "
        "right one. If one or more places in the nesting can't be defined accurately with this "
        "procedure, CANCEL the dialog and create your new place in the Places "
        "Tab instead of trying to create it on the fly in this dialog.\n\n"
        "Each nesting has usually a pair of radio buttons with options for you "
        "to select from. Above the radio button is a label describing the option "
        "you can select, for example: '2: Plymouth Rock, place ID #907'. The '2' just says how "
        "many layers of nesting exist above this one. You can probably ignore "
        "this number. After that comes the name of the place as you entered it, e.g. 'Plymouth Rock'. Then an ID number suggested by Treebard, or a list of ID numbers if there were more than one place by this name already in the tree. But in this case there are no places by this name in the tree already, so there's only one radio button, one possible ID number, and the radio button is pre-selected. You can just glance at this and keep going. For more information on the radio button selections, refer to the context help on this widget.",
            "New & Duplicate Places Dialog: Place Nest Label")

# places dialog radio button
places_dialog_radio_help_msg = (
    "If there are two or more radio buttons to select from, it's because Treebard thinks there could be more than one possibilities, and rather than guessing, we think we should ask you, the researcher, to select the right choice. Usually you can just click OK, but in some cases this dialog will keep you from storing the same place twice. It will help you catch spelling errors that make this easy to do. It will remind you that you alread entered Timbuktu, Africa, and it will make sure that your ancestors in Timbuktu aren't accidentally located in Timbuktoo, California.\n\nEach nest in a nested place like 'Plymouth Rock, Massachusetts, USA' has its own section of one or more radio buttons. Usually Treebard will pre-select the right one, but to eliminate bloated and complex code, some of these choices have been left up to you. In this case, since there's no place in the tree yet called 'Plymouth Rock' it's a new place. So why do we give you the choice of making a new place called 'Massachusetts' or using the one that's already been entered? It seems silly, isn't there only one place in the world named Massachusetts?\n\nThis may be true, but Treebard is not meant to do your research for you, and if we write software that makes your decisions for you--or else just doesn't validate any content--then you're going to end up putting your ancestors in the wrong Paris and you'll pay for Treebard's mistake. Treebard doesn't want to waste your time by making your decisions for you and we don't want to write bloated, complicated code. So if your ancestors are from a place called 'Paris', you're going to get every opportunity to get them into the right Paris. There are over a dozen cities named Paris, in the United States alone. We feel that Treebard can be helpful and nice, but if trying to be helpful makes more work for you, then that's not very nice. In fact, we don't like smart software because it's wrong over half the time and we have to undo its mistakes.\n\nFortunately, this dialog, which will seem superfluous much of the time, will not only save you work in the long run, but is very easy to use. If Treebard has made the right selections, just press OK and you're on your way.",
        "New & Duplicate Places Dialog: Place Nest Radio Button")

# places dialog hint input
places_dialog_hint_help_msg = (
    "Below each radio button in the New & Duplicate Places Dialog, there's a little button that says 'EDIT' if you point at it with your mouse. Next to that is a label that says 'Hint:' and unless you've stored a hint for this place, the hint display will be blank. If you click the button, a Place Hint Input opens up. This is not meant to be used all the time, but you can use it as much as you want. Its purpose is to give you a way of telling two duplicate place names apart. Here's an oversimplified example: there are dozens of names for the nation of Israel, from different periods of history. What if you wanted to have two places named 'Israel', and use one of them for 'ancient Israel' and one of them for 'modern Israel'? Just provide hints and spell the actual place names the same way. Of course this is a bad example since none of Israel's real names were probably ever spelled 'Israel' but it's just a simplified example. Another place would be a city called Maine in the State of Maine. Hints might come in handy here, or in the case of the city of Sassari which is in the state or province of Sassari. Any simple hint could be devised for easily telling the two apart, so you don't have to take a detour to try and figure out which way you entered them.",
        "New & Duplicate Places Dialog: Hint Input")

# color preferences tab color swatches
color_preferences_swatches_help_msg = ("Treebard's philosophy on color schemes is that it's none of Treebard's business what colors you want to display, but in order to give you the freedom to choose, the method of choosing should be very easy. You will find it easy to create new color schemes, which will display in the Samples Strip at the top of the Color Scheme Preferences Tab. Treebard comes with several color schemes built-in, and opens in a dark theme by default. This can be changed in seconds, either by selecting a different color scheme or by creating your own. Detailed instructions for doing this are given in the context help topics throughout the Color Scheme Preferences Tab. To delete one of your color schemes, highlight it by clicking on it or tabbing into it, and press the Delete key. You might want to COPY it first, and adjust the copy, before deleting the one you don't like. All schemes can be TRIED before they are APPLIED. Windows color schemes should have no effect on any part of Treebard's display. Built-in color schemes can't be deleted.",
    "Color Scheme Tab: New Color Scheme Area")

# image gallery thumbnails
gallery_thumbnail_help_msg = ("All the images linked to the current element (person, place or citation) will be shown as small thumbnail images in a strip across the top of the Gallery. You can link as many images to an element as you like, and if the thumbnails don't fit into the width of the Gallery, there is a horizontal scrollbar so you can use them all. In the Person Gallery, there's a radio button below each thumbnail which, if clicked, will change the corresponding image to that person's Main Image. In all the galleries, pointing at a thumbnail with the mouse will show its file name, and to see (and copy) the full path with the file name, display it in the larger Viewport and its data will appear in the far right panel. To display the image corresponding to a thumbnail, click it with the mouse.",
    "Image Gallery: Thumbnails Strip")



    
    

    

