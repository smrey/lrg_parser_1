import xml.etree.ElementTree as ET
from sys import argv

def lrg_parse(filename):
	'''
	Put some documentation here
	'''
	# opens the file and parses the XML
	tree = ET.parse(filename)
	root = tree.getroot()

	###################################
	# Iterate through tree and look for exon tags, selecting only those with "label"
	# Each exon label contains 3 sets of start/finish coordinates. We want only the 
	# coordinates for the genomic sequence, so exclude any from transcript or protein
	# so we exclude any with "t" or "p" in the coord_system tag.
	###################################

	# results list
	exons = []
	seq_max_len = 0
	gsequence = ""

	for element in tree.iter():
		# get the start and finish coordinates for the exons
		if element.tag == "exon" and "label" in element.attrib:
			for subelement in element:
				if "t" not in subelement.attrib["coord_system"] and "p" not in subelement.attrib["coord_system"]:
					coords = int(subelement.attrib["start"]), int(subelement.attrib["end"])
					exons.append(coords)
		# check the sequences, track the longest sequence seen and return the longest as this will be the genomic sequence
		if element.tag == "sequence":
			if len(element.text) > seq_max_len:
				seq_max_len = len(element.text)
				gsequence = element.text

	return gsequence, exons

def sequence_slicer(sequence, coords):
	'''
	put some documentation here
	'''
	for exon in range(0, len(coords)):
		
		start, end = coords[exon]
		start = int(start)
		end = int(end)
		print ">exon %d start: %d, end: %d" % (exon, start, end)
		# start must be -1 for indexing, end is ok as the slice locations are between positions
		print sequence[start-1: end]

gsequence, exons = lrg_parse(argv[1])
sequence_slicer(gsequence, exons)
