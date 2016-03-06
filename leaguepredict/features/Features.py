import csv
import json
import collections
import logging
import os
from leaguepredict.data.League import League
from leaguepredict.data.Fixture import Fixture

class Features:

	def __init__(self, filename):
		logger = logging.getLogger('LeaguePredict')
		
		# Read the CSV fixtures
		self.featuresList = []
		fixturesList = self.readFixtures(filename)
		
		# Initialize the league with the fixtures data
		leagueCode, seasonCode = self.getFileDetails(filename)
		logger.info('Initializing Season %s, League %s',seasonCode, leagueCode)
		league = League(leagueCode, seasonCode)
		league.addFixtures(fixturesList)
	
	def readFixtures(self, filename):
		logger = logging.getLogger('LeaguePredict')

		lineNum = 0
		header = None
		fixtureData = None
		fixturesList = []
		
		reader = csv.reader(open(filename,"rb"))
		for row in reader:
			if lineNum == 0:
				header = row
			else:
				fixtureData = row
				fixture = Fixture(header, fixtureData)
				fixturesList.append(fixture)
			lineNum += 1
			
		logger.info('Read %d fixtures from %s',len(fixturesList), filename)
		return fixturesList
							
	def getFileDetails(self, filePath):
		""" Gets the file list and parses it to 
			find the league code (e.g., E0) and
			the seasoncode (e.g, 1615)
		"""
		tokens = filePath.split(os.path.sep)
		leagueCode = tokens[-1].split('.')[0]
		seasonCode = tokens[-2]
		return leagueCode, seasonCode
	
	def getFeaturesList(self):
		return self.featuresList
