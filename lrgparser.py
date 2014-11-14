import xml.etree.ElementTree as ET
from sys import argv

def lrg_parse(filename):
	'''
	this function opens the xml file and gets the tree and root
	'''
	# opens the file and parses the XML
	
	try: #test to see if the file is an xml, the file is an lrg and the version of the lrg is 1.8
		tree = ET.parse(filename)
		root = tree.getroot()
		assert root.tag == 'lrg', "Not an lrg file"
		assert root.attrib == {'schema_version': '1.8'}, "Incorrect schema version. This tool only supports version 1.8"
	except IOError:
		print "Error: Not an xml file or ElementTree not installed"
	return tree


###################################
# Iterate through tree and look for exon tags, selecting only those with "label"
# Each exon label contains 3 sets of start/finish coordinates. We want only the 
# coordinates for the genomic sequence, so exclude any from transcript or protein
# so we exclude any with "t" or "p" in the coord_system tag.
###################################

def lrg_sequence(tree):
	'''
	to get the genomic sequence
	'''
	# results list
	seq_max_len = 0
	gsequence = ""

	for element in tree.iter():
		# check the sequences, track the longest sequence seen and return the longest as this will be the genomic sequence
		if element.tag == "sequence":
			if len(element.text) > seq_max_len:
				seq_max_len = len(element.text)
				gsequence = element.text
					
	#Checks that gsequence contains only A, C, T, G.
	nucleotides = ['A','C','T','G']

	for nuc in gsequence:
    		assert nuc in nucleotides, "Mistake- sequence contains characters other than A, T, C or G"

	return gsequence


def lrg_exoncoord(tree):
	'''
	to get the exon coordinates
	'''
	exons = []

	for element in tree.iter():
	# get the start and finish coordinates for the exons
		if element.tag == "exon" and "label" in element.attrib:
			for subelement in element:
				if "t" not in subelement.attrib["coord_system"] and "p" not in subelement.attrib["coord_system"]:
					#Checking input coordinates are numerical characters that can be converted to integers					
					try:					
						coords = int(subelement.attrib["start"]), int(subelement.attrib["end"])
					except TypeError:
						print "input coordinates are not integers"	
				
					exons.append(coords)	
	
	assert exons != [], "List of exon co-ordinates is empty. No exon co-ordinates stored."
	for tup in exons:
		try:
			assert len(tup) == 2, "Error: Missing co-ordinate in list of exon co-ordinates"
			assert tup[0] < tup[1], "Second co-ordinate of co-ordinate pair bigger than first"
		except TypeError:
			print "Error: Missing co-ordinate in list of exon co-ordinates"	

	for tupInd in range(len(exons)-1):
		assert exons[tupInd][1] < exons[tupInd+1][0], "Exon n starts before the end of exon n-1"

	return exons

def sequence_slicer(sequence, coords):
	'''
	This function takes the sequence and coordinates from lrg_parse()
	These are used to output a FASTA formatted file that contains the sections of 
	sequence defined by the coordinates.
	'''
	for exon in range(0, len(coords)):
	
		start, end = coords[exon]
		start = int(start)
		end = int(end)
		print ">exon %d start: %d, end: %d" % (exon+1, start, end)
		#exon name could be taken directly from file to account for eg exon 1b.
		# start must be -1 for indexing, end is ok as the slice locations are between positions
		print sequence[start-1: end]

tree = lrg_parse(argv[1])
gsequence = lrg_sequence(tree)
exons = lrg_exoncoord(tree)
sequence_slicer(gsequence, exons)

#lrg_parser(filename, upstream = 0, downstream = 0)
