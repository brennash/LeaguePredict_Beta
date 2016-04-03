import datetime

class Bet:

	def __init__(self, result, date, homeTeam, awayTeam, homeFT, awayFT, prediction, threshold, configThreshold, bestOdds, worstOdds):
		self.resultList = []
		self.dateList   = []
		self.homeTeam   = []
		self.awayTeam   = []
		self.homeFT     = []
		self.awayFT     = []
		self.prediction = []
		self.threshold  = []
		self.configThreshold = []
		self.bestOdds   = []
		self.worstOdds  = []
		
		self.resultList.append(result)
		self.dateList.append(datetime.datetime.strptime(date, '%d/%m/%y'))
		self.homeTeam.append(homeTeam)
		self.awayTeam.append(awayTeam)
		self.homeFT.append(homeFT)
		self.awayFT.append(awayFT)
		self.prediction.append(prediction)
		self.threshold.append(threshold[1])
		self.configThreshold.append(configThreshold)
		self.bestOdds.append(bestOdds)
		self.worstOdds.append(worstOdds)


	def add(self, result, date, homeTeam, awayTeam, homeFT, awayFT, prediction, threshold, configThreshold, bestOdds, worstOdds):
		""" Add more bet details, essentially, add more bets to an 
			accumulator. 
		"""		
		self.resultList.append(result)
		self.dateList.append(datetime.datetime.strptime(date, '%d/%m/%y'))
		self.homeTeam.append(homeTeam)
		self.awayTeam.append(awayTeam)
		self.homeFT.append(homeFT)
		self.awayFT.append(awayFT)
		self.prediction.append(prediction)
		self.threshold.append(threshold[1])
		self.configThreshold.append(configThreshold)
		self.bestOdds.append(bestOdds)
		self.worstOdds.append(worstOdds)	

	def isValidDate(self, dateStr):
		""" Return true if the date can be considered as part of a 
		    weekly or weekend accumulator. Usually, there's two weekly 
		    predictions, one for Monday to Thurday and the other from 
		    Friday to Sunday. This function replicates this type of bi-weekly
		    betting pattern.
		"""
		date = datetime.datetime.strptime(dateStr, '%d/%m/%y')
		if len(self.resultList) == 0:
			return False
		else:
			prevDate = self.dateList[-1]
			if date < prevDate :
				return False
			else:
				weekday = date.weekday()
				prevWeekday = prevDate.weekday()
				daysAhead = (date - prevDate).days

				if weekday < 4 and prevWeekday < 4:
					if daysAhead < 4:
						return True
					else:
						return False
				elif weekday > 3 and prevWeekday > 3:
					if daysAhead < 3:
						return True
					else: 
						return False
				else:
					return False

	def printBet(self):
		wonTotal = 0
		lossTotal = 0
		wonAllBets = True
		bestTotal = 0.0
		worstTotal = 0.0
		startDate = self.dateList[0].strftime('%d/%m/%Y')
		endDate = self.dateList[-1].strftime('%d/%m/%Y')
	
		for index, result in enumerate(self.resultList):
			betThreshold = self.threshold[index]
			betThresholdLimit = self.configThreshold[index]
			bestOdds = self.bestOdds[index]
			worstOdds = self.worstOdds[index]
			
			if bestOdds == 0.0 or worstOdds == 0.0:
				print self.homeTeam[index],self.awayTeam[index],bestOdds, worstOdds
			#print betThreshold, type(betThreshold)
			#print betThresholdLimit, type(betThresholdLimit)
			
			if betThreshold >= betThresholdLimit:
				bestTotal += bestOdds
				worstTotal += worstOdds
				if result < 1.0:
					lossTotal += 1
					wonAllBets = False
				else:
					wonTotal += 1
					
		if wonAllBets and lossTotal == 0 and wonTotal > 0:
			print 'WON BET {0:.2f},{1:.2f},{2},{3},{4},{5},{6}'.format(bestTotal, 
				   worstTotal, (wonTotal+lossTotal), startDate, endDate, wonTotal, lossTotal)
		elif not wonAllBets and lossTotal > 0:
			print 'LOST BET {0:.2f},{1:.2f},{2},{3},{4},{5},{6}'.format(bestTotal, 
				   worstTotal, (wonTotal+lossTotal), startDate, endDate, wonTotal, lossTotal)


	def getTotalWins(self):
		totalWins = 0
		for index, result in enumerate(self.resultList):
			betThreshold = self.threshold[index]
			betThresholdLimit = self.configThreshold[index]
			if betThreshold >= betThresholdLimit:
				if result > 0.0:
					totalWins += 1
		return totalWins

	def getTotalLosses(self):
		totalLosses = 0
		for index, result in enumerate(self.resultList):
			betThreshold = self.threshold[index]
			betThresholdLimit = self.configThreshold[index]
			if betThreshold >= betThresholdLimit:
				if result < 1.0:
					totalLosses += 1
		return totalLosses

	def getTotalBets(self):
		totalBets = 0
		for index, result in enumerate(self.resultList):
			betThreshold = self.threshold[index]
			betThresholdLimit = self.configThreshold[index]
			if betThreshold >= betThresholdLimit:
				totalBets += 1
		return totalBets

	def isWin(self):
		for index, result in enumerate(self.resultList):
			betThreshold = self.threshold[index]
			betThresholdLimit = self.configThreshold[index]
			if betThreshold >= betThresholdLimit:
				if result < 1.0:
					return False
		return True

	def getBestOdds(self):
		oddsTotal = 0.0
		for index, odds in enumerate(self.bestOdds):
			if index == 0:
				oddsTotal = odds
			else:
				oddsTotal = oddsTotal*odds		
		return oddsTotal

	def getWorstOdds(self):
		oddsTotal = 0.0
		for index, odds in enumerate(self.worstOdds):
			if index == 0:
				oddsTotal = odds
			else:
				oddsTotal = oddsTotal*odds
		return oddsTotal
		
	def printDetails(self):
		totalBestOdds = self.getBestOdds()
		totalWorstOdds = self.getWorstOdds()
		winResult = self.isWin()
		totalBets = self.getTotalBets()
		totalWins = self.getTotalWins()
		totalLosses = self.getTotalLosses()
		
		if winResult:
			print '\n=== WIN: {0}/{1}, BEST: {2:.3f}, WORST: {3:.3f} ==='.format(totalWins, totalBets, totalBestOdds, totalWorstOdds)
		else:
			print '\n=== LOST: {0}/{1}, BEST: {2:.3f}, WORST: {3:.3f} ==='.format(totalLosses, totalBets, totalBestOdds, totalWorstOdds)
		
		for index, result in enumerate(self.resultList):
			fixtureDate = self.dateList[index].strftime('%Y-%m-%d')
			homeTeam = self.homeTeam[index]
			homeFT = self.homeFT[index]
			awayTeam = self.awayTeam[index]
			awayFT = self.awayFT[index]
			threshold = self.threshold[index]
			bestOdds = float(self.bestOdds[index])
			worstOdds = float(self.worstOdds[index])
			print '{0}, {1} {2}-{3} {4} \t({5:.3f}), {6:.2f}, {7:.2f}'.format(fixtureDate, homeTeam, homeFT, awayFT, awayTeam, threshold, bestOdds, worstOdds)
