import re
import os
import logging
import json
import time
import pickle
import random
import pandas as pd
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

	def __init__(self, model, evaluationFeatures): 
		for feature in evaluationFeatures.getFeaturesList():
			feature.printFeature

	def printSummary(self):


	def predictFixtures(self, features, leagueFolder, fixturesFile) : 
		logging.basicConfig(filename='../logs/PredictFixtures.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y%m%d %H:%M:%S')

		print "Building the model..."

		# Read the features as CSV
		if self.csvFlag:
			with open(features) as f:
				featuresData = pd.DataFrame(pd.read_csv(features))
		# Read the features as JSON
		elif not self.csvFlag:
			with open(features) as f:
				featuresData = pd.DataFrame(json.loads(line) for line in f)
			logging.info('Training model on %i feature lines from %s', featuresData.shape[0], features)

		model, pca = self.fitLogisticRegressionModel(featuresData)
		
		# Pass the model to the fixture reader/league creator
		self.generatePredictions(model, pca, leagueFolder, fixturesFile)


	def generatePredictions(self, model, pca, leagueFolder, fixturesFile):
		""" This creates the current leagues and generates a features set
		    for each fixture.
		"""
		# The dict containing the leagues
		leagueList = {}

		print "Reading league data..."

		# Read in the league data and add them to the dict
		featureReader = FixturesToFeatures()
                for root, dirs, files in os.walk(leagueFolder, topdown=False):
                        for leagueFile in files:
				# Construct the fixture list
				filename = root+"/"+leagueFile
				filename = filename.replace("//","/")

		                # Generate the league data here
				if ".csv" in filename:
					fixtureList = self.getFixtureList(filename)
					leagueCode = fixtureList[0].getLeagueCode()
					seasonCode = fixtureList[0].getSeasonCode()
	
					# Instantiate the league
					league = League(leagueCode, seasonCode)
					league.addFixtures(fixtureList)
			
					# Add the instantiated league to the list
					leagueList[leagueCode] = league
		
		print "Predicting the fixtures..."

		# Read the fixtures to be predicted
		fixtureList = self.getFixtureList(fixturesFile, predictedFixture=True)
		featureList = []
		for fixture in fixtureList:
			leagueCode = fixture.getLeagueCode()
			seasonCode = fixture.getSeasonCode()
			homeTeam = fixture.getHomeTeam()
			awayTeam = fixture.getAwayTeam()
			league = leagueList[leagueCode]

			# Convert the features to a 
			featureSet = FeatureSet(seasonCode, leagueCode, fixture, league)
			jsonStr = featureSet.getJSONString()
			featureList.append(jsonStr)

		# Convert the list of feature to a pandas data frame
		featuresData = pd.DataFrame(json.loads(line) for line in featureList)
		dateList = featuresData['Date'].tolist()
		homeTeamList = featuresData['HomeTeam'].tolist()
		awayTeamList = featuresData['AwayTeam'].tolist()
		pcaFeatures = pca.transform(featuresData[self.validCols])
		predictions = model.predict(pcaFeatures)
		probabilities = model.predict_proba(pcaFeatures)

		for index, prediction in enumerate(predictions):
			if prediction > 0 :
				print '{0},{1},{2},{3},{4}'.format(predictions[index], probabilities[index][1], dateList[index], homeTeamList[index], awayTeamList[index])


	def getFixtureList(self, fileName, predictedFixture=False):
		""" Given a filename, returns a list of fixtures in this 
		    file, or None if nothing found.
		"""
		# Check to see if the file is valid
		if not os.path.isfile(fileName):
			logging.error("Problem trying to read from non-existant file %s", fileName)

		# Open the file
		file = open(fileName, "r")

		# The fixtures list
		fixtureList = []
		headerTokens = []
		completeFixtures = 0
		lineCount = 0

		# Read the line in the file
                for line in file:
			if lineCount == 0:
                                headerTokens = re.split(",", line)
                        else:
                                lineTokens = re.split(",", line)
                                fixture = Fixture(headerTokens, lineTokens)

				# If it's a predicted fixture and has yet to be played
				if predictedFixture:
	                                if fixture.isValid():
        	                                completeFixtures += 1
                	                        fixtureList.append(fixture)
	                                else:
					        logging.error("Ignoring Invalid Predicted Fixture %s",line)

				# Otherwise make sure there's goals scored
				else:
					if fixture.isValid() and fixture.hasScore():
        	                                completeFixtures += 1
                	                        fixtureList.append(fixture)
	                                else:
					        logging.error("Ignoring Invalid Fixture %s",line)
			lineCount += 1

                logging.info("Read %i complete fixtures from %i lines from %s", completeFixtures, lineCount, fileName)
		return fixtureList

	def fitLogisticRegressionModel(self, featuresData):
		trainingData, evaluationData = train_test_split(featuresData, test_size = 0.3)
		trainingResults = trainingData['Result'].tolist()
		model = linear_model.LogisticRegression(C=1e5)

		pca = decomposition.PCA(n_components=3)
		pca.fit(trainingData[self.validCols])
		trainingPCA = pca.transform(trainingData[self.validCols])
		evaluationPCA = pca.transform(evaluationData[self.validCols])
		
		model = model.fit(trainingPCA, trainingResults)
		predictions = model.predict(evaluationPCA)
		probabilities = model.predict_proba(evaluationPCA)

		worstOddsList = evaluationData['Home_WorstOdds'].tolist()
		bestOddsList = evaluationData['Home_BestOdds'].tolist()
		results = evaluationData['Result'].tolist()

		total = 0.0
		counter = 0.0
		bestList = []
		worstList = []

		for index, prediction in enumerate(predictions):
			result = results[index]
			probability = probabilities.tolist()[index]

			# The probability returned is a tuple, the prob of 0 and 
			# the probability of getting a 1
			if probability[1] > 0.7:
				counter += 1.0
				bestList.append(bestOddsList[index])
				worstList.append(worstOddsList[index])
				if result == 1:
					total += 1.0

		bestOdds = 1.0 / ( sum(bestList) / len(bestList) )
		worstOdds = 1.0 / ( sum(worstList) / len(worstList) ) 
		accuracy = (total/counter)
		accuracyDiff = round(accuracy-worstOdds,6)

		print bestOdds, worstOdds, accuracy, accuracyDiff, total, counter
		return model, pca

	def fitNaiveBayesModel(self, featuresData):
		bestModel = None
		bestAccuracy = 0.0

		for x in xrange(0,100):
			trainingData, evaluationData = train_test_split(featuresData, test_size = 0.3)
			trainingResults = trainingData['Result'].tolist()
			model = GaussianNB()
			model = model.fit(trainingData[self.validCols], trainingResults)
			predictions = model.predict(evaluationData[self.validCols])
			worstOddsList = evaluationData['Home_WorstOdds'].tolist()
			bestOddsList = evaluationData['Home_BestOdds'].tolist()
			results = evaluationData['Result'].tolist()

			total = 0.0
			counter = 0.0
			bestList = []
			worstList = []

			for index, prediction in enumerate(predictions):
				result = results[index]

				# Bet on game
				if prediction > 0.9999:
					counter += 1.0
					bestList.append(bestOddsList[index])
					worstList.append(worstOddsList[index])
					if result == 1:
						total += 1.0

			bestOdds = 1.0 / ( sum(bestList) / len(bestList) )
			worstOdds = 1.0 / ( sum(worstList) / len(worstList) ) 
			accuracy = (total/counter)
			accuracyDiff = round(accuracy-worstOdds,6)

			if accuracyDiff > bestAccuracy or bestModel is None:
				bestModel = model
				bestAccuracy = accuracyDiff

		return bestModel, bestAccuracy


	def fitRidgeRegressionModel(self, featuresData):
		bestModel = None
		bestAccuracy = 0.0

		for x in xrange(0,100):
			trainingData, evaluationData = train_test_split(featuresData, test_size = 0.3)
			trainingResults = trainingData['Result'].tolist()

			model = linear_model.Ridge(fit_intercept=False)
			model = model.fit(trainingData[self.validCols], trainingResults)
			predictions = model.predict(evaluationData[self.validCols])

			worstOddsList = evaluationData['Home_WorstOdds'].tolist()
			bestOddsList = evaluationData['Home_BestOdds'].tolist()
			results = evaluationData['Result'].tolist()

			total = 0.0
			counter = 0.0
			bestList = []
			worstList = []

			for index, prediction in enumerate(predictions.tolist()):
				result = results[index]

				# Bet on game
				if prediction > 0.9:
					counter += 1.0
					bestList.append(bestOddsList[index])
					worstList.append(worstOddsList[index])
					if result == 1:
						total += 1.0

			bestOdds = 1.0 / ( sum(bestList) / len(bestList) )
			worstOdds = 1.0 / ( sum(worstList) / len(worstList) ) 
			accuracy = (total/counter)
			accuracyDiff = round(accuracy-worstOdds,6)

			if accuracyDiff > bestAccuracy or bestModel is None:
				bestModel = model
				bestAccuracy = accuracyDiff

		return bestModel, bestAccuracy



	def fitEnsembleModel(self, ridgeModel, bayesModel, featuresData):
		trainingData, evaluationData = train_test_split(featuresData, test_size = 0.5)
		predictList1 = ridgeModel.predict(evaluationData[self.validCols])
		predictList2 = ridgeModel.predict(evaluationData[self.validCols])

		worstOddsList = evaluationData['Home_WorstOdds'].tolist()
		bestOddsList = evaluationData['Home_BestOdds'].tolist()
		resultsList = evaluationData['Result'].tolist()

		total = 0.0
		counter = 0.0
		bestList = []
		worstList = []

		for index in xrange(0, len(predictList1)):
			predict1 = predictList1[index]
			predict2 = predictList2[index]
			result = resultsList[index]

			# Bet on game
			if predict1 > 0.5 and predict2 > 0.5:
				counter += 1.0
				bestList.append(bestOddsList[index])
				worstList.append(worstOddsList[index])
				if result == 1:
					total += 1.0

		bestOdds = 1.0 / ( sum(bestList) / len(bestList) )
		worstOdds = 1.0 / ( sum(worstList) / len(worstList) ) 
		accuracy = (total/counter)
		accuracyDiff = round(accuracy-worstOdds,6)
		print accuracy, worstOdds, total, counter, accuracyDiff

		return accuracyDiff


		# Start iteration on the model training
