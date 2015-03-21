import re
import urllib2
from collections import deque
import math
import usr
import cPickle as pickle
import time

url = "http://roosterteeth.com/"																#Site to rip from
PKL_FILE = "uList.p"																			#File to store data to
LOG_FILE = "log.txt"																			#Log file to store data
queue = deque(["Ray"])																			#Queue containing initial seed user(s)
R_GENDER = ("<R_GENDER property=\"profile:gender\" content=\"(.+)\"")							#Regex for gender
R_FRIENDS = ("(\d+) Friend[s]*</a>")															#Regex for number of R_FRIENDS
R_UID = ("href=\'/members/R_FRIENDS\.php\?uid=(\d+)\'")											#Regex for UID
R_KARMA = ("<div id=\'karmaProgressBarBar\' class=\'progressBarBar\' style=.+>\+(\d+)</div>")	#Regex for karma level
R_SIGNUP = ("<span class=\'updateWhen\' data-on=.+</span> \((.+)\)")							#Regex fopr signup date
THRESHOLD = 500																					#Minimum number of R_FRIENDS to be a node
MAX_PROCESS = 100000																			#Maximum Number of users to process			
numError = 0																					#Number of errors detected from network
processed = set(queue)																		#Users that have already been processed by the main loop
userList = []																					#List of user objects to be pickled
numProcessed = 0																				#Total number of users processed by the program

f = open(LOG_FILE, "w")

def logToFile(out):
	"""
	Logs and prints a given string
	@param out: String to store and print
	"""
	f.write(out + "\n")
	print out

def ripPage(urlName):
	"""
	Return the html data at a given page
	@param urlName: the URL formatted string to rip
	@return: HTML page in string form
	"""
	req = urllib2.Request(urlName, headers={'User-Agent' : "Magic Browser"})
	return urllib2.urlopen(req).read()

def getCC():
	rx = "class='avatarA' data-uid='\d+' href='/(.+)'><img data-uid='\d+'"
	r = re.compile(rx)
	cc = ripPage("http://roosterteeth.com/staff/")
	names = r.findall(cc)
	return names
	
	
def getFriends(userID, num):
	"""
	Gets a list of all R_FRIENDS of a given user, and adds them to the queue if needed
	@param userID: a string or integer containing the uid of the user in question
	@param num: an integer containing the number of R_FRIENDS the user has
	@return: a list of all R_FRIENDS in string form
	"""
	rx = "class='avatarA' data-uid='\d+' href='/(.+)'><img data-uid='\d+'"
	r = re.compile(rx)
	numpages = int(math.ceil(num/48)) 
	friendNames = []
	for x in range(1,numpages+1):
		pg = ripPage(url + "members/R_FRIENDS.php?uid=" + str(userID) + "&page=" + str(x))
		names = r.findall(pg)
		for user in names:
			if not user in friendNames:
				friendNames.append(user)		#Want to list all users
				if not (user in processed):
					queue.append(user)			#Enqueue users we have not seen yet
					processed.add(user)
	return friendNames

def getStats(info):
	"""
	Finds the number of R_FRIENDS, gender, and uid of a user
	@param info: String formatted HTML page to search for info in
	@return: A tupple with the UID, Number of Friends, and Gender of the user in string form
	@note: Default return values are 0, Not Specified, and an empty string, in order
	"""
	regex = re.search(R_FRIENDS, info)
	num = "0"
	gen = "Not Specified"
	uid = ""
	karma = ""
	signup = ""
	if regex:
		num = regex.group(1)
	regex = re.search(R_GENDER, info)
	if regex:
		gen = regex.group(1)
	regex = re.search(R_UID, info)
	if regex:
		uid = regex.group(1)
	regex = re.search(R_KARMA, info)
	if regex:
		karma = regex.group(1)
	regex = re.search(R_SIGNUP, info)
	if regex:
		signup = regex.group(1)
	return (uid, num, gen, karma, signup)	
"""
Main Function
"""
if __name__ == '__main__':
	while len(queue) > 0:
		tempName = queue.popleft()
		try:
			logToFile(time.strftime("%H:%M:%S") + ": Ripping " + tempName)
			page = ripPage(url+tempName)
			(uid, numFriends, gender, karma, signup) = getStats(page)
			if int(numFriends) > THRESHOLD: #and not tempName in castAndCrew:
				logToFile(time.strftime("%H:%M:%S") + ": " + tempName + " has " + numFriends + " R_FRIENDS, so is being added to the file")
				fList = getFriends(uid, int(numFriends))
				logToFile(time.strftime("%H:%M:%S") + ": " + tempName + "'s R_FRIENDS added to the file")
				u = usr.user(tempName, uid, gender, numFriends, karma, signup, R_FRIENDS=fList[:])
				userList.append(u)
			numProcessed += 1
			numError = 0
			if numProcessed % 10 == 0:
				logToFile(time.strftime("%H:%M:%S") + ": " + str(numProcessed) + " users processed")
			if numProcessed >= 100000:
				break;
		except urllib2.URLError as e:
			logToFile(time.strftime("%H:%M:%S") + ": Error")
			if numError < 5:
				logToFile(time.strftime("%H:%M:%S") + ": Skipping " + tempName)
				queue.appendleft(tempName)	#Add the aborted name back to thge queue
			numError+=1
			if numError > 60:
				logToFile(time.strftime("%H:%M:%S") + "Internet Failure. Aborting.")
				break;
			logToFile(time.strftime("%H:%M:%S") + ": " + str(5-numError)+" Attempts remaining\n")
			time.sleep(10)		
	pickle.dump(userList, open(PKL_FILE, "wb"))
	logToFile(time.strftime("%H:%M:%S") + ": Data Collection Complete. Unprocessed Users: " + str(len(queue)))
	logToFile(time.strftime("%H:%M:%S") + ": Printing user list:")
	for u in userList:
		logToFile(u.printData())
	f.close()