# Treebard GPS

A showcase for genealogy software functionalities written in Python 3.8, Tkinter and SQLite.

## How to Use this Repo

The only requirement is a recent version of Python and pip install Pillow for graphics. The Pillow install has worked effortlessly for me with no other dependencies in spite of what the Pillow docs say, as long as I used Python 3.8 or 3.9. If you don't know how to pip install Pillow, five minutes of research should be enough. You'll also need to install the SQLite terminal tool which is effortless as well, only so you can import the .sql text file into a binary database file. All of this is very easy. 

Once you have the SQLite terminal installed, you can also connect to the database and enter data using SQL commands manually. But the point of this commit (2021-12-11) is that the app-so-far finally functions as a coherent unit. So entering data manually in the terminal should not be done unless you know what you're doing and how the data is structured. The GUI is functioning well as far as I know, barring the discovery of bugs. Nothing is finished but what's there is mostly now a coherent functioning whole after 6- or 7-months refactoring, during which everything was in a state of flux.

The exact commands used to import and export a SQLite database file to a text file and back are shown in treebard_gps/etc/dump_output.txt. The .sql file is a text file so it's humanly readable. It's everything that SQLite needs to recreate the database. But you don't need to humanly read it. Just import it.

To get your copy of the repo to function, import treebard_gps/etc/default_new_tree.sql into treebard_gps/data/settings/default_new_tree.db using the import commands mentioned above. Make two copies of the database using your file manager, one to be called treebard_gps/data/sample_tree/sample_tree.tbd and one to be called treebard_gps/app/default/default_new_tree_untouched.db. If you want an actual populated copy of my current messy real sample_tree.tbd so you can open a tree that has stuff in it, contact me at treebard/proboards.com and I'll send it to you, but if not, the procedure above should get you started so you can enter your own sample data into a blank tree and see how everything works.

One more import has to be done. Import treebard_gps/etc/treebard.sql to treebard_gps/data/settings/treebard.db.

# Limitations

I have not tested any of this code on Linux or MacOS. This is not yet version 0 or 1. The GPS version will never have backward compatibility, everything is subject to change drastically without notice. 

## Treebard is for Everybody

Every version of Treebard that ever exists is supposed to be portable, free and open-source, but I have no control over that, it's just my personal preference. The code is officially unlicensed (public domain).

## No Installation

Tkinter and SQLite come packaged with Python so if your Windows is in good shape, then there should be no installation or dependency problems to run Treebard, except to install Python and one dependency called Pillow. I've only tested this on a computer with completely up-to-date Windows 7 (32-bit) and Windows 10 (64-bit). Without a recent version of Python (3.8 or 3.9), good luck getting Pillow installed. Without Pillow nothing will work unless you want to downgrade to using .gif images only and rewrite all the code involving images. Tkinter will handle .gif without Pillow but this was not a good experience for me.

To run Treebard, just run the .py file that has `root` in its name and everything else should work to whatever degree it is currently functioning.

## Roadmap to Infinity and Beyond

This project is 3-1/2 years old (full-time) and will take more years to finish. The GPS version will never be backward compatible, it's a Python program so it might run too slow for big databases. (But Gramps runs on Python and I think they'd disagree that Python is too slow.) GPS' purpose is to demonstrate how things could/should/might work in a genealogy database GUI, so the main point is user experience and attention to detail when it comes to storing data in a useful way for real genealogists who care about details, sources, and the like, *as well as* a pleasant, congenial user experience.

Treebard works for even the most casual users because it's easy to use, intuitive, and doesn't force you to do things in a contrived way requiring lists of instructions. Many first-time users will be able to use it without glancing at any docs.

Treebard Version 0 will be written in Electron, JavaScript, SQLite, HTML and CSS. If you want to use more advanced programming languages, just fork it and let me know how it goes. I'm getting older every day and going from Python to a compiled language would be a big jump for an old geezer who's going blind.

