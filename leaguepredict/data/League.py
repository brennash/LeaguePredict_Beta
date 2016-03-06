from leaguepredict.data.Team import Team
from scipy.cluster.vq import kmeans, kmeans2, whiten
import numpy as np
import math
import warnings

class League:

	def __init__(self, leagueCode, seasonCode):
		# Turn off the numpy warnings
		warnings.filterwarnings("ignore")

		self.leagueCode = leagueCode
		self.seasonCode = seasonCode
		self.leagueTable = []
		self.fixtures = []

		# Need an unsorted list of team names for EV decomposition
		self.teamNames = []
		self.teamKMeans = []

		# The minimum number of games before doing EV/K-means
		self.minGames = 6
		self.numGames = 0

	def addFixtures(self, fixtureList):
		for fixture in fixtureList:
			self.addFixture(fixture)

	def listTeams(self):
		return self.teamNames

	def addFixture(self, fixture):
		""" Adds a single fixture to the league and updates all the 
		    team-specific features. 
		"""
		self.numGames += 1
		self.fixtures.append(fixture)
		homeTeam = fixture.getHomeTeam()
		awayTeam = fixture.getAwayTeam()
		
		# Update the home team
		if homeTeam not in self.teamNames:
			self.teamNames.append(homeTeam)
			team = Team(homeTeam)
			team.addFixture(fixture)
			self.leagueTable.append(team)
		else:
			teamIndex = -1
			for x in xrange(0, len(self.leagueTable)):
				if self.leagueTable[x].getTeamName() == homeTeam:
					teamIndex = x
					break	
			self.leagueTable[teamIndex].addFixture(fixture)			

		# Update the away team
		if awayTeam not in self.teamNames:
			self.teamNames.append(awayTeam)
			team = Team(awayTeam)
			team.addFixture(fixture)
			self.leagueTable.append(team)
		else:
			teamIndex = -1
			for x in xrange(0, len(self.leagueTable)):
				if self.leagueTable[x].getTeamName() == awayTeam:
					teamIndex = x
					break	
			self.leagueTable[teamIndex].addFixture(fixture)			

		# Rank the league
		self.leagueTable.sort(key=lambda team: team.getGoalDiff(), reverse=True)
		self.leagueTable.sort(key=lambda team: team.getPoints(), reverse=True)

		# Only update the k-means and eigenvalue after
		# a minimum number of games have been played. 
		if self.getGamesPlayed() >= self.minGames:
			self.kMeansCluster()
			self.setEigenValues(fixture, updateOnly=False)
		else:
			self.setEigenValues(updateOnly=True)

	def kMeansCluster(self) :
		""" Creates a simple 5-segment k-means cluster based on a 
		    small number of league parameters. The top-ranked teams 
		    are then given a k-means score of 1.0, the middle rank 0.5 
		    and the losers are assigned 0.0. Due to random fluctuation 
		    the same team may fall into a nearby group. 
		"""
		# Put the teams into a numpy array
		clusterList = []

		# List to record the order of the teams
		kMeansTeams = []

		# Check each team has more than min games
		for index, team in enumerate(self.leagueTable):

			points = team.getPoints()
			recentForm = team.getForm(5)
			probWin = team.getProbWin()
			goalsFor = team.getGF()

			kMeansTeams.append(team.getTeamName())
			row = [points, recentForm, probWin, goalsFor]
			clusterList.append(row)

		# Get the cluster array
		clusterArray = np.array(clusterList)

		# Normalize this array
		rows, cols = clusterArray.shape
    		for col in xrange(cols):
        		clusterArray[:,col] /= abs(clusterArray[:,col]).max()

		# Randomize over several kmeans
		res, groupIDs = kmeans2(clusterArray, 5)

		# Set the team's 
		index = 0
		topGroup = groupIDs[0]
		bottomGroup = groupIDs[-1]

		for groupID in groupIDs:
			if groupID == topGroup:
				self.setKMeans(kMeansTeams[index], 1.0)
			elif groupID == bottomGroup:
				self.setKMeans(kMeansTeams[index], 0.0)
			else:
				self.setKMeans(kMeansTeams[index], 0.5)
			index += 1

	def setKMeans(self, teamName, value):
		""" Helper function to set the k-means for a named team
		"""
		for index, team in enumerate(self.leagueTable):
			if team.getTeamName() == teamName:
				self.leagueTable[index].setKMeans(value)
				break

	def setEigenValues(self, fixture=None, updateOnly=False):
		""" Updates the adjacency matrix describing the link, i.e, result
		    between teams given the current fixture list. This means that 
		    the adjacency matrix is appended with information after each 
		    fixture. The updateOnly flag when True just appends to the 
		    adjacency matrix but does not calculate EVs. 
		"""

		if fixture == None and updateOnly == True:
			self.createEVMatrix()
		elif fixture != None and updateOnly == False:
			self.updateEVMatrix(fixture)
		else:
			print "ERROR - input parameters to setEigenValues function incorrect!"

	def createEVMatrix(self):
		n = len(self.teamNames)
               	self.adjMatrix = np.zeros(n*n).reshape((n, n))
               	for fixture in self.fixtures :
			self.updateEVMatrix(fixture, updateOnly=True)

	def updateEVMatrix(self, fixture, updateOnly=False):
		index1 = self.teamNames.index(fixture.getHomeTeam())
		index2 = self.teamNames.index(fixture.getAwayTeam())
		
		if index1 != -1 and index2 != -1:
			homeFT = fixture.getHomeFT()
			awayFT = fixture.getAwayFT()

			if homeFT > awayFT:
				self.adjMatrix[index1][index2] = 1.0
			elif homeFT == awayFT:
				self.adjMatrix[index2][index1] = 0.5
				self.adjMatrix[index1][index2] = 0.5
			elif homeFT < awayFT:
				self.adjMatrix[index2][index1] = 1.0

			if updateOnly == False:
				# Get the maximum eigenvalue
				ev, evec = np.linalg.eig(self.adjMatrix)
				maxIndex = self.getMaxIndex(ev)
	
				# Get the right-hand column from the vector
				normList = []
				for vec in evec:
					normList.append(round(abs(vec[maxIndex]),16))

				# Normalize this vector to sum to 1
				evList = self.normalizeList(normList)

				# Tick through the team list and set the normalized eigen values
				minEv = min(evList)
				maxEv = max(evList)
				for index, teamName in enumerate(self.teamNames):
					teamEigenValue = (evList[index]-minEv)/(maxEv-minEv)
					self.setTeamEigenValue(teamName, teamEigenValue)
		else:
			print "Error - Cannot find teams",fixture.getHomeTeam()," and ",fixture.getAwayTeam() 

	def normalizeList(self, L, sumTo=1):
    		''' Normalize Eigen-value list to make it sum to 1, helper function for
		    the calculateEVs function.
		'''
		sum = reduce(lambda x,y:x+y, L)
		return [ x/(sum*1.0)*sumTo for x in L]

	def setTeamEigenValue(self, teamName, eigenValue):
		""" Function that sets the eigenvalue of a named team.
		"""
		for index, team in enumerate(self.leagueTable):
			if team.getTeamName() == teamName:
				self.leagueTable[index].setEigenValue(eigenValue)
				break

        def getMaxIndex(self, valueList):
		""" Helper function that iterates over a numpy array, 
		    returning the index of the maximum value therein. 
		"""
                maxValue = max(valueList)
                index = -1
                for i, value in enumerate(valueList):
                        if(value == maxValue):
                                index = i
                        i+=1
                return index

	def getFixtures(self):
		""" Returns the list of fixtures for this league so 
		    far, i.e., all fixtures. 
		"""
		return self.fixtures

	def getTeam(self, teamName):
		""" Returns a team object (or None) for a team at a 
		    specified team name string.
		"""
		for team in self.leagueTable:
			if team.getTeamName() == teamName:
				return team
		return None

	def getEigenValue(self, teamName):
		team = self.getTeam(teamName)
		return team.getEigenValue()

	def getEigenValueSumSquaredDiff(self, teamName1, teamName2):
		team1 = self.getTeam(teamName1)
		team2 = self.getTeam(teamName2)
		team1List = team1.getEigenValueList()
		team2List = team2.getEigenValueList()
		limit = team1.getRecentLimit()

		if len(team1List) >= limit and len(team2List) >= limit:
			total = 0.0
			count = 0.0
			for x in xrange(1,limit+1):
				count += 1.0
				ev1 = team1List[-1*x]
				ev2 = team2List[-1*x]
				total = ((ev1-ev2)*(ev1-ev2))

			return (total/count)
		else:
			return 0.0

	def getKMeans(self, teamName):
		team = self.getTeam(teamName)
		return team.getKMeans()

	def getKMeansSquaredDiff(self, teamName1, teamName2):
		team1 = self.getTeam(teamName1)
		team2 = self.getTeam(teamName2)
		team1List = team1.getKMeansList()
		team2List = team2.getKMeansList()
		limit = team1.getRecentLimit()

		if len(team1List) >= limit and len(team2List) >= limit:
			total = 0.0
			count = 0.0
			for x in xrange(1,limit+1):
				count += 1.0
				km1 = team1List[-1*x]
				km2 = team2List[-1*x]
				total = ((km1-km2)*(km1-km2))

			return (total/count)
		else:
			return 0.0

	def getLeagueCode(self):
		return self.leagueCode

	def getSeasonCode(self):
		return self.seasonCode

	def getPosition(self, teamName):
		position = 1
		for team in self.leagueTable:
			if team.getTeamName() == teamName:
				return position
			position += 1
		return None

	def getNumFixtures(self):
		return len(self.fixtures)

	def getNumTeams(self):
		return len(self.teamNames)

	def getNumGames(self):
		return self.numGames

	def getGamesPlayed(self):
		""" Returns the minimum number of games played
		    in this league.
		"""
		if len(self.fixtures) == 0:
			return 0
		else:
			playedList = []
			for team in self.leagueTable:
				playedList.append(team.getPlayed())
			return min(playedList)

	def getMatchDay(self):
		""" Returns the current match day for the league
		"""
		if len(self.fixtures) == 0:
			return 0
		else:
			playedList = []
			for team in self.leagueTable:
				playedList.append(team.getPlayed())
			return max(playedList)

	def hasMinGames(self):
		currentMin = self.getGamesPlayed()
		if currentMin >= self.minGames:
			return True
		return False

	def getMaxGoalsScoredPerGame(self, homeOnly=False):
		max = 0.0
		for team in self.leagueTable:
			value = team.getGoalsScoredPerGame(homeOnly=False)
			if value > max:
				max = value
		return max

	def getMaxGoalsConcededPerGame(self, awayOnly=False):
		max = 0.0
		for team in self.leagueTable:
			value = team.getGoalsConcededPerGame(awayOnly)
			if value > max:
				max = value
		return max

	def printTable(self):
		print '\n{0} ({1})'.format(self.leagueCode, self.seasonCode)
		print '========================================='
		
		for team in self.leagueTable:
			# Get the formatting right
			if len(team.getTeamName()) < 7:
				print '{0} \t\t {1},{2},{3},{4},{5},{6},{7},{8}'.format(team.getTeamName(), team.getPlayed(), team.getWins(), team.getDraws(), \
				team.getLosses(), team.getGF(), team.getGA(), team.getGoalDiff(), team.getPoints())
			else:
				print '{0} \t {1},{2},{3},{4},{5},{6},{7},{8}'.format(team.getTeamName(), team.getPlayed(), team.getWins(), team.getDraws(), \
				team.getLosses(), team.getGF(), team.getGA(), team.getGoalDiff(), team.getPoints())

