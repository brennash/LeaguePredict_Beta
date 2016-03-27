#!/usr/bin/env python

# Package:     runLeaguePredict (main function)
# Author:      Shane Brennan
# Date:        20150229
# Description: The main calling function for the LeaguePredict package. 
#
import sys
import os
import json
import logging
from leaguepredict.features.FeatureSet import FeatureSet
from leaguepredict.model.LeaguePredictModel import LeaguePredictModel
from leaguepredict.evaluation.ModelEvaluation import ModelEvaluation

from optparse import OptionParser

# Set the log details
logger = logging.getLogger('LeaguePredict')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('log/leaguepredict.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def main(argv):
	# Set the input parameters
	parser = OptionParser(usage="Usage: runLeaguePredict <config-json>")
	(options, filename) = parser.parse_args()

	# Check a single config file is included
	if len(filename) != 1:
		parser.print_help()
		print 'Error - you need to provide a JSON file with the model config.'
		logger.error('Tried to start LeaguePredict without JSON config, exiting')
		sys.exit(1)
	
	# Check the config file exists	
	if not os.path.exists(filename[0]):
		parser.print_help()
		print 'Error - you need to provide an existing JSON file with the model config.'
		logger.error('Tried to start LeaguePredict with invalid JSON (%s) file, exiting', filename[0])		
		sys.exit(1)

	# Create the training and evaluation features
	try:
		logger.info('Reading JSON Config filename %s',filename[0])		
		configDict = json.loads(open(filename[0]).read())
	except ValueError:
		print 'Error - invalid JSON config provided.'
		logger.error('Invalid JSON config provided in %s',filename[0])
		exit(1)
		
	# Now the main part of the simulation
	# 1. Get the training and evaluation features
	trainingFeatureSet = getFeatureSet('training-data', configDict)
	evaluationFeatureSet = getFeatureSet('evaluation-data', configDict)
	logger.info('Training Features: %d',trainingFeatureSet.size())
	logger.info('Evaluation Features: %d',evaluationFeatureSet.size())

	# 2. Build a model with the training features only
	leaguePredictModel = LeaguePredictModel(trainingFeatureSet)
	model = leaguePredictModel.getModel()
	
	# 3. Evaluate the performance of the model
	logger.error('Evaluation Features: %d',evaluationFeatureSet.size())
	evaluation = ModelEvaluation(model, evaluationFeatureSet)
#	evaluation.printSummary()
		


def getFeatureSet(jsonHeader, configDict):
	""" Gets the list of features associated with each provided data file. Takes as 
		input the jsonHeader ('training-data'|'evaluation-data') as well as the dict 
		representing the JSON configuration. Outputs a list of features, 
		one per each input line. 
	"""
	# The features list for each input file
	resultSet = FeatureSet()
		
	if jsonHeader != 'training-data' and jsonHeader != 'evaluation-data':
		logger.error('%s','GetFeatures() needs to specify training-data or evaluation-data')
		return None
		
	parentDir = os.getcwd()
	jsonFileList = configDict[jsonHeader]
	for inputFile in jsonFileList:
		jsonFile = inputFile['file']
		if jsonFile[0] == '/':
			path = jsonFile
		else:
			path = parentDir+'/'+jsonFile

		if os.path.exists(path) and os.path.isfile(path):
			# Take each JSON file as input and parse it to create features
			logger.info('Reading from CSV data (%s), %s', jsonHeader, path)
			featureSet = FeatureSet()
			featureSet.addFeatures(path)
			resultSet.append(featureSet)
		else:
			logger.error('Cannot read from file %s', path)
	return resultSet


if __name__ == "__main__":
    sys.exit(main(sys.argv))
