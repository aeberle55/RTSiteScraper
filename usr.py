class user:
	"""
	Class designed to store data concerning users of the Roosterteeth site
	"""
	
	def __init__(self, username, uid, gender, numFriends, karma, signedUp, friends=None):
		"""
		@param username: Name of the user
		@param uid: User ID of the user
		@param gender: Gender of the user; expect male, female, or Not Specified
		@param numFriends: Number of friends the user has
		@param karma: Karma level of the user
		@param signedUp: Signup date of the user
		@param friends: List of user's friends in string form
		@note: All parameters are in string form
		"""
		self.username = username
		self.uid = uid
		self.gender = gender
		self.numFriends = numFriends
		self.karma = karma
		self.signedUp = signedUp
		if friends != None:
			self.friends = set(friends)
		else:
			self.friends = set()	#Create set

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return other.uid == self.uid
		else:
			return False

	def __ne__(self, other):
		return not self.__eq__(other)
	
	def __hash__(self):
		return hash(self.uid)

	def addFriend(self, f):
		"""
		Adds a friend to the the urer's friends list
		@param f: String containing the friend's name
		"""
		self.friends.append(f)

	def getURL(self):
		"""
		Returns the URL of this user's member page
		@return: A string formatted URL string
		"""
		return "http://roosterteeth.com/" + self.username

	def getName(self):
		"""
		Accessor for this user's name
		@return: The username in string form
		"""
		return self.username

	def getUID(self):
		"""
		Accessor for UID
		@return: String of user's UID
		"""
		return self.uid

	def getNumFriends(self):
		return self.numFriends

	def getFriendsList(self):
		return self.friends
	
	def getSignUp(self):
		return self.signedUp
	
	def getYear(self):
		if self.signedUp == None:
			return 15
		return int(self.signedUp[-2:])
	
	def getKarma(self):
		return int(self.karma)
	
	def printData(self, printAll = False):
		"""
		Prints user data of the User
		@param printAll: if True, prints the data from the function; Default False
		@return: A string with the user data
		"""
		output = ("Name " + self.username + ", UID: " + self.uid + ", Gender: " + self.gender + ", Friends: " + self.numFriends + 
			", Karma: " + self.karma + ", Sign up Date: " + self.signedUp)
		if printAll:
			print output
		return output
