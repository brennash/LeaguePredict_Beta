import csv
import json
import collections
import logging
import os
from leaguepredict.data.League import League
from leaguepredict.data.Fixture import Fixture
from leaguepredict.features.Features import Features

class FeatureSet:

	def __init__(self):
		self.logger = logging.getLogger('LeaguePredict')
	
		# The list of Features objects
		self.featuresList = []
	
	def addFeatures(self, filename):
		""" Adds features from a specified filename.
		"""
		self.logger = logging.getLogger('LeaguePredict')

		# Read the CSV fixtures
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

		# Initialise the features list
		self.setFeatures(fixturesList, filename)

	def getFeaturesList(self):
		""" Returns the list of features objects, allowing FeatureSets 
			to append multiple lists of features. 
		"""
		return self.featuresList

	def append(self, featureSet):
		""" Adds another featureSet to this one, i.e., appends
			the list of features in the other featureSet to the 
			list of features in this one. Used to concatenate 
			multiple featureSets.
		"""
		otherFeaturesList = featureSet.getFeaturesList()
		self.featuresList = self.featuresList + otherFeaturesList
		self.sortFeaturesByDate()
		self.logger.info('Adding to FeatureSet, size: %d',len(self.featuresList))
		
							
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
				features = Features(league, fixture)
				self.featuresList.append(features)
				league.addFixture(fixture)
			else:
				league.addFixture(fixture)
			numFixtures += 1

		self.sortFeaturesByDate()
		self.logger.info('Initialized Season %s, League %s with %d fixtures',seasonCode, leagueCode, numFixtures)
	
	def sortFeaturesByDate(self):
		self.featuresList.sort(key=lambda x: x.getDate(), reverse=False)
			
	def getFeaturesData(self):
		""" Returns the features data as a list of lists.
		"""
		resultList = []
		#self.sortFeaturesByDate()
		for index, feature in enumerate(self.featuresList):
			featureData = feature.getFeatureData()
			resultList.append(featureData)
		return list(resultList)

	def getHeader(self):
		if len(self.featuresList) > 0:
			return self.featuresList[0].getHeader()
		else:
			return None

	def getValidCols(self, homeResult=True):
		""" Returns the valid columns considered as part of a model. 
			If the homeResult variable is set, or ignored then features
			associated with a home win are returned. If the variable is 
			set to False, it returns features associated with an away win. 
		"""
		return self.featuresList[0].getValidCols(homeResult)
			
	def size(self):
		""" Returns the number of features in the featureSet.
		"""
		return len(self.featuresList)
