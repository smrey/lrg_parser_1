#Is the sequence the genomic sequence, i.e. is it the longest seqeunce available
#is the sequence of zero length...?

#Import file
##TO DO
gsequence = 'AGCTAG2TCGATCT'
sequencesList = []

# opens the file and parses the XML
tree = ET.parse(filename)
root = tree.getroot()

for element in tree.iter():
    if element.tag == "sequence":
        sequencesList.append(element.attrib) ##Could try nesting len in here
LongestSeq = max(sequencesList) ##May need to be len(each element)
assert LongestSeq == gsequence, "The pulled sequence is not the longest"
assert len(gsequence) > 0, "The pulled sequence's length is 0" ##Should we set a higher limit for what we think is too small for a genomic sequence??
    
        
        
        
        
        
    if len(element.text) > seq_max_len:
		seq_max_len = len(element.text)
			gsequence = element.text