#		for x in xrange(0,self.iterationLimit):
			# Split the data into training and evaluation data

			# Train the ridge regression model
			#ridgePredictions, ridgeModel = self.trainRidgeRegression(trainingData, evaluationData, self.validCols)
			#ridgeAccuracy = self.evaluateModel("Ridge_Regression", ridgePredictions, evaluationData, self.validCols)

			# Train the random forest model
			#forestPredictions, forestModel = self.trainRandomForestRegressor(trainingData, evaluationData, self.validCols)
			#forestAccuracy = self.evaluateModel("Random_Forest_Regressor", forestPredictions, evaluationData, self.validCols)

			# Naive Bayes classifier
#			predictions, probs, model = self.trainNaiveBayesModel(trainingData, evaluationData, self.validCols)
#			naiveBayesAccuracy = self.evaluateProbModel("Naive_Bayes", predictions, probs, evaluationData, self.validCols)

#			print naiveBayesAccuracy
			# Train the extra random forest model
			#extraForestPredictions, extraForestModel = self.trainExtraRandomForest(trainingData, evaluationData, self.validCols)
			#extraForestAccuracy = self.evaluateModel("Extra_Random_Forest", extraForestPredictions, evaluationData, self.validCols)

			# Train the decision tree model
			#decisionPredictions, decisionModel = self.trainDecisionTree(trainingData, evaluationData, self.validCols)
			#decisionAccuracy = self.evaluateModel("Decision_Tree", decisionPredictions, evaluationData, self.validCols)

			# Evaluate the ensemble model
			#ensembleAccuracy = self.evaluateEnsemble(ridgePredictions, forestPredictions, extraForestPredictions, decisionPredictions, evaluationData, self.validCols)

			#print "Results", ridgeAccuracy, forestAccuracy, extraForestAccuracy, decisionAccuracy, ensembleAccuracy
			##print "Results", ridgeAccuracy, forestAccuracy, naiveBayesAccuracy

		# Save out the model to file
		timestr = time.strftime("%Y%m%d_%H%M%S")

		filename = '../models/ridge_model_'+timestr+'.pkl'
		joblib.dump(bestRidge, filename)

		filename = '../models/forest_model_'+timestr+'.pkl'
		joblib.dump(bestForest, filename)

		filename = '../models/extra_forest_model_'+timestr+'.pkl'
		joblib.dump(bestExtraForest, filename)

		filename = '../models/decision_tree_model_'+timestr+'.pkl'
		joblib.dump(bestDecision, filename)

	def trainRidgeRegression(self, trainingData, evaluationData, validCols):
		""" Train the ridge regression model, and return the trained model
		"""
		# Get the results list
		trainingResults = trainingData['Result'].tolist()
		ridgeModel = linear_model.Ridge(fit_intercept=False)

		# Train the model
		start = time.clock()
		ridgeModel = ridgeModel.fit(trainingData[validCols],trainingResults)
		elapsed = (time.clock() - start)		
		logging.info('Ridge Regression - Training Time %f secs', elapsed)

		# Return the model predictions for evaluation
		return ridgeModel.predict(evaluationData[validCols]), ridgeModel

	def trainRandomForestRegressor(self, trainingData, evaluationData, validCols):
		""" Train the random forest model, and return the predictions and 
		    the instantiated trained model
		"""
		# Get the results list
		trainingResults = trainingData['Result'].tolist()
		nEstimators = 300
		logging.info('Random Forest - Model Iterations %i', nEstimators)
		forestModel = RandomForestRegressor(n_estimators = nEstimators, max_depth=None, min_samples_split=1, random_state=0)

		# Train the model
		start = time.clock()
		forestModel = forestModel.fit(trainingData[validCols],trainingResults)
		elapsed = (time.clock() - start)		
		logging.info('Random Forest - Training Time %f secs', elapsed)

		# Return the model predictions for evaluation
		return forestModel.predict(evaluationData[validCols]), forestModel

	def trainExtraRandomForest(self, trainingData, evaluationData, validCols):
		""" Train the extra random forest model, and return the predictions and 
		    the instantiated trained model
		"""
		# Get the results list
		trainingResults = trainingData['Result'].tolist()
		nEstimators = randint(50,1000)
		logging.info('Extra Random Forest - Model Iterations %i', nEstimators)
		extraModel = ExtraTreesClassifier(n_estimators= nEstimators, max_depth=None, min_samples_split=1, random_state=0)

		# Train the model
		start = time.clock()
		extraModel = extraModel.fit(trainingData[validCols],trainingResults)
		elapsed = (time.clock() - start)		
		logging.info('Extra Random Forest - Training Time %f secs', elapsed)

		# Return the model predictions for evaluation
		return extraModel.predict(evaluationData[validCols]), extraModel

	def trainDecisionTree(self, trainingData, evaluationData, validCols):
		""" Train the extra random forest model, and return the predictions and 
		    the instantiated trained model
		"""
		# Get the results list
		trainingResults = trainingData['Result'].tolist()
		decisionModel = DecisionTreeClassifier(max_depth=None, min_samples_split=1, random_state=0)

		# Train the model
		start = time.clock()
		decisionModel = decisionModel.fit(trainingData[validCols],trainingResults)
		elapsed = (time.clock() - start)		
		logging.info('Decision Tree - Training Time %f secs', elapsed)

		# Return the model predictions for evaluation
		return decisionModel.predict(evaluationData[validCols]), decisionModel

	def evaluateModel(self, modelName, predictions, evaluationData, validCols):
		""" Evaluate the output of the models, comparing the accuracy against
		    the probability ascribed by the odds.
		"""
		worstOddsList = evaluationData['Home_WorstOdds'].tolist()
		bestOddsList = evaluationData['Home_BestOdds'].tolist()
		results = evaluationData['Result'].tolist()

		total = 0.0
		counter = 0.0

		bestList = []
		worstList = []

		for index, prediction in enumerate(predictions):
			result = results[index]

			# Bet on game
			if prediction == 1:
				counter += 1.0
				bestList.append(bestOddsList[index])
				worstList.append(worstOddsList[index])
				if result > 0:
					total += 1.0

		accuracy = (total/counter)
		bestOdds = 1.0 / ( sum(bestList) / len(bestList) )
		worstOdds = 1.0 / ( sum(worstList) / len(worstList) ) 

		logging.info('%s, Correct %i, Total %i, Eval %i', modelName, total, counter, len(evaluationData) )
		logging.info('%s, Accuracy %f, BestOdds %f, WorstOdds %f', modelName, accuracy, bestOdds, worstOdds)
		logging.info('%s, WorstCaseDiff %f', modelName, round((accuracy-worstOdds),6) )
		return round((accuracy-worstOdds),6)

	def evaluateEnsemble(self, model1, model2, model3, model4, evaluationData, validCols):
		modelName = 'Ensemble'
		worstOddsList = evaluationData['Home_WorstOdds'].tolist()
		bestOddsList = evaluationData['Home_BestOdds'].tolist()
		results = evaluationData['Result'].tolist()

		total = 0.0
		counter = 0.0

		bestList = []
		worstList = []

		for index, prediction1 in enumerate(model1):
			prediction2 = model2[index]
			prediction3 = model3[index]
			prediction4 = model4[index]

			result = results[index]

			# Bet on game
			if prediction1 > 0.75 and prediction2 > 0.75 and prediction3 > 0.75 and prediction4 > 0.75:
				counter += 1.0
				bestList.append(bestOddsList[index])
				worstList.append(worstOddsList[index])
				if result > 0:
					total += 1.0

		accuracy = (total/counter)
		bestOdds = 1.0 / ( sum(bestList) / len(bestList) )
		worstOdds = 1.0 / ( sum(worstList) / len(worstList) ) 

		logging.info('%s, Correct %i, Total %i, Eval %i', modelName, total, counter, len(evaluationData) )
		logging.info('%s, Accuracy %f, BestOdds %f, WorstOdds %f', modelName, accuracy, bestOdds, worstOdds)
		logging.info('%s, WorstCaseDiff %f', modelName, round((accuracy-worstOdds),6) )
		return round((accuracy-worstOdds),6)

	def getRandomCols(self):
		validCols = []
		for col in self.columns:
			value = random.random()
			if value > 0.3:
				validCols.append(col)
		return validCols




	def logisticRegression(self, trainingResults, trainingData, evaluationResults, evaluationData):
		try:
			# Now the Logistic Regression Model
			logit = sm.Logit(trainingResults, trainingData[self.validCols])
 			logReg = logit.fit(disp=False)
			predictionsDF = logReg.predict(evaluationData[self.validCols])
			return predictionsDF.tolist()
		except KeyError:
			return None
	
	def predictEnsemble(self, randomForest, logisticRegression, evaluationData):
		results = evaluationData['Result'].tolist()
		#dates = evaluationData['Date'].tolist()
		#homeTeams = evaluationData['HomeTeam'].tolist()
		#awayTeams = evaluationData['AwayTeam'].tolist()
		#homeFT = evaluationData['HomeFT'].tolist()
		#awayFT = evaluationData['AwayFT'].tolist()
		oddsList = evaluationData['Home_WorstOdds'].tolist()

		hits = 0.0
		misses = 0.0
		oddsTotal = 0.0

		for index, LR_Prediction in enumerate(logisticRegression):
			RF_Prediction = randomForest[index]
			if LR_Prediction >= 0.75 and RF_Prediction > 0:
				# print results[index], LR_Prediction, dates[index], homeTeams[index], homeFT[index], awayFT[index], awayTeams[index], oddsList[index]
				if results[index] > 0.0:
					hits += 1.0
				else:
					misses += 1.0
	
				oddsTotal += oddsList[index]

