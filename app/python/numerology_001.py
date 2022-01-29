# numerology_001


# finish numerology.py: user uses arrow keys to move w, u, y to vowel or consonant row (if text in (u,w,y):don't move; bind to arrow, turn red show instrux

import tkinter as tk

from dev_tools import looky, seeline

ones = ('a', 'j', 's') 
twos = ('b', 'k', 't')
threes = ('c', 'l', 'u') 
fours = ('d', 'm', 'v') 
fives = ('e', 'n', 'w') 
sixes = ('f', 'o', 'x')
sevens = ('g', 'p', 'y')
eights = ('h', 'q', 'z')
nines = ('i',  'r')

char_dict = {
	ones : 1,
	twos : 2,
	threes : 3,
	fours : 4,
	fives : 5,
	sixes : 6,
	sevens : 7,
	eights : 8,
	nines : 9}

vowels = ('a', 'e', 'i', 'o', 'u')
consonants = ('b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z')

 




name = "Robert Scott Lazar"

name = name.split()
lowered = []
for nick in name:
    nick = nick.lower()
    lowered.append(nick)
name = "".join(lowered)

nums_vowel = []
nums_consonant = []

for char in name:
    print("line", looky(seeline()).lineno, "char:", char)
    if char == "": continue
    for k,v in char_dict.items():
        if char in k and char in vowels:
            nums_vowel.append(v)
        elif char in k and char in consonants:
            nums_consonant.append(v)

sum_vowels = sum(nums_vowel)
sum_consonants = sum(nums_consonant)
sum_all = sum_vowels + sum_consonants
print(sum_vowels)
print(sum_consonants)
print(sum_all)
sum_vowels = str(sum_vowels)
sum_consonants = str(sum_consonants)
sum_all = str(sum_all)


sumv = 0
for char in sum_vowels:
    sumv += int(char)
print(sumv)
# final = final + str(sumv)

sumc = 0
for char in sum_consonants:
    sumc += int(char)
print(sumc)
# final = final + str(sumc)

suma = 0
for char in sum_all:
    suma += int(char)
print(suma)

def run_stage_2(stg):
    if len(str(stg)) > 1:
        sumall = str(stg)
        x = 0
        for char in sumall:
            x += int(char)
    else:
        x = stg
    print("x", x)
    return x

final = ''
for stg in (sumv, sumc, suma):
    stg = run_stage_2(stg)
    print(stg)
    final = final + str(stg)
print(final)



root = tk.Tk()

ent1 = tk.Entry(root)
ent1.grid(column=0, row=1)

ent11 = tk.Entry(root)
ent11.grid(column=0, row=3)

ent11.insert(0, ent1.get())








root.mainloop()



# DO LIST

# make GUI where user types the name then uses arrows to shift the letters above if vowel or below if consonant.

# 922
# Edward Ernest Reinhold Junior (actor Judge Reinhold) May 21, 1957 Wilmington, Delaware
# David Robert Magin the Third (pat's brother)

# 191
# reece joseph jones 191
# Henry Mancini b. Enrico Nicola Mancini; April 16, 1924 – June 14, 1994
# Mark Elliot Zuckerberg

# 854
# Billie Jean Moffit (Billie Jean King--tennis player) born: November 22, 1943, Long Beach, California, U.S
# donald lee morey 854

# 584
# Robert Larimore Riggs (Bobby Riggs--tennis player) Born: February 25, 1918, Lincoln Heights CA
# Donald Ray Robertson
# actor Brad Pitt: William Bradley Pitt Born: 18 December 1963, Shawnee, Oklahoma, United States

# 483
# Alison Maria Krauss Born: 23 July 1971 Decatur, Illinois

# 134
# Robert Anthony De Niro Junior born August 17, 1943 New York City, U.S

# 685
# william henry gates the third    born october 28 1955 - scorpio
# Hoyt Wayne Axton
# Antoinette Grace Gerber
# Mark Robert Michael Wahlberg Born: 5 June 1971, Dorchester, Boston, Massachusetts

# 628
# robert charles brozman
# Michael Francis Moore April 23, 1954 Davison, Michigan

# 268
# Chester Burton Atkins
# Mark Alan Robertson

# 786
# Herbert Buckingham Khaury --Tiny Tim-- (April 12, 1932 – November 30, 1996) b. Manhattan NY
# Reginald Kenneth Dwight 25 March 1947 Pinner, Middlesex, England (singer Elton John)
# Russell Asa Neal (inventor Bob Neal)
# David Bruce Rhaesa

