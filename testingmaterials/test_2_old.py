#Checks that the sequence contains only A, C, T, G.
##Sequence we want is gsequence from first function

#Import file
##TO DO
gsequence = 'zAGCTAGTCGATCTz'

nucleotides = ['A','C','T','G']

for nuc in gsequence:
    if nuc not in nucleotides:
        #print 'error'
        raise Exception, "Non-nucleotide character in sequence"
    else:
        print 'yay'