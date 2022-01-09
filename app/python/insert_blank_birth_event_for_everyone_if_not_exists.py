# decided to make a blank birth event for each person as they are created, so this is to catch up by making blank birth events for everyone who doesn't already have a birth event in finding table; PART ONE worked but then PART TWO had to be run since every finding requires a blank place in finding_places if there is no place;

import sqlite3

# # PART ONE

# missing_births = '''    
    # SELECT person_id FROM person 
        # WHERE person_id NOT IN (
            # SELECT person_id FROM finding WHERE event_type_id = 1)
# '''

# conn = sqlite3.connect("d:/treebard_gps/data/sample_tree/sample_tree.tbd")
# conn.execute("PRAGMA foreign_keys = 1")
# cur = conn.cursor()
# cur.execute(missing_births)
# all_missing = cur.fetchall()
# # print(all_missing)


# cur.executemany('''
    # INSERT INTO finding  
    # VALUES (null, '0000-00-00-------', '', '0', ?, 1, '0,0,0')''', 
    # all_missing)
# conn.commit()

# # PART TWO

missing_places = '''    
    SELECT finding_id FROM finding 
        WHERE finding_id NOT IN (
            SELECT finding_id FROM finding_places)
'''

conn = sqlite3.connect("d:/treebard_gps/data/sample_tree/sample_tree.tbd")
conn.execute("PRAGMA foreign_keys = 1")
cur = conn.cursor()
cur.execute(missing_places)
all_missing = cur.fetchall()
# print(all_missing)


cur.executemany('''
    INSERT INTO finding_places  
    VALUES (null, ?, 1, null, null, null, null, null, null, null, null)''', 
    all_missing)
conn.commit()




cur.close()
conn.close()






'''sqlite> select person_id from finding where event_type_id = 1;
person_id
1
77
88
6
81
2
4
5
12
292
293
294
301
302
303
304
305
306
307
297
309
631
5555
388
3
5561
623
5592
421
5596
5598
5599
5600
5595
5557
5666
5675
5635
392
5766
5777
5778
5779
5783
5740
5711
5732
5677
5685


sqlite> select person_id from person where person_id in (select person_id from finding where person_id is not null and event_type_id = 1) and person_id is not null;
PERSON_ID
1
2
3
4
5
6
12
77
88
292
293
294
297
301
302
303
304
305
306
307
309
388
392
421
623
631
5555
5557
5561
5592
5595
5596
5598
5599
5600
5635
5666
5675
5677
5685
5711
5732
5740
5766
5777
5778
5779
5783

sqlite> select person_id from person where person_id not in (select person_id from finding where person_id is not null and event_type_id = 1) and person_id is not null;
PERSON_ID
7
8
11
295
296
298
299
300
308
310
311
312
322
324
379
380
381
382
383
386
387
389
390
391
393
394
395
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
448
449
450
451
452
453
454
455
456
457
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
624
625
626
627
628
629
630
632
633
634
635
636
637
638
5554
5556
5558
5559
5560
5562
5563
5564
5565
5566
5567
5568
5569
5570
5571
5573
5575
5576
5577
5578
5579
5580
5581
5582
5583
5584
5585
5586
5587
5588
5589
5590
5591
5593
5594
5597
5601
5602
5603
5604
5605
5606
5607
5608
5609
5610
5622
5623
5624
5625
5626
5627
5628
5629
5630
5631
5632
5633
5634
5636
5637
5638
5639
5640
5641
5642
5643
5644
5645
5646
5647
5648
5649
5650
5651
5652
5653
5654
5655
5656
5657
5658
5659
5660
5661
5662
5663
5664
5665
5667
5668
5669
5670
5671
5672
5673
5674
5676
5678
5679
5680
5681
5682
5683
5684
5686
5687
5688
5689
5690
5691
5692
5693
5694
5695
5696
5697
5698
5699
5700
5701
5702
5703
5704
5705
5706
5707
5708
5709
5710
5712
5713
5714
5715
5716
5717
5718
5719
5720
5721
5722
5733
5734
5735
5736
5737
5738
5739
5741
5742
5743
5744
5745
5746
5747
5748
5749
5750
5751
5752
5753
5754
5755
5756
5757
5758
5759
5760
5761
5762
5763
5764
5765
5767
5768
5769
5770
5771
5772
5773
5774
5775
5776
5780
5781
5782
5784
5785
5786
5787
5788
5789
5790
5791
5792
5793
'''


