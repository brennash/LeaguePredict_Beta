class Bet:

	def __init__(self, type='single'):
		self.resultList = []
		self.type  		= type
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
		self.win        = False
		self.ignored    = True
		
	def addDetails(self, result, date, homeTeam, awayTeam, homeFT, awayFT, prediction, threshold, configThreshold, bestOdds, worstOdds):
		if self.type == 'single':
			self.resultList = [result]
			self.dateList   = [date]
			self.homeTeam   = [homeTeam]
			self.awayTeam   = [awayTeam]
			self.homeFT     = [homeFT]
			self.awayFT     = [awayFT]
			self.prediction = [prediction]
			self.threshold  = [threshold]
			self.configThreshold = [configThreshold]
			self.bestOdds   = [bestOdds]
			self.worstOdds  = [worstOdds]
			if threshold >= configThreshold:
				self.ignored = False
				if result > 0.0:
					self.win = True
				else:
					self.win = False
		else:
				self.resultList = []
		self.type  		= type
		self.dateList   = []
		self.homeTeam   = []
		self.awayTeam   = []
		self.homeFT     = []
		self.awayFT     = []
		self.prediction = []
		self.threshold  = []
		self.bestOdds   = []
		self.worstOdds  = []		

	def checkNextDate(self, dateStr):
		date = datetime.datetime.strptime(dateStr, '%d/%m/%y')
		if len(resultList) == 0:
			return True
		else:
			prevDate = dateList[-1]
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

