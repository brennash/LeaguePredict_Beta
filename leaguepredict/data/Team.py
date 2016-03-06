import math
from leaguepredict.data.Fixture import Fixture

class Team :

	def __init__(self, teamName) :
		self.teamName = teamName
		self.homePlayed = 0
		self.homeWin = 0
		self.homeDraw = 0
		self.homeLose = 0
		self.homeGF = 0
		self.homeGA = 0
		self.homePoints = 0

		self.awayPlayed = 0
		self.awayWin = 0
		self.awayDraw = 0
		self.awayLose = 0
		self.awayGF = 0
		self.awayGA = 0
		self.awayPoints = 0

		self.totalShots = 0.0
		self.totalShotsTarget = 0.0
		self.totalShotsAgainst = 0.0
		self.totalShotsAgainstTarget = 0.0

		self.clearHomeWins = 0.0
		self.clearHomeLosses = 0.0
		self.clearAwayWins = 0.0
		self.clearAwayLosses = 0.0

		self.totalHTWins = 0.0
		self.totalHTLosses = 0.0

		self.prevLossFlag = 0.0

		self.kMeans = 0.0
		self.kMeansList = []

		self.eigenValue = 0.0
		self.eigenValueList = []

		self.fixtureList = []

		self.recentLimit = 5
		self.goalsForList = []
		self.goalsAgainstList = []

	def addFixture(self, fixture) :
		self.fixtureList.append(fixture)

		if fixture.getHomeTeam() == self.teamName :
			self.homePlayed += 1
			self.homeGF += fixture.getHomeFT()
			self.homeGA += fixture.getAwayFT()

			self.goalsForList.append(fixture.getHomeFT())
			self.goalsAgainstList.append(fixture.getAwayFT())

			self.totalShots += fixture.getHomeShots()
			self.totalShotsTarget += fixture.getHomeShotsTarget()
			self.totalShotsAgainst += fixture.getAwayShots()
			self.totalShotsAgainstTarget += fixture.getAwayShotsTarget()
	
			if fixture.getHomeFT() > fixture.getAwayFT() :
				self.homeWin += 1
				self.homePoints += 3
			elif fixture.getHomeFT() == fixture.getAwayFT() :
				self.homeDraw += 1
				self.homePoints += 1
			else :
				self.homeLose += 1
		else :
			self.awayPlayed += 1
			self.awayGF += fixture.getAwayFT()
			self.awayGA += fixture.getHomeFT()

			self.goalsForList.append(fixture.getAwayFT())
			self.goalsAgainstList.append(fixture.getHomeFT())

			self.totalShots += fixture.getAwayShots()
			self.totalShotsTarget += fixture.getAwayShotsTarget()
			self.totalShotsAgainst += fixture.getHomeShots()
			self.totalShotsAgainstTarget += fixture.getHomeShotsTarget()

			if fixture.getHomeFT() > fixture.getAwayFT() :
				self.awayLose += 1
			elif fixture.getHomeFT() == fixture.getAwayFT() :
				self.awayDraw += 1
				self.awayPoints += 1
			else :
				self.awayWin += 1
				self.awayPoints += 3

		# Sets the previous fixtures
		self.setClearResult(fixture)
		self.setPreviousFixture(fixture)
		self.setHTResult(fixture)

	def setClearResult(self, fixture):
		""" Increments a flag when the home team wins 
		    by two clear goals or the away team loses by 
		    two clear goals. 
		"""
		homeTeam = fixture.getHomeTeam()
		awayTeam = fixture.getAwayTeam()
		homeHT = fixture.getHomeHT()
		awayHT = fixture.getAwayHT()
		homeFT = fixture.getHomeFT()
		awayFT = fixture.getAwayFT()

		# Home game 
		if self.teamName == homeTeam:
			if (homeFT - awayFT) >= 2:
				self.clearHomeWins += 1.0
			elif (awayFT - homeFT) >= 2:
				self.clearHomeLosses += 1.0
		# Away game
		else:
			if (homeFT - awayFT) >= 2:
				self.clearAwayLosses += 1.0
			elif (awayFT - homeFT) >= 2:
				self.clearAwayWins += 1.0

	def setPreviousFixture(self, fixture):
		homeTeam = fixture.getHomeTeam()
		awayTeam = fixture.getAwayTeam()
		homeFT = fixture.getHomeFT()
		awayFT = fixture.getAwayFT()

		#Home game
		if self.teamName == homeTeam:
			if homeFT < awayFT: 
				self.prevLossFlag = 1.0
			else:
				self.prevLossFlag = 0.0
		#Away game
		else:
			if homeFT > awayFT:
				self.prevLossFlag = 1.0
			else:
				self.prevLossFlag = 0.0
			
	def setHTResult(self, fixture):
		homeTeam = fixture.getHomeTeam()
		awayTeam = fixture.getAwayTeam()
		homeHT = fixture.getHomeHT()
		awayHT = fixture.getAwayHT()

		# Home game 
		if self.teamName == homeTeam:
			if homeHT > awayHT:
				self.totalHTWins += 1.0
			elif homeHT < awayHT:
				self.totalHTLosses += 1.0
		# Away game
		else:
			if homeHT < awayHT:
				self.totalHTWins += 1.0
			elif homeHT > awayHT:
				self.totalHTLosses += 1.0


	def setKMeans(self, value):
		self.kMeansList.append(value)
		self.kMeans = value

	def getKMeans(self):
		return self.kMeans
		
	def getKMeansList(self):
		return self.kMeansList

	def setEigenValue(self, value):
		self.eigenValueList.append(value)
		self.eigenValue = value

	def getEigenValue(self):
		return self.eigenValue

	def getEigenValueList(self):
		return self.eigenValueList

	def setRecentLimit(self, value):
		self.recentLimit = value

	def getRecentLimit(self):
		return self.recentLimit

	def getProbClearWin(self):
		totalPlayed = float( self.homePlayed + self.awayPlayed )
		wins = float( self.clearHomeWins + self.clearAwayWins )
		if totalPlayed > 0.0:
			return wins/totalPlayed
		return 0.0

	def getProbClearHomeWins(self):
		totalPlayed = float(self.homePlayed)
		if totalPlayed < 1.0:
			return 0.0
		else:
			return (self.clearHomeWins/totalPlayed)

	def getProbClearHomeLosses(self):
		totalPlayed = float(self.homePlayed)
		if totalPlayed < 1.0:
			return 0.0
		else:
			return (self.clearHomeLosses/totalPlayed)

	def getProbClearLoss(self):
		totalPlayed = float( self.homePlayed + self.awayPlayed )
		wins = float( self.clearHomeLosses + self.clearAwayLosses )
		if totalPlayed > 0.0:
			return wins/totalPlayed
		return 0.0

	def getProbClearAwayWins(self):
		totalPlayed = float(self.awayPlayed)
		if totalPlayed < 1.0:
			return 0.0
		else:
			return (self.clearAwayWins/totalPlayed)

	def getProbClearAwayLosses(self):
		totalPlayed = float(self.awayPlayed)
		if totalPlayed < 1.0:
			return 0.0
		else:
			return (self.clearAwayLosses/totalPlayed)

	def getHomeGoalDiff(self):
		return (self.homeGF - self.homeGA)

	def getAwayGoalDiff(self):
		return (self.awayGF - self.awayGA)

	def getGoalDiff(self) :
		return (self.homeGF + self.awayGF - self.homeGA - self.awayGA)

	def getHomePoints(self):
		return self.homePoints

	def getAwayPoints(self):
		return self.awayPoints

	def getPoints(self) :
		return (self.awayPoints + self.homePoints)

	def getTeamName(self) :
		return self.teamName

	def getPlayed(self):
		return (self.homePlayed + self.awayPlayed)

	def getWins(self):
		return (self.homeWin + self.awayWin)

	def getDraws(self):
		return (self.homeDraw + self.awayDraw)

	def getLosses(self):
		return (self.homeLose + self.awayLose)

	def getHomeWins(self):
		return self.homeWin

	def getHomeDraws(self):
		return self.homeDraw

	def getHomeLosses(self):
		return self.homeLose

	def getAwayWins(self):
		return self.awayWin

	def getAwayDraws(self):
		return self.awayDraw

	def getAwayLosses(self):
		return self.awayLose

	def getWinningStreak(self):
		streak = 0.0
		for fixture in self.fixtureList[::-1]:
			if fixture.getHomeTeam() == self.teamName and fixture.getHomeFT() > fixture.getAwayFT():
				streak += 1.0
			elif fixture.getAwayTeam() == self.teamName and fixture.getAwayFT() > fixture.getHomeFT():
				streak += 1.0
			else:
				break
		return streak

	def getLosingStreak(self):
		streak = 0.0
		for fixture in self.fixtureList[::-1]:
			if fixture.getHomeTeam() == self.teamName and fixture.getHomeFT() < fixture.getAwayFT():
				streak += 1.0
			elif fixture.getAwayTeam() == self.teamName and fixture.getAwayFT() < fixture.getHomeFT():
				streak += 1.0
			else:
				break
		return streak

	def getGF(self):
		return (self.homeGF + self.awayGF)

	def getGA(self):
		return (self.homeGA + self.awayGA)

	def getTotalShots(self):
		return self.totalShots

	def getTotalShotsAgainst(self):
		return self.totalShotsAgainst

	def getTotalShotsTarget(self):
		return self.totalShotsTarget

	def getTotalShotsAgainstTarget(self):
		return self.totalShotsAgainstTarget

	def getNumFixtures(self):
		return len(self.fixtureList)

	def getGoalsForPerGame(self):
		played = float(self.homePlayed + self.awayPlayed)
		goalsFor = float(self.homeGF + self.awayGF)
		if played > 0:
			return ( goalsFor / played )
		else:
			return 0.0

	def getGoalsAgainstPerGame(self, awayOnly=False):
		played = float(self.homePlayed + self.awayPlayed)
		goalsAgainst = float(self.homeGA + self.awayGA)
		if played > 0:
			return ( goalsAgainst / played ) 
		else:
			return 0.0

	def getProbWin(self):
		if (self.homePlayed + self.awayPlayed) > 0:
			return float(self.homeWin+self.awayWin)/float(self.homePlayed+self.awayPlayed)
		return 0.0

	def getProbLoss(self):
		if (self.homePlayed + self.awayPlayed) > 0:
			return float(self.homeLose+self.awayLose)/float(self.homePlayed+self.awayPlayed)
		return 0.0

	def getProbHTWin(self):
		if (self.homePlayed + self.awayPlayed) > 0:
			return float(self.totalHTWins)/float(self.homePlayed+self.awayPlayed)
		return 0.0

	def getProbHTLoss(self):
		if (self.homePlayed + self.awayPlayed) > 0:
			return float(self.totalHTLosses)/float(self.homePlayed+self.awayPlayed)
		return 0.0

	def getProbHomeWin(self):
		if self.homePlayed > 0:
			return float(self.homeWin)/float(self.homePlayed)
		return 0.0

	def getProbHomeLoss(self):
		if self.homePlayed > 0:
			return float(self.homeLose)/float(self.homePlayed)
		return 0.0

	def getProbAwayWin(self):
		if self.awayPlayed > 0:
			return float(self.awayWin)/float(self.awayPlayed)
		return 0.0

	def getProbAwayLoss(self):
		if self.awayPlayed > 0:
			return float(self.awayLose)/float(self.awayPlayed)
		return 0.0

	def getShotsPerGame(self):
		shots = float(self.totalShots) 
		played = float(self.homePlayed + self.awayPlayed)
		if played > 0.0:
			return ( shots / played )
		return 0.0

	def getShotsPerGameOnTarget(self):
		shots = float(self.totalShotsTarget) 
		played = float(self.homePlayed + self.awayPlayed)
		if played > 0.0:
			return ( shots / played )
		return 0.0

	def getShotsAgainstPerGame(self):
		if self.awayPlayed > 0:
			return self.totalShotsAgainst/float(self.awayPlayed)
		return 0.0

	def getShotsAgainstPerGameOnTarget(self):
		if self.awayPlayed > 0:
			return self.totalShotsAgainstTarget/float(self.awayPlayed)
		return 0.0

	def getPreviousLosses(self, n):
		if n <= len(self.fixtureList):
			fixture = self.fixtureList[-1*n]
			if fixture.isLoss(self.teamName):
				return 1
			else:
				return 0
		else:
			return None

	def getPreviousWins(self, n):
		if n <= len(self.fixtureList):
			fixture = self.fixtureList[-1*n]
			if fixture.isWin(self.teamName):
				return 1
			else:
				return 0
		else:
			return None

	def getPreviousResult(self, n):
		if n <= len(self.fixtureList):
			fixture = self.fixtureList[-1*n]
			if fixture.isWin(self.teamName):
				return 1.0
			elif fixture.isLoss(self.teamName):
				return 0.0
			else:
				return 0.5
		else:
			return 0.0

	def getPreviousResults(self):
		results = []
		for fixture in self.fixtureList:
			if fixture.isWin(self.teamName):
				results.append('W')
			elif fixture.isLoss(self.teamName):
				results.append('L')
			else:
				results.append('D')
		return results

	def getFixtureList(self):
		return self.fixtureList

	def getRecentPoints(self):
		points = 0
		if len(self.fixtureList) > self.recentLimit:
			results = self.getPreviousResults()
			for result in reversed(results[(-1*self.recentLimit):]):
				if result == 'W':
					points += 3
				elif result == 'D':
					points += 1
		return points

	def getRecentGA(self):
		total = 0
		if len(self.goalsAgainstList) > self.recentLimit:
			for value in reversed(self.goalsAgainstList[(-1*self.recentLimit):]):
				total += value
		return total


	def getRecentGF(self):
		total = 0
		if len(self.goalsForList) > self.recentLimit:
			for value in reversed(self.goalsForList[(-1*self.recentLimit):]):
				total += value
		return total


	def getRecentProbWin(self):
		total = 0.0
		count = 0.0
		if len(self.fixtureList) > self.recentLimit:
			results = self.getPreviousResults()
			for result in reversed(results[(-1*self.recentLimit):]):
				count += 1.0
				if result == 'W':
					total += 1.0
		if count == 0.0:
			return 0.0
		else:
			return (total/count)

	def getRecentProbLoss(self):
		total = 0.0
		count = 0.0
		if len(self.fixtureList) > self.recentLimit:
			results = self.getPreviousResults()
			for result in reversed(results[(-1*self.recentLimit):]):
				count += 1.0
				if result == 'L':
					total += 1.0
		if count == 0.0:
			return 0.0
		else:
			return (total/count)


	def getForm(self, n):
		""" Get the weighted form using the 
		    weighting E^-lambdaWeight*(Size-Index)
		"""
		if n > len(self.fixtureList):
			return 0.0

		weightList = []
		resultList = []

		sumWeights = 0.0
		index = 1
		lambdaWeight = 0.2

		for x in xrange(0, n):
			result = self.getPreviousResult(index)
			weight = math.exp(lambdaWeight*-1.0*(float(n-index)))
			weightList.append(weight)
			resultList.append(result)
			sumWeights += weight
			index += 1
	
		weightedSum = 0.0
		for wIndex, weight in enumerate(weightList):
			result = resultList[wIndex]
			weightedSum += (result*(weight/sumWeights))		

		return weightedSum
