"""Helper functions for parsing xml using lxml"""
def search(xmlroot, string):
    """Search xmlroot for string and return the text value"""
    return xmlroot.find('.//{%s}%s' % (xmlroot.nsmap[None], string)).text

def nodestring(xmlroot, string):
    """convert string into a tag that lxml can search in xml tree"""
    return '{%s}%s' % (xmlroot.nsmap[None], string)

def findstring(xmlroot, string):
    """Return the search string to be used by lxml .find()"""
    return './/{%s}%s' % (xmlroot.nsmap[None], string)

def findvalue(xmlroot, string):
    """Return text from value in text node"""
    node = xmlroot.find(findstring(xmlroot, string))
    return node.find(findstring(node, 'Value')).text

def findhasvalue(xmlroot, string):
    """Return text from HasValue"""
    node = xmlroot.find(findstring(xmlroot, string))
    return node.find(findstring(node,  'HasValue')).text

def hasNode(xmlroot,  string):
    """Return True if xml has node otherwise False"""
    if xmlroot.find('.//{%s}%s' % (xmlroot.nsmap[None], string)) != None:
        return True
    else:
        return False
