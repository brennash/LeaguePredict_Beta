import csv
import json
import collections
import logging
import os
from leaguepredict.data.League import League
from leaguepredict.data.Fixture import Fixture

class FeatureSet:

	def __init__(self):
		self.logger = logging.getLogger('LeaguePredict')
		self.featuresList = []
		
	def addFeatures(self, filename):
		self.logger = logging.getLogger('LeaguePredict')

		# Read the CSV fixtures
		fixturesList = self.readFixturesCSV(filename)

		# Initialise the features list
		self.setFeatures(fixturesList, filename)

	def append(self, featureSet):
		""" Adds another featureSet to this one, i.e., appends
			the list of features in the other featureSet to the 
			list of features in this one. Used to concatenate 
			multiple featureSets.
		"""
		otherFeaturesList = featureSet.getFeaturesList()
		self.featuresList = self.featuresList + otherFeaturesList
	
	def readFixturesCSV(self, filename):
		""" Loads the specified CSV file, and extracts the data as
			fixtures, which are then returned as a list of Fixture objects.
		"""
		lineNum = 0
		header = None
		fixtureData = None
		fixturesList = []
		
		# Open and read the CSV fixtures file
		reader = csv.reader(open(filename,"rb"))
		for row in reader:
			if lineNum == 0:
				header = row
			else:
				fixtureData = row
				fixture = Fixture(header, fixtureData)
				fixturesList.append(fixture)
			lineNum += 1
			
		# Return the list of the fixtures in the CSV file
		self.logger.info('Read %d fixtures from %s (%d lines)',len(fixturesList), filename, lineNum)
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

	def setFeatures(self, fixturesList, filename):
		""" Function which iterates through the fixtures list
			creating an associated feature set for each fixture.
			The features are stored in the global featuresList variable. 
		"""		
		# Initialize the league with the fixtures data
		leagueCode, seasonCode = self.getFileDetails(filename)
		league = League(leagueCode, seasonCode)

		numFixtures = 0
		for fixture in fixturesList:
			if league.hasMinGames():
				# get the features
				fixtureFeatures = self.getFixtureFeatures(league, fixture)
				self.featuresList.append(fixtureFeatures)
				
				# Update the league with the fixture
				league.addFixture(fixture)
			else:
				league.addFixture(fixture)
			numFixtures += 1

		self.logger.info('Initialized Season %s, League %s with %d fixtures',seasonCode, leagueCode, numFixtures)
	
	def getFixtureFeatures(self, league, fixture):
		fixtureFeatures = []
		features = Features()
		features.addFeatures(league, fixture)
		return features
		
	def getFeaturesList(self):
		""" Returns the instantiated list of features for the 
			Features object.
		"""
		return self.featuresList
		
	def size(self):
		""" Returns the number of features in the featureSet.
		"""
		return len(self.featuresList)