# 865
# Terence Kemp McKenna  Nov 16, 1946 - Apr 3, 2000
# David Alan Richter b. Salina KS nov 5 1955

# 281
# stevenpauljobs born February 24, 1955 San Francisco, California, created Apple Computer in mid-1976 (birth name abdul lateef jandali)
# william burgess powell (amnesia victim "Benjaman Kyle") born August 29, 1948, in Lafayette, Indiana; disappeared in 1976.

# 821
# Francis Augustus Hamer (tracked down & killed Bonnie & Clyde) d. 7/10/1955
# Laura Phillips Anderson (musician Laurie Anderson)

# 246
# Pink (singer, aka Alecia Beth Moore) (born September 8, 1979)
# Roseann O'Donnell March 21, 1962
# Ferdinand Joseph LaMothe (Jelly Roll Morton)

# 426
# Geethali Norah Jones Shankar; March 30, 1979 USA
# robert eugene murray
# Taran Gostavo Braga Maquiran
# David Robert Magin Junior (pat's father)

# 314
# jovilla ortega maquiran
# born little panay 22 Nov 1962 3:00 a.m.

# 461
# John Fitzgerald Kennedy
# born 29 May 1917, Brookline, Massachusetts, United Statesthe 35th President of the United States, was assassinated on November 22, 1963, at 12:30 p.m. Central Standard Time in Dallas, Texas, while riding in a presidential motorcade through Dealey Plaza.
# David Andrew Sinclair Born: 26 June 1969, Sydney, Australia (biology of aging)

# 415
# David Byrne (songwriter, artist)
# 14 May 1952 (age 68) Dumbarton, Dunbartonshire, Scotland

# 235
# Zachary Monroe Bush MD, biology/environment/farming/health/teacher

# 123
# Diane Barbara Kapp

# 213
# charles hardin holly (singer Buddy Holly)  
# Nicholas Kim Coppola, (actor Nicholas Cage, born January 7, 1964, Long Beach, California)
# Elon Reeve Musk June 28, 1971 Pretoria, South Africa
# Kaspar Hauser (mystery boy)

# 112
# Aldous Leonard Huxley
# Aldous Huxley, (born July 26, 1894, Godalming, Surrey, England—died November 22, 1963, Los Angeles, California, U.S.

# 764
# Clive Staples Lewis
# C.S. Lewis, (born November 29, 1898, Belfast, Ireland [now in Northern Ireland]—died November 22, 1963, Oxford, Oxfordshire, England)
# Harry Edward Nilsson the third (June 15, 1941 Brooklyn NY – January 15, 1994)

# 671
# Herman Webster Mudgett aka "H H Holmes" America's first serial killer born 1861 gilmanton new hampshire

# 674
# Fred McFeely Rogers (March 20, 1928 – February 27, 2003) (Mister Rogers Neighborhood)
# Matthew Paige Damon, actor (October 8, 1970 Cambridge, Massachusetts)

# 178
# Terry Robert Miller born feb 9 1934 Neosho, Newton Co MO
# Bessie Louise Rathbun

# 371
# Donald Scott Robertson
# Opo of Opononi
# laura jeanne reese witherspoon actress born march 22 1976 - aries/taurus
# Owen Cunningham Wilson, actor born November 18, 1968 Dallas, Texas
# tammy wynette = virginia wynette pugh 371-8 May 5, 1942 – April 6, 1998
# patrick hubert kelly 371
# melissa marion ridgway 371 computer programmer/dog fanatic/hypochondriac
# the plumber who didn't wash his hands 371
# the trailer dweller who ran for pres every 4 years Jerry ? Carroll


# 731
# "Freddie Mercury"
# Bernard John Taupin 22 May 1950 (age 69) Sleaford, Lincolnshire, England (elton john's lyricist)
# Edward Harrison Norton; actor August 18, 1969, Boston, Massachusetts

# 527
# Leonard Dietrich Orr Birth 15 Nov 1937 Walton, Delaware County, NY Death 	5 Sep 2019 Asheville, Buncombe County, NC

# 573
# karen anne carpenter Mar 2, 1950, Feb 4, 1983
# Henry Saint Clair Fredericks (blues musician Taj Mahal) Born	May 17, 1942 Harlem, New York
# William Jefferson Clinton, (pres bill clinton)

# 437
# ann marie zimmerman Capricorn
# Todd Harry Rundgren Born	June 22, 1948 Philadelphia, Pennsylvania

