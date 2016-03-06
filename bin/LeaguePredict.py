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
from optparse import OptionParser

def main(argv):

	# Set the log details
	logger = logging.getLogger('LeaguePredict')
	logger.setLevel(logging.INFO)
	handler = logging.FileHandler('log/leaguepredict.log')
	handler.setLevel(logging.INFO)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	logger.info('Starting LeaguePredict in %s', os.getcwd())

	# Set the input parameters
	parser = OptionParser(usage="Usage: runLeaguePredict <config-json>")
	parser.add_option("-v", "--verbose",
		action="store_true", 
		dest="verbose",
		default=False,
 		help="verbose output")
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

		# Initialise the feature set with the specified name
		trainingFeatureSet = getFeatureSet('training-data', configDict)
		evaluationFeatureSet = getFeatureSet('evaluation-data', configDict)
		
	except ValueError:
		print 'Error - invalid JSON config provided.'


def getFeatureSet(jsonHeader, configDict):
	""" Gets the list of features associated with each provided 
		data file. Takes as input the jsonHeader ('training-data'|'evaluation-data') as
		well as the dict representing the JSON configuration.
		
		Outputs a list of features, one per each input line. 
	"""

	logger = logging.getLogger('LeaguePredict')

	# The features list for each input file
	resultSet = FeatureSet()
		
	if jsonHeader != 'training-data' and jsonHeader != 'evaluation-data':
		logger.error('%s','GetFeatures() needs to specity training-data or evaluation-data')
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
			
	logger.info('Total %s is %d',jsonHeader, resultSet.size())
	return resultSet


if __name__ == "__main__":
    sys.exit(main(sys.argv))
