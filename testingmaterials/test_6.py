#Is the second co-ordinate from exon n-1 smaller than the first co-ordinate from exon n

exons = [(0, 3), (6, 7), (10, 16)] #Create a list of errors to test (remember to include floats)

#for tupN in len(exons):
#tupN = len(exons)
#print range(tupN)

for tupInd in range(len(exons)-1):
    #print exons[tupInd][1]
    #print exons[tupInd+1][0]
    assert exons[tupInd][1] < exons[tupInd+1][0], "Exon n starts before the end of exon n-1"
     