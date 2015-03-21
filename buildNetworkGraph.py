import usr
import cPickle as pickle
import networkx as nx
import matplotlib.pyplot as plt
from cAndC import getCCFromNet
import math
import urllib2
import sys

NODE_SIZE = "date"       #Factor to decide node size; Options are 'friends', 'date', 'karma' and 'none'
FILTER_BY = "friends"          #Factor to decide what users to filter; Options are 'friends', 'date', 'karma', 'none'
MIN_YEAR = 0                #Earliest year a user can sign up by before being filtered by date, inclusive
MAX_YEAR = 10               #Latest year a user can sign up by before being filtered by date, inclusive
MIN_FRIENDS = 700           #Minimum number of friends a user can have when being filtered by friends, inclusive
MAX_FRIENDS = None           #Maximum number of friends a user can have when being filtered by friends, inclusive
MIN_KARMA = 50               #Minimum karma when filtering by karma, inclusive
MAX_KARMA = 99              #Maximum karma when filtering by karma, inclusive
FONT_SIZE = 14              #Font size of username
K_VAL = None                #Spring constant for spring formatting of positions
NUM_ITERATIONS = 100         #Number of iterations run by the position generator
PKL_FILE = "uList.p"        #Location of user data in pickle file
CC_LIST = "CCList.p"        #List of all cast and crew, in cpickle format
IMG_FILE = "temp.png"       #Location to store image
HIST_FILE = "histTemp.png"  #Location of histogram image
FIG_SIZE = 90              #Height and width of image in hundreds of pixels
INCLUDE_CC = 1              #Status of Cast and Crew; 0->Exclude, 1->Treat as User, 2->Never Filter
GET_HIST = True             #Generate a Histogram of node degrees
LOG_LOG = False             #Make the histogram a Lgo-Log scale

def getCC():
    """
        Accesses the internet to get a list of all cast and crew
        @return: A list of names in string form of all cast and crew
    """
    try:
        names = pickle.load(open(CC_LIST, "rb"))
    except IOError:
        print "No file found at " + CC_LIST
        print "Getting names from internet"
        try:
            names = getCCFromNet()
            print "List of names found. Pickling"
            pickle.dump(names, open(CC_LIST, "wb"))
        except urllib2.HTTPError:
            print "Network Error. Failed to get list of Cast and Crew"
            return []
        except pickle.PickleError:
            print "Unable to store Cast and Crew Names at" + CC_LIST
            return names
    return names 

def getEdgeColor(u1, u2, G):
    """
        Returns the propper color of the edge between two nodes
        @param u1: First user object
        @param u2: Second user object
        @param G: The related Graph
        @return: Returns a color in string form based on the current node colors;
            If the nodes are the same color, return that color; 
            If only one is staff, return purple;
            If they are otherwise different colors, return green
        @note: Node colors must be set before running this function
    """
    if G.colors[u1] == G.colors[u2]:
        return G.colors[u1]
    if G.colors[u1] == 'red' or G.colors[u2] == 'red':
        return 'purple'
    return 'green'

def getWeight(u1,u2, CCList):
    """
        Returns the edge weight between two nodes based on C&C status
        @param u1: First user object
        @param u2: Second user object
        @param CCList: List of all members of Cast & Crew
        @return: Weight in integer form;
        If both are C&C, return 5;
        If one is C&C, return 3;
        Else, return 1
    """
    if u1.lower() in CCList and u2.lower() in CCList:
        return 5
    if u1.lower() in CCList or u2.lower() in CCList:
        return 3
    return 1

def getNodeSize(user):
    """
        Returns the size of a node based on the user object and a pre-set specifier
        @param user: The user object
        @return: Based on the value of NODE_SIZE string;
        If "karma", the size is based on user karma level;
        If "date", the size is based on how old the account is;
        If "friends", the size is based on how many friends the user has
        Else, returns 5000
    """
    if NODE_SIZE.lower() == "karma":
        return 50*math.pow(int(u.karma)+15,1.3)
    if NODE_SIZE == "date":
        if user.getSignUp() == None:
            return 1000
        year = 16-user.getYear()
        return 10000*math.log10(year)
    if NODE_SIZE == "friends":
        num = int(u.getNumFriends())
        if num > 2000:
            num = 1175 + 250*math.log10(num)    #Prevents huge friend numbers from dominating
        return 5*num
    return 5000

