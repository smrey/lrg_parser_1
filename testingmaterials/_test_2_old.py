#Test that output file has same number of exons as input file

import xml.etree.ElementTree as ET
from sys import argv

#Import xml file
def _test_2(xmlfilename, fastafilename):
	'''
	this function opens the xml file and gets the tree and root
	'''
	# opens the xml file, parses the XML and counts number of times xml file has the exon tag
	tree = ET.parse(xmlfilename)
	root = tree.getroot()
	xmlExonCount = 0
	fastaExonCount = 0
        for element in tree.iter():
		if element.tag == "exon" and "label" in element.attrib:
			xmlExonCount += 1
	#xmlExonCount = 20	#Just put this line in to make sure it catches problems
	#print "xmlExonCount is", xmlExonCount
	
	#Parse FASTA file
	fastafile = open(fastafilename)	
	for line in fastafile:
		#print line[0:1]
		if line[0:1] == '>': #CAUTION: Assumes each exon has a header and that this is the only header
			fastaExonCount += 1
	#print "fastaExonCount is",  fastaExonCount
	assert xmlExonCount == fastaExonCount, 'Output number of exons does not match number expected from input file'
	return 'Number of exons in input and output file match. Yay!'
#raise ExonNumberingError('Output number of exons does not match number expected from input file')
#Exception('Output number of exons does not match number expected from input file')
	




compExonCount = _test_2(argv[1], argv[2])
print compExonCount
#test2 = _test_2(filename)
