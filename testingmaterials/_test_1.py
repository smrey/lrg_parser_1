#Is the sequence the genomic sequence, i.e. is it the longest seqeunce available
#is the sequence of zero length...?

import xml.etree.ElementTree as ET
from sys import argv

#Import file
##TO DO
def lrg_parse(filename):
	'''
	this function opens the xml file and gets the tree and root
	'''
	# opens the file and parses the XML
	tree = ET.parse(filename)
	root = tree.getroot()
        return tree


def lrg_sequence(tree): ##Taken from original code (is there a way to call this when it is already loaded)

        #to get the genomic sequence

	# results list
	seq_max_len = 0
	gsequence = ""

	for element in tree.iter():
		# check the sequences, track the longest sequence seen and return the longest as this will be the genomic sequence
		if element.tag == "sequence":
			if len(element.text) > seq_max_len:
				seq_max_len = len(element.text)
				gsequence = element.text
	return gsequence

def test_1(tree):
	sequencesList = []
	gsequence = lrg_sequence(tree)
	#gsequence = 'ACTG' #Test that the test catches problems
	#print gsequence
	for element in tree.iter():
		if element.tag == "sequence":
			sequencesList.append(len(element.text)) ##This needs to include length
	LongestSeqLen = max(sequencesList)
	#print LongestSeqLen	
	assert LongestSeqLen == len(gsequence), "The pulled sequence is not the longest"
	assert len(gsequence) > 0, "The pulled sequence's length is 0" ##Should we set a higher limit for what we think is too small for a genomic sequence??


tree = lrg_parse(argv[1])
#gsequence = lrg_sequence(tree)
test = test_1(tree)

  
