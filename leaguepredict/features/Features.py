import re
import collections
from leaguepredict.data.League import League
from leaguepredict.data.Fixture import Fixture

class Features :

	def __init__(self, league, fixture):
		self.dict = collections.OrderedDict()
		self.fixture = fixture
		self.seasonCode = league.getSeasonCode()
		self.leagueCode = league.getLeagueCode()
		homeTeam = league.getTeam(fixture.getHomeTeam())
		awayTeam = league.getTeam(fixture.getAwayTeam())
		
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
			
	def getCSV(self):
		valueList = []
		for key, value in self.dict.items():
			valueList.append(value)
		return ','.join(valueList)
	
	def getHeader(self):
		keyList = []
		for key, value in self.dict.items():
			keyList.append(key)
		return ','.join(keyList)
	
	def addFeatureElement(self, key, value):
		if key in self.dict.keys():
			logger.warning('Overwriting Feature Element (%s)',key)
			self.dict[key] = value
		else:			
			self.dict[key] = value
		
