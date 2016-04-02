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

	def checkDate(self, dateStr):
		date = datetime.datetime.strptime(dateStr, '%d/%m/%y')
		if len(self.resultList) == 0:
			return True
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
				   

	def getOdds(self):
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