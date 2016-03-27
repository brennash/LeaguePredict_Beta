import re
import os
import logging
import json
import time
import pickle
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

	def __init__(self, model, featureSet): 
		featureList = featureSet.getFeaturesData()
		header = featureSet.getHeader()
		validCols = featureSet.getValidCols(homeResult=True)
		
		evaluationData = pandas.DataFrame(featureList, columns=header)
		evaluationResults = evaluationData['homeResult'].tolist()
		# evaluationPCA = pca.transform(evaluationData[validCols])
		predictions = model.predict(evaluationData[validCols])
		thresholds = model.predict_proba(evaluationData[validCols])

		worstOddsList = evaluationData['worstHomeOdds'].tolist()
		bestOddsList = evaluationData['bestHomeOdds'].tolist()

		right = 0.0
		wrong = 0.0
		totalBest = 0.0
		totalWorst = 0.0
		
		for index, prediction in enumerate(predictions):
			threshold = thresholds[index][1]
			print prediction, threshold, evaluationResults[index], worstOddsList[index]
			if prediction == 1.0 and prediction == 1.0:
				right += 1.0
				totalBest += (bestOddsList[index] - 1.0)
				totalWorst += (worstOddsList[index] - 1.0)
			elif prediction == 1.0 and prediction != 1.0:
				wrong += 1.0
				totalBest -= 1.0
				totalWorst -= 1.0
		
		print validCols
		print (right+wrong), right/(right+wrong), wrong/(right+wrong), totalBest, totalWorst