def buildHistogram(G, skipped=1):
    """
    Builds a histogram of users based on their degree (number of edges)
    @param G: Graph of users and edges
    @param skipped: Decreace density of graph. 1-> None skipped, 2-> Every other graphed, 3-> every third...
    """
    plt.clf()
    plt.figure(figsize=(20,10))
    deg_seq = sorted(nx.degree(G).values(), reverse=True)[::skipped]
    if LOG_LOG:
        plt.loglog(deg_seq, 'b-', marker='o') 
    else:
        plt.plot(deg_seq, 'b-', marker='o')
    plt.title("Degree Plot")
    plt.ylabel("Degree")
    plt.xlabel("Rank")
    plt.savefig(HIST_FILE)

def drawGraph(G):
    plt.figure(figsize=(FIG_SIZE,FIG_SIZE))
    edges,colors = zip(*nx.get_edge_attributes(G, 'color').items())
    edges,weights = zip(*nx.get_edge_attributes(G,'weight').items())
    edges,arrows = zip(*nx.get_edge_attributes(G,'arrow').items())
    G.pos = nx.spring_layout(G, k=K_VAL, weight = 'weights', iterations=NUM_ITERATIONS)
    nx.draw_networkx_nodes(G, G.pos, node_size=[G.nodeSize[v] for v in G], node_color=[G.colors[v] for v in G])
    nx.draw_networkx_edges(G, pos=G.pos, edgelist=edges, width=weights, edge_color=colors, arrows=arrows)
    nx.draw_networkx_labels(G, pos=G.pos, font_size=FONT_SIZE)
    plt.savefig(IMG_FILE)
    
def getNodeColor(user, CCList):
    """
        Returns the color of the node
        @param user: The user object
        @param CCList: List of C&C names
        @return: Color based on gender/c&c status;
        C&C are red;
        Males are blue;
        Females are pink;
        N/A are grey
    """
    n = user.getName()
    if n.lower() in CCList:
        return 'red'
    if u.gender == "male":
        return 'blue'
    if u.gender == "female":
        return 'pink'
    return 'grey'

def filterUser(u):
    """
        Returns if a user should be included in the graph based on settings
        @param user: User object
        @return: Boolean that is true if they should be added, false otherwise;
        Cast and Crew are filtered based on INCLUDE_CC:
            If 0, they are always excluded
            If 1, they are filtered as normal users
            If 2, they are always included
        Normal users are filtered based on FILTER_BY:
            If "none", no users are filtered;
            If "friends", filtered by number of friends;
            If "date", filtered by sign up year
            If "karma", filtered by karma level
    """
    if u.getName().lower() in CCList:
        if INCLUDE_CC is 0:     #Exclude Cast and Crew
            return False
        elif INCLUDE_CC is 2:   #Always include Cast and Crew
            return True;
    if FILTER_BY == "none":
        return True
    if FILTER_BY == "friends":
        return MIN_FRIENDS <= int(u.numFriends) and MAX_FRIENDS is None or (MIN_FRIENDS<=int(u.numFriends)<=MAX_FRIENDS)
    if FILTER_BY == "date":
        return MIN_YEAR<=u.getYear()<=MAX_YEAR
    if FILTER_BY == "karma":
        k = u.getKarma()
        return MIN_KARMA<=k<=MAX_KARMA
    return False

"""
Main Function
"""
if __name__ == '__main__':
    try:
        uList = set(pickle.load(open(PKL_FILE, "rb")))
    except pickle.UnpicklingError:
        print "Failed to open file " + PKL_FILE +"\nAborting."
        sys.exit(-1)
    usersToMap = {}
    G = nx.Graph()
    G.nodeSize = {}
    G.colors = {}
    CCList = getCC()
    
    
    for u in uList:
        if filterUser(u):
            n = u.getName()
            G.nodeSize[n] = getNodeSize(u)
            usersToMap[n] = u
            G.add_node(n)
            G.colors[n] = getNodeColor(u, CCList)
    del u
    keys = usersToMap.keys()
    for key in keys:
        flist = usersToMap[key].getFriendsList()
        for other in keys:
            if other in flist:
                G.add_edge(other, key, color=getEdgeColor(other, key, G), weight=getWeight(other,key, CCList), arrow=True)
    
    #drawGraph(G) 
    if GET_HIST:
        buildHistogram(G, skipped=1)