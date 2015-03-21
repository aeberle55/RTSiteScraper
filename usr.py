class user:
	"""
	Class designed to store data concerning users of the Roosterteeth site
	"""
	
	def __init__(self, username, uid, gender, numFriends, karma, signedUp, R_FRIENDS=None):
		"""
		@param username: Name of the user
		@param uid: User ID of the user
		@param gender: Gender of the user; expect male, female, or Not Specified
		@param numFriends: Number of R_FRIENDS the user has
		@param karma: Karma level of the user
		@param signedUp: Signup date of the user
		@param R_FRIENDS: List of user's R_FRIENDS in string form
		@note: All parameters are in string form
		"""
		self.username = username
		self.uid = uid
		self.gender = gender
		self.numFriends = numFriends
		self.karma = karma
		self.signedUp = signedUp
		if R_FRIENDS != None:
			self.friends = set(R_FRIENDS)
		else:
			self.friends = set()

	def __eq__(self, other):
		"""
		Overloaded equivilance to test for UID being the same
		"""
		if isinstance(other, self.__class__):
			return other.uid == self.uid
		else:
			return False

	def __ne__(self, other):
		"""
		Overloaded not equivilance
		"""
		return not self.__eq__(other)
	
	def __hash__(self):
		"""
		Overloaded hash function to take into account equivilance based on UID
		"""
		return hash(self.uid)

	def addFriend(self, f):
		"""
		Adds a friend to the the urer's R_FRIENDS list
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
		"""
		Accessor for numFriends
		@return: Number of R_FRIENDS in string form
		"""
		return self.numFriends

	def getFriendsList(self):
		"""
		Accessor method for R_FRIENDS list
		@return: A list of strings containing the usernames of all R_FRIENDS
		"""
		return self.friends
	
	def getSignUp(self):
		"""
		Accessor method for sign up date
		 @return: Date of sign up in dd/mm/yy string form
		"""
		return self.signedUp
	
	def getYear(self):
		"""
		Returns the year the user signed up, or 2015 if not available
		@return: Last two digits of sign up year in integer form
		@note: This will break in 85 years or so. Patch by then.
		"""
		if self.signedUp == None:
			return 15
		return int(self.signedUp[-2:])
	
	def getKarma(self):
		"""
		Accessor method for karma level
		@return: Karma level in integer format
		"""
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