##		print "TARGET:",(((hits+misses)/oddsTotal)),"RESULT:",hits/(hits+misses)
		targetResult = (hits+misses)/oddsTotal
		actualResult = hits/(hits+misses)
		diff = actualResult-targetResult
		return diff, targetResult, actualResult, hits


		# Instantiate the Random Forest Classifier
#		clf = RandomForestClassifier(n_jobs=2)
#		clf.fit(trainingData[validCols], resultData)
#
#		predictions = clf.predict(evaluationData[validCols])
#
#		hit = 0.0
#		miss = 0.0
#		totalOdds = 0.0
#		totalGames = 0.0
#		dfList = evaluationData['WorstHomeOdds'].tolist()
#		
#		for index, prediction in enumerate(predictions):
#			row = evaluationData.iloc[[index]]
#			result = actualResults[index]
#			odds = dfList[index]
#
#			totalOdds += 1.0/odds
#			totalGames += 1.0
#
#			if prediction == 1 and result == prediction:
#				hit += 1.0
#			elif prediction == 1 and result != prediction:
#				miss += 1.0
#
#		print "Bookies:",(totalOdds/totalGames), "Predictor:", (hit/(hit+miss))*100.0, "Total:", (hit+miss)


#		pd.crosstab(evalData['species'], preds, rownames=['actual'], colnames=['preds'])

