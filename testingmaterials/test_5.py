#Are the co-ordinates pairs?
#Is co-ordinate 2 of pair > co-ordinate 1 of pair

#exons = [(0, 3), (6, 7), (10, 16)] #Create a list of errors to test (remember to include floats)
exons = []

assert exons == True, "List of exon co-ordinates is empty. No exon co-ordinates stored."
for tup in exons:
    try:
        assert len(tup) == 2, "Error: Missing co-ordinate in list of exon co-ordinates"
        assert tup[0] < tup[1], "Second co-ordinate of co-ordinate pair bigger than first"
    except TypeError:
        print "Error: Missing co-ordinate in list of exon co-ordinates"
    
    '''
    if tup[0] > tup[1]:
        print 'error'
    else:
        print 'whahay'
    '''
    