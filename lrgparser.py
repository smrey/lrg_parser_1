import xml.etree.ElementTree as ET
from sys import argv

def lrg_parse(filename):
	'''
	this function opens the xml file and gets the tree and root
	'''
	# opens the file and parses the XML
	tree = ET.parse(filename)
	root = tree.getroot()
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
					coords = int(subelement.attrib["start"]), int(subelement.attrib["end"])
					exons.append(coords)
	return exons

def sequence_slicer(sequence, coords):
	'''
	This function takes the sequence and coordinates from lrg_parse()
	These are used to output a FASTA formatted file that contains the sections of 
	sequence defined by the coordinates.
	'''
	exons = []
	for exon in range(0, len(coords)):
		
		start, end = coords[exon]
		start = int(start)
		end = int(end)
		info = "exon %d start: %d, end: %d" % (exon+1, start, end)
		# start must be -1 for indexing, end is ok as the slice locations are between positions
		exon = info, sequence[start-1: end]
		exons.append(exon)
	return exons

def fasta_output(exons, outfile="lrgparser_output"):
	'''
	Writes the list of exons to a fasta file
	'''
	try: 
		out = open(outfile, "w")
	except:
		print "could not open output file"

	for exon in exons:
		header, sequence = exon
		out.write(header)
		# write the sequence with a newline every 80 characters,
		# for readability and also (i think) to meet FASTA standard
		# there is probably no reason for this not to be hard coded
		for i in range(0, len(sequence)):
			if i % 80 == 0:
				out.write(sequence[i])
				out.write("\n")
			else:
				out.write(sequence[i])
		# add an empty line between exons
		out.write("\n\n")

# Ideally the argv options should be properly parsed, this may balls up with the wrong number of inputs...
tree = lrg_parse(argv[1])
gsequence = lrg_sequence(tree)
exons = lrg_exoncoord(tree)
exon_sequences = sequence_slicer(gsequence, exons)
if len(argv) > 2:
	fasta_output(exon_sequences, argv[2])
else:
	fasta_output(exon_sequences)
