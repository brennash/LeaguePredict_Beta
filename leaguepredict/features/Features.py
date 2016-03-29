import re
import collections
import datetime
from leaguepredict.data.League import League
from leaguepredict.data.Fixture import Fixture

class Features :

	def __init__(self, league, fixture):
		self.dict = collections.OrderedDict()
		self.mask = collections.OrderedDict()
		
		self.fixture = fixture
		self.seasonCode = league.getSeasonCode()
		self.leagueCode = league.getLeagueCode()
	
		homeTeam = league.getTeam(fixture.getHomeTeam())
		awayTeam = league.getTeam(fixture.getAwayTeam())
		
		if homeTeam is None:
			print homeTeam, 'home team is none'
		elif awayTeam is None:
			print awayTeam, 'away team is none'
			print fixture.toString()
		
		homeTeamName = homeTeam.getTeamName()
		awayTeamName = awayTeam.getTeamName()

		# Adding the result (if applicable) for model building
		homeResult = self.checkHomeWin(homeTeam, awayTeam, fixture)
		awayResult = self.checkAwayWin(homeTeam, awayTeam, fixture)
		self.addFeatureElement('homeResult', homeResult)
		self.addFeatureElement('awayResult', awayResult)
		
		# The information on the feature
		self.addFeatureElement('leagueCode', self.leagueCode)
		self.addFeatureElement('seasonCode', self.seasonCode)
		self.addFeatureElement('date', fixture.getDateString())
		self.addFeatureElement('homeTeam', fixture.getHomeTeam())
		self.addFeatureElement('awayTeam', fixture.getAwayTeam())
		self.addFeatureElement('homeFT', fixture.getHomeFT())
		self.addFeatureElement('awayFT', fixture.getAwayFT())
		self.addFeatureElement('bestHomeOdds', fixture.getBestHomeOdds())
		self.addFeatureElement('worstHomeOdds', fixture.getWorstHomeOdds())

		probWin = (homeTeam.getProbWin() + awayTeam.getProbLoss() ) / 2.0
		probLoss = (homeTeam.getProbLoss() + awayTeam.getProbWin() ) / 2.0
		probHomeWin = (homeTeam.getProbHomeWin() + awayTeam.getProbAwayLoss() ) / 2.0
		probHomeLoss = (homeTeam.getProbHomeLoss() + awayTeam.getProbAwayWin() ) / 2.0
		probClearWin = (homeTeam.getProbClearHomeWins() + awayTeam.getProbClearAwayLosses() ) / 2.0
		probClearLoss = (homeTeam.getProbClearHomeLosses() + awayTeam.getProbClearAwayWins() ) / 2.0
		homeShots = (homeTeam.getShotsPerGame() + awayTeam.getShotsAgainstPerGame()) / 2.0
		homeShotsAgainst = (homeTeam.getShotsAgainstPerGame() + awayTeam.getShotsPerGame()) / 2.0
		homeShotsTarget = (homeTeam.getShotsPerGameOnTarget() + awayTeam.getShotsAgainstPerGameOnTarget()) / 2.0
		homeShotsAgainstTarget = (homeTeam.getShotsAgainstPerGameOnTarget() + awayTeam.getShotsPerGameOnTarget()) / 2.0
		formDiff = (homeTeam.getForm(5) - awayTeam.getForm(5))
		evDiff = (league.getEigenValue(homeTeamName) - league.getEigenValue(awayTeamName))
		kMeansDiff = (league.getKMeans(homeTeamName) - league.getKMeans(awayTeamName))
		homeWinOdds1 = (fixture.getBestHomeOdds() - fixture.getBestAwayOdds())
		homeWinOdds2 = (fixture.getWorstHomeOdds() - fixture.getWorstAwayOdds())

		self.addFeatureElement('probWin', probWin)
		self.addFeatureElement('probLoss', probLoss)
		self.addFeatureElement('probHomeWin', probHomeWin)
		self.addFeatureElement('probHomeLoss', probHomeLoss)
		self.addFeatureElement('probClearWin', probClearWin)
		self.addFeatureElement('probClearLoss', probClearLoss)
		self.addFeatureElement('homeShots', homeShots)
		self.addFeatureElement('homeShotsAgainst', homeShotsAgainst)
		self.addFeatureElement('homeShotsTarget', homeShotsTarget)
		self.addFeatureElement('homeShotsAgainstTarget', homeShotsAgainstTarget)
		self.addFeatureElement('formDiff', formDiff)
		self.addFeatureElement('evDiff', evDiff)
		self.addFeatureElement('kMeansDiff', kMeansDiff)
		self.addFeatureElement('homeWinOdds1', homeWinOdds1)
		self.addFeatureElement('homeWinOdds2', homeWinOdds2)

		self.addFeatureMask('homeResult')			
		self.addFeatureMask('awayResult')			
		self.addFeatureMask('leagueCode')
		self.addFeatureMask('seasonCode')
		self.addFeatureMask('date')
		self.addFeatureMask('homeTeam')
		self.addFeatureMask('awayTeam')
		self.addFeatureMask('homeFT')
		self.addFeatureMask('awayFT')
		self.addFeatureMask('bestHomeOdds')
		self.addFeatureMask('worstHomeOdds')
		
	def getCSV(self):
		valueList = []
		for key, value in self.dict.items():
			valueList.append(value)
		return ','.join(valueList)
			
	def addFeatureElement(self, key, value):
		""" Add a feature element. By default do not set a 
			mask to exclude this feature. 
		"""
		if key in self.dict.keys():
			logger.warning('Overwriting Feature Element (%s)',key)
			self.dict[key] = value
			self.mask[key] = False
		else:			
			self.dict[key] = value
			self.mask[key] = False
			
	def addFeatureMask(self, key):
		self.mask[key] = True
	
	def getHomeResult(self):
		""" Returns the numeric home result of this feature/fixture, where
			1.0 indicates a home win, and 0.0 a draw or loss.
		"""
		try:
			result = self.dict['homeResult']
			return result
		except:
			return None
	
	def getAwayResult(self):
		""" Returns the numeric away result of this feature/fixture, where
			1.0 indicates a home win, and 0.0 a draw or loss.
		"""
		try:
			result = self.dict['awayResult']
			return result
		except:
			return None
	
	def printFeature(self):
		header = self.getHeader()
		values = self.getCSV()
		print header
		print values
	
	def checkHomeWin(self, homeTeam, awayTeam, fixture):
		if fixture.hasScore():
			if fixture.isHomeWin():
				return 1.0
			return 0.0
		return -1.0	

	def checkAwayWin(self, homeTeam, awayTeam, fixture):
		if fixture.hasScore():
			if fixture.isAwayWin():
				return 1.0
			return 0.0
		return -1.0	
	
	def getDate(self):
		try:
			dateString = self.dict['date']
			return datetime.datetime.strptime(dateString, '%d/%m/%y')
		except:
			return None		
	
	def getHeader(self):
		""" Returns all the headers for the entire set of 
			features. This includes descriptive metrics. 
		"""
		keyList = []	
		for key, value in self.dict.items():
			keyList.append(key)
		return keyList
		
	def getValidCols(self, homeResult=True):
		""" Returns a list of headers which will only
			be used for the models.  
		"""					
		keyList = []	
		for key, value in self.dict.items():
			if self.mask[key] == False:
				keyList.append(key)
		return keyList
	
	def getFeatureData(self):
		""" If you set the mask to False, only the relevant
			data will be returned. If True the data that's been 
			masked out will be returned. 
		"""		
		valueList = []
		for key, value in self.dict.items():
				valueList.append(value)
		return valueList