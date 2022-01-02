# restore_default_color_schemes.py

# accidentally deleting everything in a table is easy, so save this in case it's ever needed again

import sqlite3

default_color_schemes = ((1,'#061D2F','#284b80','#267d82','#71cfd5',1,0),
	(None,'#232931','#393e46','#2E5447','#eeeeee',1,0),
	(None,'#393932','#4d4545','#8d6262','#f1c5c5',1,0),
	(None,'#212121','#323232','#0d7377','#7efee1',1,0),
	(None,'#423030','#605656','gray','lightgray',1,0),
	(None,'#a3e4db','#fed1ef','#72aef7','#333333',1,0),
	(None,'#f0ece3','#dfd3c3','#c7b198','#5e5448',1,0),
	(None,'#d3e4cd','#f2ddc1','#e2c2b9','#33282d',1,0),
	(None,'#fff1af','#b4c6a6','#ab937b','#1c150e',1,0),
	(None,'#f3f0d7','#cee5d0','#fed2aa','#1f1913',1,0),
	(None,'#c8e3d4','#f6d7a7','#f6eabe','#1a1814',1,0),
	(None,'#e5dcc3','#c7bea2','#aaa492','#12110f',1,0),
	(None,'#faeee0','#f9e4c8','#d8d0c0','#121110',1,0),
	(None,'#f3f0d7','#cee5d0','#e0c097','#1d2226',1,0),
	(None,'#f3d5c0','#d4b499','#889eaf','#242426',1,0),
	(None,'#ffe3e3','#e4d8dc','#c9ccd5','#21201a',1,0),
	(None,'#feffe2','#f0f0cb','#dad5ab','#1c1a17',1,0),
	(None,'#f4dfd0','#dad0c2','#cdbba7','#1a1615',1,0),
	(None,'#f8e2cf','#f5c6aa','#fcd8d4','#0f1112',1,0),
	(None,'#f1ecc3','#c9d8b6','#90a7b0','#171612',1,0),
	(None,'#e6ddc6','#c3b8a3','#a19882','#1f181b',1,0),
	(None,'#caf7e3','#f6dfeb','#e4bad4','#1c1a16',1,0),
	(None,'#f6e6cb','#e3cdc1','#a0937d','#171a16',1,0),
	(None,'#f8ede3','#bdd2b6','#798777','#171315',1,0),
	(None,'#caf7e3','#f6dfeb','#e4bad4','#141414',1,0),
	(None,'#f9f7cf','#f2dcbb','#bbbbbb','#151617',1,0),
	(None,'#f4f4f2','#e8e8e8','#bbbfca','#170e11',1,0),
	(None,'#d6e5fa','#baabda','#d77fa1','#1a0e12',1,0),
	(None,'#7b6079','#506362','#de8971','#e3d8e2',1,0),
	(None,'#433520','#025955','#00917c','#fde8cd',1,0),
	(None,'#0d335d','#1a508b','#c1a1d3','#fff3e6',1,0),
	(None,'#19456b','#11698e','#16c79a','#f8f1f1',1,0),
	(None,'#424242','#a98b98','#4e3d53','#a6f0c6',1,0),
	(None,'#351f39','#726a95','#485154','#a0c1b8',1,0),
	(None,'#222831','#4f8a8b','#615229','#eeeeee',1,0),
	(None,'#3e3838','#ae7c7c','#365e5a','#e3dada',1,0),
	(None,'#305973','#ef7e56','#787371','#e6dfdc',1,0),
	(None,'#041c32','#04293a','#064663','#ced7db',1,0),
	(None,'#112031','#152d35','#345b63','#d4ecdd',1,0),
	(None,'#334257','#476062','#548ca8','#eeeeee',1,0),
	(None,'#351f39','#726a95','#485154','#a0c1b8',1,0),
	(None,'#382933','#3b5249','#3d5448','#a4b494',1,0),
	(None,'#4d4646','#5b5656','#47544a','#f5eaea',1,0),
	(None,'#222831','#393e46','#d65a31','#eeeeee',1,0),
	(None,'#33313b','#62374e','#007880','#ccbec5',1,0),
	(None,'#33313b','#3c4f65','#834c69','#e6f5ff',1,0),
	(None,'#272121','#363333','#e16428','#f6e9e9',1,0),
	(None,'#2a2438','#352f44','#5c5470','#dbd8e3',1,0),
	(None,'#a0937d','#3a6351','#5f939a','#f2edd7',1,0),
	(None,'#35483a','#647d73','#7e6373','#d5e0dc',1,0),
	(None,'#35483a','#647d73','#4d444b','#d5e0dc',1,0),
	(None,'#34615f','#4a8a87','#486a8c','#b9ddd9',1,0),
	(None,'#344140','#5a7270','#977d77','#ffffff',1,0),
	(None,'#1e1e1e','#484848','#43523f','#d7d7d7',1,0),
	(None,'#b8a089','#cbbaa9','#ded3c9','#2d241c',1,0),
	(None,'#0C1021','#55606c','#808c9b','white',1,0),
	(None,'#283133','#899ea3','#86a68b','white',1,0),
	(None,'#2F343F','#424242','#212121','#AFB9C6',1,0),
	(None,'#38555f','#507987','#4d598a','#ced6d9',1,0),
	(None,'#151a26','#3d4b6d','#6c8093','#dadee6',1,0),
	(None,'#152028','#232b32','#202945','#d8dee3',1,0),
	(None,'#121212','#606782','#34393b','#99b0bb',1,0),
	(None,'#121212','#403250','#34383d','#d9d5de',1,0),
	(None,'#dbdde8','#b4b8cf','#8087ae','#1c1c21',1,0),
	(None,'#bcd0d3','#97b7bb','#639196','#141b1c',1,0))

print(default_color_schemes)

conn = sqlite3.connect('d:/treebard_gps/data/sample_tree/sample_tree.tbd')
cur = conn.cursor()
cur.executemany('''
    INSERT INTO color_scheme 
    VALUES (?,?,?,?,?,?,?)''', 
    default_color_schemes)
conn.commit()
cur.close()
conn.close()