# 753
# John Anthony Burgess Wilson - Anthony Burgess, also called Joseph Kell, (born February 25, 1917, Manchester, England—died November 22, 1993, London)

# 718
# Joseph Levitch (comedian Jerry Lewis) March 16, 1926 - August 20, 2017 Newark, New Jersey, U.S.

# 663
# Stephen Edwin King, born September 21, 1947 Portland, Maine

# 933
# Jeffrey Bryne Griffy

# 393
# Rowan Sebastian Atkinson, Born 6 January 1955, Consett, County Durham, England

# 336
# patricia lee smith 336 (singer Patti Smith)

# 999
# patricia lee huyett
# Steven Demetre Georgiou (Cat Stevens); 21 July 1948: London

# 595
# Barbara Ann Meier
# 2 1 9 2 1 9 1 1 5 5 4 5 9 5 9
#  3 1 2 3 1 1 2 6 1 9 9 5 5 5
#   4 3 5 4 2 3 8 7 1 9 5 1 1
#    7 8 9 6 5 2 6 8 1 5 6 2
#     6 8 6 2 7 8 5 9 6 2 8
#      5 5 8 9 6 4 5 6 8 1
#       1 4 8 5 1 9 2 5 9
#        5 3 4 6 1 2 7 5
#         8 7 1 7 3 9 3
#          6 8 8 1 3 3
#           5 7 9 4 6
#            3 7 4 1
#             1 2 5
#              3 7
#               1

# 955

# Alan Wilson Watts born 6 January 1915 Chislehurst, England Died	16 November 1973

# 549
# William Claude Dukenfield (W C Fields) born January 29, 1880 Darby, Pennsylvania, Died December 25, 1946

# 966
# Rodney Thomas Lunde
# Donovan Philips Leitch

# 696
# Marilyn Kay Moore

# 911
# Christine Ellen Hynde (Chrissie Hynde, The Pretenders)

# 819
# Richard Buckminster Fuller born July 12, 1895 Milton, Massachusetts
# "Luther Limbolust"
# Liv Rundgren (actress Liv Tyler) July 1, 1977, New York City, New York, U.S.
# Charlize Theron Born 7 August 1975 Benoni, South Africa
# Richard John Harris actor Born: 1 October 1930, Limerick, Ireland

# 988
# Patrick George Magin

# 898
# Kristina Kroesen

# 279
# Cynthia Ann Stephanie Lauper Born: 22 June 1953 Astoria, NY
# Ann Elizabeth McCarthy (leo)

# 729
# Theodore Robert Bundy (Ted Bundy serial killer)
# Richard Milhous Nixon, Born: January 9, 1913, Yorba Linda, California 
# Thomas Earl Petty, singer

# 742
# Eldon Russell Carter Junior
# Matthew David McConaughey, actor born November 4, 1969, Uvalde, Texas

# 472
# Alicia Christian Foster  "Jodie Foster" Born: 19 November 1962, Los Angeles

# 257
# Minnie Julia Riperton was born in Chicago, Illinois on November 8, 1947
# Thomas Alva Edison Born: 11 February 1847, Milan, Ohio Died: 18 October 1931, West Orange, New Jersey

# 797
# Jeffrey David McDonald

# 887
# "Limberluck"

# 538
# George Lafayette Heaton Junior
# Edward Estlin Cummings, (poet e e cummings)
# Dorthea Lauren Allegra Lapkus, comedian, born September 6, 1985, Evanston, Illinois

# 358
# Phoebe Ann Laub (Phoebe Snow) July 17, 1950 -  April 26, 2011 b. New York City

# 832
# aka Paul Rubens aka PeeWee Herman
# Paul Rubenfeld, August 27, 1952, Peekskill, New York

# 224
# James Thomas Patrick Kiernan
# John Joseph Nicholson, actor Jack Nicholson, Born: April 22, 1937, Neptune City, New Jersey

# 494
# Karen Sue Robertson
# Debra Kay Robertson

# 156
# Jimmy John Shea
# John Ronald Reuel Tolkien
# Robert Scott Lazer (UFO back-engineer Bob Lazer), born January 26, 1959 in Coral Gables, Florida

# 516
# Jerry Jeff Walker (born Ronald Clyde Crosby; March 16, 1942 – October 23, 2020
# John Harvey Kellogg (health scam industrialist)

# 167
# Mervyn Laurence Peake (9 July 1911 – 17 November 1968)
# James Michael Rhaesa (10 April 1957)
# James Edward Franco born April 19, 1978 Palo Alto, California

# 551
# David Robert Jones (singer David Bowie)







