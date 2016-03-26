import re
import collections
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

		# Adding the result (if applicable) for model building
		homeResult = self.checkHomeWin(homeTeam, awayTeam, fixture)
		awayResult = self.checkAwayWin(homeTeam, awayTeam, fixture)
		self.addFeatureElement('homeResult', homeResult)
		self.addFeatureElement('awayResult', awayResult)
		
		# The information on the feature
		self.addFeatureElement('leagueCode', self.leagueCode)
		self.addFeatureElement('seasonCode', self.seasonCode)
		self.addFeatureElement('date', fixture.getDate())
		self.addFeatureElement('homeTeam', fixture.getHomeTeam())
		self.addFeatureElement('awayTeam', fixture.getAwayTeam())
		self.addFeatureElement('homeFT', fixture.getHomeFT())
		self.addFeatureElement('awayFT', fixture.getAwayFT())
		self.addFeatureElement('probHomeWin', homeTeam.getProbHomeWin())
		self.addFeatureElement('probAwayLoss', awayTeam.getProbAwayLoss())
			
		self.addFeatureMask('homeResult')
		self.addFeatureMask('awayResult')
		self.addFeatureMask('leagueCode')
		self.addFeatureMask('seasonCode')
		self.addFeatureMask('date')		
		self.addFeatureMask('homeTeam')
		self.addFeatureMask('awayTeam')
		self.addFeatureMask('homeFT')
		self.addFeatureMask('awayFT')
		
	def getCSV(self):
		valueList = []
		for key, value in self.dict.items():
			valueList.append(value)
		return ','.join(valueList)
	
	def getHeader(self, mask=False):
		keyList = []
		for key, value in self.dict.items():
			if self.mask[key] == mask:
				keyList.append(key)
		return keyList
		
	def getFeatureData(self, mask=False):
		""" If you set the mask to False, only the relevant
			data will be returned. If True the data that's been 
			masked out will be returned. 
		"""
		valueList = []
		for key, value in self.dict.items():
			if self.mask[key] == mask:
				valueList.append(value)
		return valueList
	
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
