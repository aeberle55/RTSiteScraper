import re
import urllib2
import cPickle as pickle

storageFile = "CCList.p"

def getCCFromNet():
    """
        Accesses the internet to get a list of all cast and crew
        @return: A list of names in string form of all cast and crew
        @todo: Write the list to a file and access it rather than the internet
    """
    rx = "<li> <a href=\"/wiki/.+\" title=\".+\">.+</a>.+\[(.+)\]"
    r = re.compile(rx)
    req = urllib2.Request("http://roosterteeth.wikia.com/wiki/Cast_%26_Crew", headers={'User-Agent' : "Magic Browser"})
    cc = urllib2.urlopen(req).read()
    namesT = r.findall(cc)
    names = []
    for name in namesT:
        names.append(name.lower())
    return names
"""
Main Function
"""
if __name__ == '__main__':
    try:
        lst = getCCFromNet();
        pickle.dump(lst, open(storageFile, "wb"))
        print "Cast and Crew list successfully created and stored"
    except urllib2.URLError as e:
        print "Error in HTTP request. Aborting."
    except pickle.PickleError as e:
        print "Error storing Cast and Crew list. Aborting."