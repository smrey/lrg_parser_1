#test to see if the file is an xml, the file is an lrg and the version of the lrg is 1.8
import xml.etree.ElementTree as etree
try:
	lrg = etree.parse('LRG_292.xml')
	lrg_root = lrg.getroot()
	print lrg_root.attrib
	print lrg_root.tag		
	assert lrg_root.tag == 'lrg', "Not an lrg file"
	assert lrg_root.attrib == {'schema_version': '1.8'}, "Incorrect schema version. This tool only supports version 1.8"
except IOError:
	print "Error: Not an xml file or ElementTree not installed"


	

