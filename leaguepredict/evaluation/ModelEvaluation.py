import re
import os
import logging
import json
import time
import pickle
import datetime
import random
import pandas
import statsmodels.api as sm
from random import randint
from sklearn.externals import joblib
from sklearn.preprocessing import normalize
from sklearn import linear_model
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import cross_validation
from sklearn.linear_model import LogisticRegression
from sklearn import decomposition
from leaguepredict.features.FeatureSet import FeatureSet
from leaguepredict.model.LeaguePredictModel import LeaguePredictModel

class ModelEvaluation:


	def __init__(self, model, featureSet, config): 
		featureList = featureSet.getFeaturesData()
		header = featureSet.getHeader()		
		evaluationData = pandas.DataFrame(featureList, columns=header)
		
		evalutionConfig = config['evaluation-config']
		self.verbose = evalutionConfig['verbose']
		self.singleThreshold = evalutionConfig['single-threshold']
		self.accumThreshold = evalutionConfig['accumulator-threshold']
		
		validCols = featureSet.getValidCols(homeResult=True)
		self.evaluationResults = evaluationData['homeResult'].tolist()

		self.fixtureDate = evaluationData['date'].tolist()
		self.homeTeam = evaluationData['homeTeam'].tolist()
		self.awayTeam = evaluationData['awayTeam'].tolist()
		self.homeFT = evaluationData['homeFT'].tolist()
		self.awayFT = evaluationData['awayFT'].tolist()
				
		self.predictions = model.predict(evaluationData[validCols])
		self.thresholds = model.predict_proba(evaluationData[validCols])
		self.worstOddsList = evaluationData['worstHomeOdds'].tolist()
		self.bestOddsList = evaluationData['bestHomeOdds'].tolist()

	def printSummary(self):
		""" Print the summary for the evaluation metrics.
		"""
		totalWins      = [0.0, 0.0]
		totalLosses    = [0.0, 0.0]
		totalIgnored   = [0.0, 0.0]
		totalBestGain  = [0.0, 0.0]
		totalWorstGain = [0.0, 0.0]
		totalBets      = [0.0, 0.0]
	
		# The previous date, initialized to an early date
		prevDate = datetime.datetime(1990,1,1,0,0,0)
		
		for index, result in enumerate(self.evaluationResults):
			prediction = self.predictions[index]
			threshold = self.thresholds[index]

			fixtureDate = datetime.datetime.strptime(self.fixtureDate[index], '%d/%m/%y')
			


			homeTeam = self.homeTeam[index]
			awayTeam = self.awayTeam[index]
			homeFT = self.homeFT[index]
			awayFT = self.awayFT[index]

			bestOdds = self.bestOddsList[index]
			worstOdds = self.worstOddsList[index]

			if threshold[1] >= self.singleThreshold and result > 0.0:
				totalWins[0] += 1.0
				totalBestGain[0]  += (bestOdds-1.0)
				totalWorstGain[0] += (worstOdds-1.0)
				totalBets[0] += 1.0
			elif threshold[1] > self.singleThreshold and result < 1.0:
				totalLosses[0]   += 1.0
				totalBestGain[0]  -= 1.0
				totalWorstGain[0] -= 1.0
				totalBets[0] += 1.0
			else:
				totalIgnored  += 1.0
	
		print 'Bets:{0}, Won:{1}, Lost:{2}, Ignored:{3}, BestGain:{4:.2f}, WorstGain:{5:.2f}'.format(totalBets[0], \
			   totalWins[0], totalLosses[0], totalIgnored[0], totalBestGain[0], totalWorstGain[0])

