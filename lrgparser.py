from sys import argv

'''
LRG file parser

Usage: python lrgparser <LRG_filename>

Opens the given file, checks if file is likely to be an LRG, returns the open file
'''
def open_LRG(filename):
    '''
    Attempts to open the given filename

    Returns the open file pointer
    '''
    try:
        f = open(filename, "r")
    except:
        print "Error: Could not open file or file does not exist"

    # check that the file is an LRG file by looking for the schema def tag
    isvalid = False
    # only reads the first 10 lines, may cause problems but simple for now
    for i in range(0, 10):
        line = f.readline()
        if "lrg" in line:
            isvalid = True
    assert isvalid == True, "File does not appear to be an LRG file"

    return f

open_LRG(argv[1])
