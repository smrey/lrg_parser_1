#Are the exon co-ordinates of the correct type
#The list is called 'exons' (The co-ordinates within are stored as tuples and called 'coords') and should be integers



exons = [(0, 3), (6, 7), (10, 16)] #Create a list of errors to test (remember to include floats). Should we test for co-ords not = 0 (i.e. is 0 a possible co-ordinate or not)??

#print type(exons)
#print type(exons[0])

for tupInd in range(len(exons)):
    #print type(tup)
    #print tupInd
    for num in exons[tupInd]:
        #print num
        assert type(num) == int, "Exon co-ordinates are not integers" #This is pretty much impossible
        
        
        '''
        #print type(num)
        print exons[tupInd][num]
        assert type(exons[tupInd][num]) == int, "Exons is somehow not a list"
        '''
