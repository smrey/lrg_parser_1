#Is the sequence the genomic sequence, i.e. is it the longest sequence available

import xml.etree.ElementTree as ET
from sys import argv

#Import file
def lrg_parse(filename):
	'''
	In this test, this function opens the xml file and gets the tree and root
	Example usage: lrg_parse(LRG_292.xml)
	'''
	# opens the file and parses the XML
	tree = ET.parse(filename)
	root = tree.getroot()
        return tree


def lrg_sequence(tree): ##Taken from original code- gsequence can be read directly from this function within the code if required
	'''
	In this test, this function gets the genomic sequence in the same way as it is done within the code.
	A future piece of work will be to read this output in from the code (as it actually ran) in a more efficient way.
	Example usage: In this test, requires that lrg_parse be run and is called directly by another function.
	'''	
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
	#gsequence = 'ACGT' #This line can be uncommented to show that the assertion will trigger if the sequence is not the longest	
	return gsequence

def test_1(tree):
	'''
	This function creates a list containing all of the sequences within the LRG file. It finds the longest sequence in the list
	and then compares this to the genomic sequence identified from the code to ensure that the genomic sequence has been correctly 
	identified. It assumes that the genomic sequence is the longest sequence stored within the LRG file.
	This test has not been incorporated into the code to save doing this test every time the code runs as it has a few loops and
	therefore might slow the code down.
	Example usage: test_1(lrg_parse(LRG_292.xml))
	'''
	sequencesList = []
	gsequence = lrg_sequence(tree)
	for element in tree.iter():
		if element.tag == "sequence":
			sequencesList.append(len(element.text)) ##Creates a list with the lengths of each sequence in the xml
	LongestSeqLen = max(sequencesList)	
	assert LongestSeqLen == len(gsequence), "The pulled sequence is not the longest"


test = test_1(lrg_parse(argv[1]))

  