GPS stands for _Genieware Pattern Simulation_. It originally stood for _genealogy programming source-first_ but I eventually realized that users won't be told how or when to enter their sources, so flexibility is my new dogma. Make it work for everybody, make it portable, make it public domain. My silliest fantasy is a genealogy program that becomes more ubiquitous than GEDCOM. I know, it will never happen. But the slogan would be, "Don't share a GEDCOM file... share the whole program!" So Treebard has to be portable because I'm a dreamer and because I believe that steep learning curves are an excuse for writing apps without considering the needs of the average user. Apps with a forbidding appearance and a steep learning curve are geekware written for geeks. Nothing wrong with that, but genealogy is a hobby for most and for this reason I've tried to keep the GUI simple-looking while making it able to manipulate complex data behind the scenes.

There's a lot left to do. For example, someday I'll use my domain **treebard.com** to publish a manual and tutorial.

For more details see the [forum](https://treebard.proboards.com/thread/22/history-future-treebard-project).

## We Support Each Other

If you're trying to test what there is so far and want me to support you, post your question at the [informal forum](https://treebard.proboards.com) and I'll see what I can do. Same goes if you just want to give me some advice. (But don't tell me to give up...) If you want to support me, you can check out my bio and some info on the solar energy project I gave my previous life to at [GoFundMe.com](https://gofundme.com/whearly). 

## Contributing is Allowable

I'm not actively looking for a team of coders right now but if such a team were looking for Treebard, I'd consider a team effort. After about four years of doing this full-time, I might be better advised to get out of this chair and into the garden, if I want to live long enough to get old.

### To ask questions, make suggestions, or request to join the team in any capacity:

* Go to [the Treebard forum](https://treebard.proboards.com)
* Join the forum and read some of my rants.
* Introduce yourself by answering these questions: 
  * How you heard about Treebard.
  * Why you're interested in the project.
  * What you like and don't like about the Treebard philosophy.
  * Your level of experience with...
    * genealogy
    * programming, Python, SQL, GUI, html/css/JavaScript, other.
* Post your question/suggestion/request in a new thread.

## Treebard's Kind of Genealogy

Genealogists of today are in two opposing camps: conclusion-based genealogy programs let the user decide what happened way back when, and allow sourcing but don't require it. (And usually make it prohibitively tedious to go to the trouble, so many users don't bother.) On the other side of the fence is evidence-based genieware. The creators of this genre of genieware try to solve the problem of users who don't get around to entering sources by encouraging you or forcing you to enter sources first. I once wanted to do it this way so bad that I was forced to take a look at my motivations. What finally convinced me to stop enforcing sourcing was when a Mr. Tamura Jones said something in a blog post to the effect that genealogists might actually _want or physically need_ to put their details into their database one factoid at a time. I got to thinking about this and had to admit that I wanted to do it my way too, which might be a different way on a different day. Instead of being forced to input data according to someone else's mindset being built into enforcementware.

I love to input sources but one of my goals will be to make it super easy to do, without all the copying and pasting of citations currently required by Brand X.

My other goal is to create a compromise between the two opposing camps with this slogan: "Evidence--Assertion--Conclusion." In Treebard, **assertions** have to be backed up with sources, **conclusions** can be linked to assertions *optionally*, and the assertions are never merged with the conclusions they support. So for example on the person tab you'll see a table of events (conclusions) for the current person. Each event row includes a button that says how many sources back up that conclusion. Zero sources is OK, because some of our conclusions are based on hunches or the sources will be filled in later. But in Treebard, the zero is explicit. Clicking the button shows the sources linked to the conclusion by opening the dialog where assertions and sources can be created, modified, and linked to conclusions.

The idea is to provide an alternative to typical conclusion-based genieware which is a spaghetti interface of bad _feng shui_ with no focus on sources unless you can find it somehow... vs. typical evidence-based genieware which has to allow sourceless input anyway if it's ever gonna be popular. My idea is to start out with a formal and permanent separation of assertions and conclusions and keep them separate. (For example, this will keep the user from recording more than one birth event for a person in a well-meant attempt to track all the evidence. In Treebard, sources do not form conclusions. The user does that.) 

We'll see how it goes. The backbone of the plan is a _friendly and intuitive user interface_. Good software should make it look easy to do complicated things.
