# Treebard GPS

A showcase for genealogy software functionalities written in Python 3.8, Tkinter and Sqlite. 

## Treebard is for Everybody

Every version of Treebard that ever exists is supposed to be portable, free and open-source, but I have no control over that, it's just my personal preference. The code is officially unlicensed (public domain).

## No Installation

Tkinter and Sqlite come packaged with Python so if your Windows is in good shape, there are no installation or dependency problems, except to install Python. I've only tested it on a computer with completely up-to-date Windows 7 (32-bit). You should be able to install slightly older versions of Python (3.5?) if your Win 7 isn't up to date. Treebard should work on other operating systems, but I don't know.

To run Treebard, just run the .py file that has `root` in its name and everything else should work to whatever degree it is currently functioning.

## Roadmap to Infinity and Beyond

This project is a few years old and will take more years to finish. The GPS version will never be backward compatible, it's a Python program so I assume it will always run too slow for big databases. Its purpose is to demonstrate how things could/should/might work in a genealogy database GUI, so the main point is user experience and attention to detail when it comes to storing data in a useful way for real genealogists who care about details, sources, and the like, *as well as* a pleasant, congenial user experience.

Treebard works for even the most casual users because it's easy to use, intuitive, and doesn't force you to do things in a contrived way requiring lists of instructions. Brand new beginners can use it without glancing at any docs. Which is good because I haven't written the docs yet.

Treebard Version 0, if it comes to pass, might be written in Go and GioUI, or Dart and Flutter... who knows? I'm getting older every day and it might end up not being my problem. I'd love to take it on, but going from Python to a compiled language is a big jump for an old geezer.

GPS stands for _Genieware Pattern Simulation_. It originally stood for _genealogy programming source-first_ but I eventually realized that users won't be told how or when to enter their sources, so flexibility is my new dogma. Make it work for everybody, make it portable, make it public domain. My silliest fantasy is a genealogy program that becomes more ubiquitous than GEDCOM. I know, it will never happen. But the slogan would be, "Don't share a GEDCOM file... share the whole program!" So Treebard has to be portable because I'm a dreamer and because I believe that steep learning curves are an excuse for writing apps without considering the needs of the average user. Apps with a steep learning curve are geekware written for geeks.

I'm currently working to get data in and out of the database with the GUI itself rather than typing SQL commands. The action takes place mainly in an events table on the person tab and a person search dialog. I've been working on these portions of the GUI for many months. When the events table can be used to edit all the data types it can already display, it will be time to move on to linking sources. After that I suppose it will be time to work on defining, storing and calculating relationships. Then GEDCOM, charts, reports, etc. 

There's a lot left to do. For example, someday I'll use my domain **treebard.com** to publish a manual and tutorial.

For more details see the [forum](https://treebard.proboards.com/thread/22/history-future-treebard-project).

## We Support Each Other

If you're trying to test what there is so far and want me to support you, post your question at the [informal forum](https://treebard.proboards.com) and I'll see what I can do. Same goes if you just want to give me some advice. (But don't tell me to give up...) If you want to support me, you can check out my bio and some info on the solar energy project I gave my life to at [GoFundMe.com](https://gofundme.com/whearly). 

## Contributing is Allowable

I'm not actively looking for a team of coders right now but if such a team were looking for Treebard, I'd consider a team effort. 

### To ask questions, make suggestions, or request to join the team in any capacity:

* Go to [the Treebard forum](https://treebard.proboards.com)
* Join the forum.
* Introduce yourself by answering these questions: 
  * How you heard about Treebard.
  * Why you're interested in the project.
  * What you like and don't like about the Treebard philosophy.
  * Your level of experience with...
    * genealogy
    * programming, Python, SQL, GUI, html/css/Javascript, other.
* Post your question/suggestion/request in a new thread.

## Treebard's Kind of Genealogy

Genealogists of today are in two opposing camps: conclusion-based genealogy programs let the user decide what happened way back when, and allow sourcing but don't require it. (And usually make it prohibitively tedious to go to the trouble, so many users don't bother.) On the other side of the fence is evidence-based genieware. The creators of this genre of genieware try to solve the problem of users who don't get around to entering sources by encouraging you or forcing you to enter sources first. I once wanted to do it this way so bad that I was forced to take a look at my motivations. What finally convinced me to stop enforcing sourcing was when a Mr. Tamura Jones said something in a blog post to the effect that genealogists might actually _want or physically need_ to put their details into their database one factoid at a time. I got to thinking about this and had to admit that I wanted to do it my way too, which might be a different way on a different day. Instead of being forced to input data according to someone else's mindset being built into enforcementware.

I love to input sources but one of my goals will be to make it super easy to do, without all the copying and pasting of citations currently required by Brand X.

My other goal is to create a compromise between the two opposing camps with this slogan: "Assertion--Evidence--Conclusion." In Treebard, **assertions** have to be backed up with sources, **conclusions** can be linked to assertions *optionally*, and the assertions are never merged with the conclusions they support. So for example on the person tab you'll see a table of events (conclusions) for the current person. Each event row includes a button that says how many sources back up that conclusion. Zero sources is OK, because some of our conclusions are based on hunches or the sources will be filled in later. But in Treebard, the zero is explicit. Clicking the button shows the sources linked to the conclusion by opening the dialog where assertions and sources can be created, modified, and linked to conclusions.

The idea is to provide an alternative to typical conclusion-based genieware which is a spaghetti interface of bad _feng shui_ with no focus on sources unless you can find it somehow... vs. typical evidence-based genieware which has to allow sourceless input anyway if it's ever gonna be popular. My idea is to start out with a formal and permanent separation of assertions and conclusions and keep them separate. (For example, this will keep the user from recording more than one birth date conclusion for a person in a well-meant attempt to track all the evidence. Sources do not form conclusions. The user does that.) 

We'll see how it goes. The backbone of the plan is a _friendly and intuitive user interface_. Good software should make it look easy to do complicated things.
