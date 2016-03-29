import re
import datetime

class Fixture :

	def __init__(self, header, values):

		self.fixture = {}
		self.validScore = True
		self.validShots = True
		self.validOdds = True
		self.validFixture = True
		self.fixtureString = values
	
		try:
			self.fixture['leagueCode'] = self.getString("Div", header, values)
			self.fixture['seasonCode'] = self.extractSeasonCode("Date", header, values)
			self.fixture['homeTeam']   = self.getString("HomeTeam", header, values)
			self.fixture['awayTeam']   = self.getString("AwayTeam", header, values)
			self.fixture['date']       = self.parseDateString("Date", header, values)
		except:
			self.validFixture = False

		try:
			self.fixture['homeFT']   = self.getInt("FTHG", header, values)
			self.fixture['awayFT']   = self.getInt("FTAG", header, values)
			self.fixture['resultFT'] = self.getString("FTR", header, values)
			self.fixture['homeHT']   = self.getInt("HTHG", header, values)
			self.fixture['awayHT']   = self.getInt("HTAG", header, values)
			self.fixture['resultHT'] = self.getString("HTR", header, values)
		except:
			self.fixture['homeFT'] = -1
			self.fixture['awayFT'] = -1
			self.fixture['resultFT'] = -1
			self.fixture['homeHT'] = -1
			self.fixture['awayHT'] = -1
			self.fixture['resultHT'] = -1
			self.validScore = False

		try:
			self.fixture['homeShots'] = self.getInt("HS", header, values)
			self.fixture['awayShots'] = self.getInt("AS", header, values)
			self.fixture['homeShotsTarget'] = self.getInt("HST", header, values)
			self.fixture['awayShotsTarget'] = self.getInt("AST", header, values)
		except:
			self.fixture['homeShots'] = 0
			self.fixture['awayShots'] = 0
			self.fixture['homeShotsTarget'] = 0
			self.fixture['awayShotsTarget'] = 0
			self.validShots = False

		try:
			self.fixture['bestHomeOdds'] = self.findBestHomeOdds(header, values)
			self.fixture['worstHomeOdds'] = self.findWorstHomeOdds(header, values)
			self.fixture['bestAwayOdds'] = self.findBestAwayOdds(header, values)
			self.fixture['worstAwayOdds'] = self.findWorstAwayOdds(header, values)
		except:
			self.fixture['bestHomeOdds'] = 0.0
			self.fixture['worstHomeOdds'] = 0.0
			self.fixture['bestAwayOdds'] = 0.0
			self.fixture['worstAwayOdds'] = 0.0
			self.validOdds = False		

	def isValid(self):
		return self.validFixture

	def toString(self):
		return self.fixtureString

	def hasScore(self):
		return self.validScore

	def hasShots(self):
		return self.validShots

	def hasOdds(self):
		return self.validOdds

	def isComplete(self):
		if self.validFixture and self.validShots and self.validOdds:
			return True
		else:
			return False

	def getString(self, key, header, values):
		try:
			indexPos = header.index(key)
			return values[indexPos].rstrip()
		except:
			raise

	def getInt(self, key, header, values):
		try:
			indexPos = header.index(key)
			intString = values[indexPos]
			regex = re.compile("^[-+]?[0-9]+$")
			if regex.match(intString):
				return int(intString)
			else:
				raise ValueError
		except:
			raise

	def getFloat(self, key, header, values):
		try:
			indexPos = header.index(key)
			floatString = values[indexPos]
			regex = re.compile("[-+]?\d*\.\d+|\d+")
			if regex.match(floatString):
				return float(floatString)
			else:
				raise ValueError
		except:
			raise

	def getOddsFloat(self, key, header, values):
		""" Difference between this and the above function is that 
		    this returns 0.0 if the header value isn't found, and the 
		    getFloat() function returns a ValueError Exception
		"""
		try:
			indexPos = header.index(key)
			floatString = values[indexPos]
			regex = re.compile("[-+]?\d*\.\d+|\d+")
			if regex.match(floatString):
				return float(floatString)
			else:
				return 0.0
		except:
			return 0.0

	def parseDateString(self, key, header, values):
		try:
			indexPos = header.index(key)
			dateValue = values[indexPos]
			regex = re.compile("^[0-9]{2}/[0-9]{2}/[0-9]{2}$")
			if regex.match(dateValue):
				return dateValue
			else:
				raise ValueError
		except:
			raise

	def setLeagueCode(self, leagueCode):
		self.fixture['leagueCode'] = leagueCode

	def setSeasonCode(self, seasonCode):
		self.fixture['seasonCode'] = seasonCode

	def setDate(self, dateValue):
		self.fixture['date'] = dateValue

	def setHomeTeam(self, homeTeam):
		self.fixture['homeTeam'] = homeTeam

	def setAwayTeam(self, awayTeam):
		self.fixture['awayTeam'] = awayTeam

	def setHomeFT(self, homeFT):
		if type(homeFT) is float:
			self.fixture['homeFT'] = homeFT
		else:
			self.fixture['homeFT'] = float(homeFT)

	def setHomeHT(self, homeHT):
		if type(homeHT) is float:
			self.fixture['homeHT'] = homeHT
		else:
			self.fixture['homeHT'] = float(homeHT)

	def setAwayFT(self, awayFT):
		if type(awayFT) is float:
			self.fixture['awayFT'] = awayFT
		else:
			self.fixture['awayFT'] = float(awayFT)

	def setAwayHT(self, awayHT):
		if type(awayHT) is float:
			self.fixture['awayHT'] = awayHT
		else:
			self.fixture['awayHT'] = float(awayHT)

	def setResultFT(self, result):
		self.fixture['resultFT'] = result

	def setResultHT(self, result):
		self.fixture['resultHT'] = result

	def setHomeShots(self, value):
		if type(value) is float:
			self.fixture['homeShots'] = value
		else:
			self.fixture['homeShots'] = float(value)

	def setHomeShotsTarget(self, value):
		if type(value) is float:
			self.fixture['homeShotsTarget'] = value
		else:
			self.fixture['homeShotsTarget'] = float(value)

	def setAwayShots(self, value):
		if type(value) is float:
			self.fixture['awayShots'] = value
		else:
			self.fixture['awayShots'] = float(value)

	def setAwayShotsTarget(self, value):
		if type(value) is float:
			self.fixture['awayShotsTarget'] = value
		else:
			self.fixture['awayShotsTarget'] = float(value)

	def getLeagueCode(self):
		return self.fixture['leagueCode']

	def getSeasonCode(self):
		return self.fixture['seasonCode']

	def getDateString(self):
		return self.fixture['date']

	def getDate(self):
		dateString = self.fixture['date']
		return datetime.datetime.strptime(dateString, '%d/%m/%y')

	def getHomeTeam(self):
		try:
			return self.fixture['homeTeam']
		except KeyError:
			print 'HOME TEAM KEY ERROR'
			

	def getAwayTeam(self):
		return self.fixture['awayTeam']

	def getHomeFT(self):
		return self.fixture['homeFT']

	def getAwayFT(self):
		return self.fixture['awayFT']

	def getResultFT(self):
		return self.fixture['resultFT']

	def getHomeHT(self):
		if self.fixture['homeHT'] is None:
			return 0
		else:
			return self.fixture['homeHT']

	def getAwayHT(self):
		if self.fixture['awayHT'] is None:
			return 0
		else:
			return self.fixture['awayHT']

	def getHomeShots(self):
		if self.fixture['homeShots'] is None:
			return 0
		else:
			return self.fixture['homeShots']

	def getHomeShotsTarget(self):
		if self.fixture['homeShotsTarget'] is None:
			return 0
		else:
			return self.fixture['homeShotsTarget']

	def getAwayShots(self):
		if self.fixture['awayShots'] is None:
			return 0
		else:
			return self.fixture['awayShots']

	def getAwayShotsTarget(self):
		if self.fixture['awayShotsTarget'] is None:
			return 0
		else:
			return self.fixture['awayShotsTarget']

	def getResultHT(self):
		if self.fixture['resultHT'] is None:
			return "D"
		else:
			return self.fixture['resultHT']
		
	def getBestHomeOdds(self):
		return self.fixture['bestHomeOdds']

	def getWorstHomeOdds(self):
		return self.fixture['worstHomeOdds']

	def getBestAwayOdds(self):
		return self.fixture['bestAwayOdds']

	def getWorstAwayOdds(self):
		return self.fixture['worstAwayOdds']
		
	def findBestHomeOdds(self, header, values):
		oddsList = []
		oddsList.append(self.getOddsFloat("B365H", header, values))
		oddsList.append(self.getOddsFloat("BWH", header, values))
		oddsList.append(self.getOddsFloat("IWH", header, values))	
		oddsList.append(self.getOddsFloat("LBH", header, values))
		oddsList.append(self.getOddsFloat("PSH", header, values))
		oddsList.append(self.getOddsFloat("WHH", header, values))
		oddsList.append(self.getOddsFloat("SJH", header, values))
		oddsList.append(self.getOddsFloat("VCH", header, values))

		validList = []
		for element in oddsList:
			if element is not None:
				validList.append(element)
		
		if len(validList) > 0:
			return max(validList)
		else:
			raise ValueError
	
	def findWorstHomeOdds(self, header, values):
		oddsList = []
		oddsList.append(self.getOddsFloat("B365H", header, values))
		oddsList.append(self.getOddsFloat("BWH", header, values))
		oddsList.append(self.getOddsFloat("IWH", header, values))	
		oddsList.append(self.getOddsFloat("LBH", header, values))
		oddsList.append(self.getOddsFloat("PSH", header, values))
		oddsList.append(self.getOddsFloat("WHH", header, values))
		oddsList.append(self.getOddsFloat("SJH", header, values))
		oddsList.append(self.getOddsFloat("VCH", header, values))

		validList = []
		for element in oddsList:
			if element is not None and element > 0.0:
				validList.append(element)
		
		if len(validList) > 0:
			return min(validList)
		else:
			raise ValueError

	def findBestAwayOdds(self, header, values):
		oddsList = []
		oddsList.append(self.getOddsFloat("B365A", header, values))
		oddsList.append(self.getOddsFloat("BWA", header, values))
		oddsList.append(self.getOddsFloat("IWA", header, values))	
		oddsList.append(self.getOddsFloat("LBA", header, values))
		oddsList.append(self.getOddsFloat("PSA", header, values))
		oddsList.append(self.getOddsFloat("WHA", header, values))
		oddsList.append(self.getOddsFloat("SJA", header, values))
		oddsList.append(self.getOddsFloat("VCA", header, values))

		validList = []
		for element in oddsList:
			if element is not None:
				validList.append(element)
		
		if len(validList) > 0:
			return max(validList)
		else:
			raise ValueError
	
	def findWorstAwayOdds(self, header, values):
		oddsList = []
		oddsList.append(self.getOddsFloat("B365A", header, values))
		oddsList.append(self.getOddsFloat("BWA", header, values))
		oddsList.append(self.getOddsFloat("IWA", header, values))	
		oddsList.append(self.getOddsFloat("LBA", header, values))
		oddsList.append(self.getOddsFloat("PSA", header, values))
		oddsList.append(self.getOddsFloat("WHA", header, values))
		oddsList.append(self.getOddsFloat("SJA", header, values))
		oddsList.append(self.getOddsFloat("VCA", header, values))

		validList = []
		for element in oddsList:
			if element is not None and element > 0.0:
				validList.append(element)
		
		if len(validList) > 0:
			return min(validList)
		else:
			raise ValueError
			

	def extractSeasonCode(self, key, header, values):
		try:
			dateIndex = header.index(key)	
			dateString = values[dateIndex]
			dateTokens = re.split("/",dateString)
			if len(dateTokens) != 3:
				return None
			else:
				if (int(dateTokens[2])-1) < 0:
					yearPrior = '99'
				elif (int(dateTokens[2])-1) < 10:
					yearPrior = '0' + str(int(dateTokens[2])-1)
				else:
					yearPrior = str(int(dateTokens[2])-1)

				year = dateTokens[2]

				if (int(dateTokens[2])+1) == 100:
					yearAfter = '00'
				elif (int(dateTokens[2])+1) < 10:
					yearAfter = '0' + str(int(dateTokens[2])+1)
				else:
					yearAfter = str(int(dateTokens[2])+1)

				month = int(dateTokens[1])
				if month >= 7:
					return (year+yearAfter)
				else:
					return (yearPrior+year)
		except:
			return None

	def isHomeWin(self):
		""" Returns true if the result is a home win, otherwise returns false. 
		"""
		if self.getHomeFT() > self.getAwayFT():
			return True
		else:
			return False

	def isAwayWin(self):
		""" Returns true if an away win, false otherwise.
		"""
		if self.getHomeFT() < self.getAwayFT():
			return True
		else:
			return False
			
	def isWin(self, teamName):
		""" Returns true if the given team name wins the fixture, 
		    otherwise returns false, even if the team is unknown.
		"""
		if self.getHomeTeam() == teamName and self.isHomeWin():
			return True
		elif self.getAwayTeam() == teamName and self.isAwayWin():
			return True
		else:
			return False

	def isLoss(self, teamName):
		""" Returns true if the given team name loses the fixture, 
		    otherwise returns false, even if the team is unknown.
		"""
		if self.getAwayTeam() == teamName and self.isHomeWin():
			return True
		elif self.getHomeTeam() == teamName and self.isAwayWin():
			return True
		else:
			return False
