import xml.etree.ElementTree as ET
from sys import argv

'''
Locus Reference Genomic (LRG) file simple exon parser.
------------------------------------------------------

Extracts the exonic sequences defined in the primary transcript of 
an LRG file defined by the user. Currently very basic, but has plenty
of scope for future expansion. Should handle pretty much any case,
including incorrect or malformed LRG, with basic sanity checking for 
exonic coordinates.

Usage: python lrgparser.py <input_file>

'''

def lrg_parse(filename):
	'''
	Opens the LRG file and parses the XML using etree.
	Only accepts valid LRG version 1.8 files.

	Inputs : filename - a valid LRG file.
	
	Outputs : tree - an etree parsed XML tree.
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

def lrg_sequence(tree):
	'''
	Extracts the genomic sequence from the LRG file.
	
	Inputs : tree - an etree parsed XML tree.
	
	Outputs : gsequence - single line string containing the genomic 
		 	      sequence of the LRG gene.
	'''
	# results list
	seq_max_len = 0
	gsequence = ""

	for element in tree.iter():
		# check the sequences, track the longest sequence seen and 
		# return the longest as this will be the genomic sequence
		if element.tag == "sequence":
			if len(element.text) > seq_max_len:
				seq_max_len = len(element.text)
				gsequence = element.text
	assert len(gsequence) > 0, "The pulled sequence's length is 0"	
					
	#Checks that gsequence contains only A, C, T, G.
	nucleotides = ['A','C','T','G']

	for nuc in gsequence:
    		assert nuc in nucleotides, "Mistake- sequence contains characters other than A, T, C or G (note: case sensitive)"
	return gsequence


def lrg_exoncoord(tree):
	'''
	Extracts start and finish coordinates of exons in LRG file
	
	Inputs : tree - an etree parsed XML tree.
	
	Outputs : exons - tuple (start_coordinates, end_coordinates)
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
	
	Inputs : sequence - The genomic sequence of the gene extracted by lrg_sequence()
		 coords - List of exons, defined by start and finish coordinates.
		 	  From lrg_exoncoord().
	Outputs : exons - list of tuple(exon details, exon sequence)
	'''
	exons = []
	for exon in range(0, len(coords)):
		start, end = coords[exon]
		start = int(start)
		end = int(end)
		assert end <= len(sequence), "Co-ordinates lie outside of the range of the sequence"
		info = "exon%d|start: %d|end: %d" % (exon+1, start, end)
		slicesequence = sequence[start-1: end]
		exonSeq = sequence[start-1: end]
		# exon name could be taken directly from file to account for eg exon 1b.
		# start must be -1 for indexing, end is ok as the slice locations are between positions
		assert len(exonSeq) > 0, "Exon is not long enough, it has fewer than 1 nucleotide"		
		exon = info, slicesequence
		exons.append(exon)
	
	return exons
	
def get_gene_info(tree):
	'''
	Looks through the xml tree to find the details of the gene
	
	Inputs : tree - an etree parsed XML tree.
	
	Outputs : tuple (accnumber - Gene accession number,
			LRGid - LRG gene ID number,
			gname - Name of gene from LRG file)
			   
	'''

	# default values in case nothing is found, so the rest of the program will work
	accnumber = "Accession_Number_Not_Found"
	LRGid = "LRG_ID_Not_Found"
	gname = "Gene_Name_Not_Found"

	# get the key details from the xml
	# NOTE: if multiples are found, this will keep the last one
	for node in tree.iter('sequence_source'):
		accnumber = node.text
	for node in tree.iter('id'):
		LRGid = node.text
	for node in tree.iter('lrg_locus'):
		gname = node.text

	assert accnumber != "", "Accession number has no assigned value"
	assert LRGid != "", "LRG ID has no assigned value"
	assert gname != "", "Gene name has no assigned value"

	return accnumber, LRGid, gname

def fasta_output(exons, accession, outfile):
	'''
	Writes the list of exons to a fasta file.
	
	Inputs : exons - list of header/sequence tuples for each exon of the gene
		accession - accession number of the gene
		outfile - name of the file to write to
	
	Outputs : writes to <outfile>.fa 
	'''

	try: 
		out = open(outfile, "w")
	except:
		print "could not open output file"

	for exon in exons:
		header, sequence = exon
		###########################################################
		# This bit adds the accession number to the start of the 
		# FASTA header. I would prefer to do this in sequence_slicer,
		# as future work
		#
		out.write(">")
		out.write(accession)
		###########################################################
		out.write(header)
		out.write("\n")

		# write the sequence with a newline every 80 characters,
		# for readability and also (i think) to meet FASTA standard
		# there is probably no reason for this not to be hard coded
		#
		# CHECK THE FULL LENGTH EXON IS PRINTING
		#

		for i in range(1, len(sequence)):
			if i > 1 and i % 80 == 0:
				out.write(sequence[i])
				out.write("\n")
			else:
				out.write(sequence[i])
		# add an empty line between exons, for neatness
		out.write("\n\n")

def run_parser(infile):
	'''
	Groups commands into a single function, purely for neatness.
	Plenty of stuff here that would change if we added more options,
	e.g. custom output filename, flanking intron sequence, etc.
	'''
	tree = lrg_parse(infile)
	gsequence = lrg_sequence(tree) 
	exons = lrg_exoncoord(tree)
	exon_sequences = sequence_slicer(gsequence, exons)
	accession, lrgid, gname = get_gene_info(tree)
	out = lrgid + ".fa"
	fasta_output(exon_sequences, accession, out)

# Get the first argument from argv as this should be the input filename
# Not currently a very well handled system, but would use argparse or
# similar if using more command line options

if len(argv) != 2:
	print "Usage: python lrgparser.py <input_file>"
else:
	infile = argv[1]
	run_parser(infile)
