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
from leaguepredict.evaluation.Bet import Bet

class ModelEvaluation:


	def __init__(self, model, featureSet, evalutionConfig): 
		featureList = featureSet.getFeaturesData()
		header = featureSet.getHeader()		
		evaluationData = pandas.DataFrame(featureList, columns=header)
		
		# Get the JSON Config Parameters
		self.verbose = evalutionConfig['verbose']
		self.singleThreshold = evalutionConfig['single-threshold']
		self.accumThreshold = evalutionConfig['accumulator-threshold']

		validCols = featureSet.getValidCols(homeResult=True)
		self.evaluationResults = evaluationData['homeResult'].tolist()
		self.fixtureDates = evaluationData['date'].tolist()
		self.homeTeam = evaluationData['homeTeam'].tolist()
		self.awayTeam = evaluationData['awayTeam'].tolist()
		self.homeFT = evaluationData['homeFT'].tolist()
		self.awayFT = evaluationData['awayFT'].tolist()
				
		self.predictions = model.predict(evaluationData[validCols])
		self.thresholds = model.predict_proba(evaluationData[validCols])
		self.worstOddsList = evaluationData['worstHomeOdds'].tolist()
		self.bestOddsList = evaluationData['bestHomeOdds'].tolist()

		self.singleBetsList = []
		self.accumBetsList = []


	def startEvaluation(self):
		""" Calculates the accumulator and single bets for the predictions. 
			The gain and the total are dependent on the config inputs. 
		"""
		
		# Go through each prediction
		for index, result in enumerate(self.evaluationResults):
			result = self.evaluationResults[index]
			fixtureDate = self.fixtureDates[index]
			prediction = self.predictions[index]
			threshold = self.thresholds[index]
			homeTeam = self.homeTeam[index]
			awayTeam = self.awayTeam[index]
			homeFT = self.homeFT[index]
			awayFT = self.awayFT[index]
			bestOdds = self.bestOddsList[index]
			worstOdds = self.worstOddsList[index]
			
			# For each prediction test it's valid
			addedBet = False
			for bet in self.accumBetsList:
				if bet.isValidDate(fixtureDate):
					if threshold[1] >= self.accumThreshold:
						bet.add(result, fixtureDate, homeTeam, awayTeam, homeFT, awayFT, prediction, threshold, self.accumThreshold, bestOdds, worstOdds)
						addedBet = True
						break
			# Otherwise start an accumulator
			if not addedBet:
				if threshold[1] >= self.accumThreshold:
					bet = Bet(result, fixtureDate, homeTeam, awayTeam, homeFT, awayFT, prediction, threshold, self.accumThreshold, bestOdds, worstOdds)
					self.accumBetsList.append(bet)

		totalBestWins = 0.0
		totalWorstWins = 0.0
		for bet in self.accumBetsList:
			bet.printDetails()
			if bet.isWin():
				totalBestWins += (bet.getBestOdds() - 1.0)
				totalWorstWins += (bet.getWorstOdds() - 1.0)
			else:
				totalBestWins -= 1.0
				totalWorstWins -= 1.0
		
		print '\nWINNINGS BEST:{0:.3f}, WORST:{1:.3f}'.format(totalBestWins, totalWorstWins)