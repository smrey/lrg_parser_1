#Test that output file has same number of exons as input file

import xml.etree.ElementTree as ET
from sys import argv

#Import xml file
def _test_2(xmlfilename, fastafilename):
	'''
	This test is to ensure that the output FASTA file has the same number of exons as the input xml file.
	If the number of exons does not match, an assetion error will occur and the files will need to be manually inspected.
	If the test passes, the function returns a message indicating success.		
	Example usage: _test_2(LRG_292.xml, LRG_292.fa). The names of the file minus the file extention must be the same.
	'''
	# opens the xml file, parses the XML and counts number of times xml file has the exon tag
	tree = ET.parse(xmlfilename)
	root = tree.getroot()
	xmlExonCount = 0
	fastaExonCount = 0
        for element in tree.iter():
		if element.tag == "exon" and "label" in element.attrib:
			xmlExonCount += 1
			######## Started mamtching exon names- unfinished...
			'''
			for subelement in element:
				if "t" not in subelement.attrib["coord_system"] and "p" not in subelement.attrib["coord_system"]:
					print subelement.attrib["coord_system"]
			'''

	
	#Parse FASTA file and counts the number of headers
	fastafile = open(fastafilename)	
	for line in fastafile:
		if line[0:1] == '>': #CAUTION: Assumes each exon has a header and that this is the only header
			fastaExonCount += 1
	assert xmlExonCount == fastaExonCount, 'Output number of exons does not match number expected from input file'
	return 'Number of exons in input and output file match. Yay!'

compExonCount = _test_2(argv[1], argv[2])
print compExonCount
