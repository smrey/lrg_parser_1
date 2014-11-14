import xml.etree.ElementTree as ET
from sys import argv
'''
lrgparser
author: Ben Sanders

usage: python lrgparser <LRG filename>

Reads a specified LRG file and extracts exonic sequences. Returns as a FASTA file.

Potential options:
	-o, --outfile	: set the output filename
	-x, --exon	: gives a specific exon only


'''
def lrg_parse(filename):
	'''
	Function: lrg_parse(filename)
	
	Input	: LRG file to open (name or path?)
	Output	: FASTA file containing exonic sequences 
	
	'''
	# opens the file and parses the XML
	tree = ET.parse(filename)
	root = tree.getroot()

	# results list
	exons = []
	seq_max_len = 0
	gsequence = ""

	for element in tree.iter():
		# check the sequences, track the longest sequence seen and return the longest as this will be the genomic sequence
		if element.tag == "sequence":
			if len(element.text) > seq_max_len:
				seq_max_len = len(element.text)
				gsequence = element.text
		# get the start and finish coordinates for the exons
		if element.tag == "exon" and "label" in element.attrib:
			for subelement in element:
				if "t" not in subelement.attrib["coord_system"] and "p" not in subelement.attrib["coord_system"]:
					coords = int(subelement.attrib["start"]), int(subelement.attrib["end"])
					exons.append(coords)

	return gsequence, exons

def sequence_slicer(sequence, coords):
	'''
	function: sequence_slicer(sequence, coords)

	Input	: A genomic sequence and a list of coordinates definig start and end points of exons.
		  These are derived from the given LRG file by the lrg_parse function
	Output	: A list containing (fasta_header, sequence) tuples for each exon
	'''
	exons = []
	for exon in range(0, len(coords)):
		
		start, end = coords[exon]
		start = int(start)
		end = int(end)
		info = ">exon %d start: %d, end: %d" % (exon+1, start, end)
		# start must be -1 for indexing, end is ok as the slice locations are between positions
		exon = info , sequence[start-1: end]
		exons.append(exon)
	return exons

gsequence, exons = lrg_parse(argv[1])
exon_list = sequence_slicer(gsequence, exons)
print exon_list[5]
