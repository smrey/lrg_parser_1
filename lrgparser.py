import xml.etree.ElementTree as ET

# opens the file and parses the XML
tree = ET.parse("LRG_292.xml")
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

print seq_max_len, len(gsequence)

