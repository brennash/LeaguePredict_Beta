import unittest
from leaguepredict.data.Fixture import Fixture
from leaguepredict.data.Team import Team
import json

class Test(unittest.TestCase):

	def test_Team_1(self):
		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values = ["E0","26/03/08","Bohs","Rowfus","4","1","H","3","1","H","4","4","10","5","1.1","1.2"]
		fixture1 = Fixture(header, values)

		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values = ["E0","27/03/08","Bohs","Rowfus","5","2","H","3","1","H","4","4","10","5","1.1","1.2"]
		fixture2 = Fixture(header, values)

		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values = ["E0","28/03/08","Bohs","Rowfus","3","1","H","1","1","D","4","4","10","5","1.1","1.2"]
		fixture3 = Fixture(header, values)

		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values = ["E0","28/03/08","Bohs","Rowfus","3","1","H","2","1","H","4","4","10","5","1.1","1.2"]
		fixture4 = Fixture(header, values)

		team = Team("Bohs")

		team.addFixture(fixture1)
		team.addFixture(fixture2)
		team.addFixture(fixture3)
		team.addFixture(fixture4)

		self.assertEquals(team.getProbWin(), 1.0)

	def test_Team_2(self):
		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values = ["E0","26/03/08","Bohs","Rowfus","4","1","H","3","1","H","4","4","10","5","1.1","1.2"]
		fixture1 = Fixture(header, values)

		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values = ["E0","27/03/08","Bohs","Rowfus","5","2","H","3","1","H","4","4","10","5","1.1","1.2"]
		fixture2 = Fixture(header, values)

		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values = ["E0","28/03/08","Bohs","Rowfus","2","1","H","1","1","D","4","4","10","5","1.1","1.2"]
		fixture3 = Fixture(header, values)

		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values = ["E0","28/03/08","Bohs","Rowfus","2","1","H","2","1","H","4","4","10","5","1.1","1.2"]
		fixture4 = Fixture(header, values)

		team = Team("Bohs")
		team.addFixture(fixture1)
		team.addFixture(fixture2)
		team.addFixture(fixture3)
		team.addFixture(fixture4)
		self.assertEquals(team.getProbClearWin(), 0.5)


	def test_Team_2(self):
		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values = ["E0","26/03/08","Bohs","Rowfus","4","1","H","3","1","H","4","4","10","5","1.1","1.2"]
		fixture1 = Fixture(header, values)

		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values = ["E0","27/03/08","Bohs","Rowfus","5","2","H","3","1","H","4","4","10","5","1.1","1.2"]
		fixture2 = Fixture(header, values)

		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values = ["E0","28/03/08","Bohs","Rowfus","2","1","H","1","1","D","4","4","10","5","1.1","1.2"]
		fixture3 = Fixture(header, values)

		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values = ["E0","28/03/08","Bohs","Rowfus","2","1","H","2","1","H","4","4","10","5","1.1","1.2"]
		fixture4 = Fixture(header, values)

		team = Team("Rowfus")
		team.addFixture(fixture1)
		team.addFixture(fixture2)
		team.addFixture(fixture3)
		team.addFixture(fixture4)
		self.assertEquals(team.getProbClearLoss(), 0.5)


	def test_GetShots_1(self):
		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values = ["E0","26/03/08","Bohs","Rowfus","4","1","H","3","1","H","1","1","1","1","1.1","1.2"]
		fixture1 = Fixture(header, values)

		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values = ["E0","27/03/08","Bohs","Rowfus","5","2","H","3","1","H","1","1","1","1","1.1","1.2"]
		fixture2 = Fixture(header, values)

		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values = ["E0","28/03/08","Bohs","Rowfus","2","1","H","1","1","D","1","1","1","1","1.1","1.2"]
		fixture3 = Fixture(header, values)

		team = Team("Rowfus")
		team.addFixture(fixture1)
		team.addFixture(fixture2)
		team.addFixture(fixture3)

		self.assertEquals(team.getTotalShots(), 3)

	def test_GetShots_3(self):
		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values = ["E0","26/03/08","Bohs","Rowfus","4","1","H","3","1","H","1","1","4","1","1.1","1.2"]
		fixture1 = Fixture(header, values)

		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values = ["E0","27/03/08","Bohs","Rowfus","5","2","H","3","1","H","1","1","1","1","1.1","1.2"]
		fixture2 = Fixture(header, values)

		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values = ["E0","28/03/08","Bohs","Rowfus","2","1","H","1","1","D","1","1","1","1","1.1","1.2"]
		fixture3 = Fixture(header, values)

		team = Team("Rowfus")
		team.addFixture(fixture1)
		team.addFixture(fixture2)
		team.addFixture(fixture3)

		total = fixture1.getHomeShots()
		total += fixture2.getHomeShots()
		total += fixture3.getHomeShots()

		self.assertEquals(total, 6)

	def test_GetTotalShots_1(self):
		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values = ["E0","26/03/08","Bohs","Rowfus","4","1","H","3","1","H","1","1","4","1","1.1","1.2"]
		fixture1 = Fixture(header, values)

		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values = ["E0","27/03/08","Bohs","Rowfus","5","2","H","3","1","H","1","1","1","1","1.1","1.2"]
		fixture2 = Fixture(header, values)

		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values = ["E0","28/03/08","Bohs","Rowfus","2","1","H","1","1","D","1","1","1","1","1.1","1.2"]
		fixture3 = Fixture(header, values)

		team = Team("Rowfus")
		team.addFixture(fixture1)
		team.addFixture(fixture2)
		team.addFixture(fixture3)

		self.assertEquals(team.getTotalShotsTarget(), 3)

	def test_GetPreviousWins_1(self):
		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values1 = ["E0","26/03/08","Bohs","Rowfus","2","2","H","0","1","H","1","1","4","1","1.1","1.2"]
		values2 = ["E0","27/03/08","Bohs","Rowfus","2","1","H","1","1","H","1","1","1","1","1.1","1.2"]
		values3 = ["E0","28/03/08","Bohs","Rowfus","2","1","H","1","1","D","1","1","1","1","1.1","1.2"]

		fixture1 = Fixture(header, values1)
		fixture2 = Fixture(header, values2)
		fixture3 = Fixture(header, values3)

		team = Team("Bohs")
		team.addFixture(fixture1)
		team.addFixture(fixture2)
		team.addFixture(fixture3)

		result = team.getPreviousWins(1)
		self.assertEquals(result, 1)

	def test_GetPreviousWins_2(self):
		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values1 = ["E0","26/03/08","Bohs","Rowfus","2","2","H","0","1","H","1","1","4","1","1.1","1.2"]
		values2 = ["E0","27/03/08","Bohs","Rowfus","2","2","H","1","1","H","1","1","1","1","1.1","1.2"]
		values3 = ["E0","28/03/08","Bohs","Rowfus","2","1","H","1","1","D","1","1","1","1","1.1","1.2"]

		fixture1 = Fixture(header, values1)
		fixture2 = Fixture(header, values2)
		fixture3 = Fixture(header, values3)

		team = Team("Bohs")
		team.addFixture(fixture1)
		team.addFixture(fixture2)
		team.addFixture(fixture3)

		result = team.getPreviousWins(2)
		self.assertEquals(result, 0)

	def test_GetPreviousWins_3(self):
		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values1 = ["E0","26/03/08","Bohs","Rowfus","2","1","H","0","1","H","1","1","4","1","1.1","1.2"]
		values2 = ["E0","27/03/08","Bohs","Rowfus","2","2","H","1","1","H","1","1","1","1","1.1","1.2"]
		values3 = ["E0","28/03/08","Bohs","Rowfus","2","2","H","1","1","D","1","1","1","1","1.1","1.2"]

		fixture1 = Fixture(header, values1)
		fixture2 = Fixture(header, values2)
		fixture3 = Fixture(header, values3)

		team = Team("Bohs")
		team.addFixture(fixture1)
		team.addFixture(fixture2)
		team.addFixture(fixture3)

		result = team.getPreviousWins(3)
		self.assertEquals(result, 1)

	def test_GetPreviousLosses_1(self):
		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values1 = ["E0","28/03/08","Bohs","Rowfus","2","1","H","1","1","D","1","1","1","1","1.1","1.2"]
		fixture1 = Fixture(header, values1)
		team = Team("Rowfus")
		team.addFixture(fixture1)
		result = team.getPreviousLosses(1)
		self.assertEquals(result, 1)

	def test_GetPreviousLosses_2(self):
		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values1 = ["E0","28/03/08","Bohs","Rowfus","2","1","H","1","1","D","1","1","1","1","1.1","1.2"]
		values2 = ["E0","28/03/08","Bohs","Rowfus","2","2","H","1","1","D","1","1","1","1","1.1","1.2"]
		fixture1 = Fixture(header, values1)
		fixture2 = Fixture(header, values2)
		team = Team("Rowfus")
		team.addFixture(fixture2)
		result = team.getPreviousLosses(1)
		self.assertEquals(result, 0)

	def test_GetPreviousLosses_3(self):
		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values1 = ["E0","26/03/08","Bohs","Rowfus","2","2","H","0","1","H","1","1","4","1","1.1","1.2"]
		values2 = ["E0","27/03/08","Bohs","Rowfus","2","1","H","1","1","H","1","1","1","1","1.1","1.2"]
		values3 = ["E0","28/03/08","Bohs","Rowfus","2","2","H","1","1","D","1","1","1","1","1.1","1.2"]

		fixture1 = Fixture(header, values1)
		fixture2 = Fixture(header, values2)
		fixture3 = Fixture(header, values3)

		team = Team("Rowfus")
		team.addFixture(fixture1)
		team.addFixture(fixture2)
		team.addFixture(fixture3)

		result = team.getPreviousLosses(2)
		self.assertEquals(result, 1)


	def test_GetPreviousLosses_4(self):
		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values1 = ["E0","26/03/08","Bohs","Rowfus","2","1","H","0","1","H","1","1","4","1","1.1","1.2"]
		values2 = ["E0","27/03/08","Bohs","Rowfus","2","2","H","1","1","H","1","1","1","1","1.1","1.2"]
		values3 = ["E0","28/03/08","Bohs","Rowfus","2","2","H","1","1","D","1","1","1","1","1.1","1.2"]
		values4 = ["E0","01/04/08","Bohs","Rowfus","2","2","H","1","1","D","1","1","1","1","1.1","1.2"]

		fixture1 = Fixture(header, values1)
		fixture2 = Fixture(header, values2)
		fixture3 = Fixture(header, values3)
		fixture4 = Fixture(header, values3)

		team = Team("Rowfus")
		team.addFixture(fixture1)
		team.addFixture(fixture2)
		team.addFixture(fixture3)
		team.addFixture(fixture4)

		result = team.getPreviousLosses(4)
		self.assertEquals(result, 1)

	def test_GetPreviousLosses_5(self):
		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values1 = ["E0","26/03/08","Bohs","Rowfus","2","2","H","0","1","H","1","1","4","1","1.1","1.2"]
		values2 = ["E0","27/03/08","Bohs","Rowfus","2","1","H","1","1","H","1","1","1","1","1.1","1.2"]
		values3 = ["E0","28/03/08","Bohs","Rowfus","2","1","H","1","1","D","1","1","1","1","1.1","1.2"]

		fixture1 = Fixture(header, values1)
		fixture2 = Fixture(header, values2)
		fixture3 = Fixture(header, values3)

		team = Team("Rowfus")
		team.addFixture(fixture1)
		team.addFixture(fixture2)
		team.addFixture(fixture3)

		result = team.getPreviousLosses(3)
		self.assertEquals(result, 0)

	def test_GetPreviousResults_1(self):
		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		values1 = ["E0","26/03/08","Bohs","Rowfus","2","1","H","0","1","H","1","1","4","1","1.1","1.2"]
		values2 = ["E0","27/03/08","Bohs","Rowfus","2","1","H","1","1","H","1","1","1","1","1.1","1.2"]
		values3 = ["E0","28/03/08","Bohs","Rowfus","2","1","H","1","1","D","1","1","1","1","1.1","1.2"]

		fixture1 = Fixture(header, values1)
		fixture2 = Fixture(header, values2)
		fixture3 = Fixture(header, values3)

		team = Team("Rowfus")
		team.addFixture(fixture1)
		team.addFixture(fixture2)
		team.addFixture(fixture3)

		results = team.getPreviousResults()
		result = True
		for testResult in results:
			if testResult != 'L':
				result = False
				break

		if len(results) != 3:
			result = False
					
		self.assertTrue(result)


	def test_RecentProbWin_1(self):
		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		win = ["E0","26/03/08","Bohs","Rowfus","2","1","H","0","1","H","1","1","4","1","1.1","1.2"]
		loss = ["E0","26/03/08","Bohs","St. Pauli","2","3","H","0","1","H","1","1","4","1","1.1","1.2"]

		fixture1 = Fixture(header, loss)
		fixture2 = Fixture(header, win)
		fixture3 = Fixture(header, win)
		fixture4 = Fixture(header, win)
		fixture5 = Fixture(header, win)
		fixture6 = Fixture(header, win)
		fixture7 = Fixture(header, win)

		team = Team("Bohs")
		team.addFixture(fixture1)
		team.addFixture(fixture2)
		team.addFixture(fixture3)
		team.addFixture(fixture4)
		team.addFixture(fixture5)
		team.addFixture(fixture6)
		team.addFixture(fixture7)

		result = team.getRecentProbWin()
		self.assertEquals(result, 1.0)


	def test_RecentPoints_1(self):
		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		win = ["E0","26/03/08","Bohs","Rowfus","2","1","H","0","1","H","1","1","4","1","1.1","1.2"]
		loss = ["E0","26/03/08","Bohs","St. Pauli","2","3","H","0","1","H","1","1","4","1","1.1","1.2"]

		fixture1 = Fixture(header, loss)
		fixture2 = Fixture(header, win)
		fixture3 = Fixture(header, win)
		fixture4 = Fixture(header, loss)
		fixture5 = Fixture(header, loss)
		fixture6 = Fixture(header, loss)
		fixture7 = Fixture(header, loss)

		team = Team("Bohs")
		team.addFixture(fixture1)
		team.addFixture(fixture2)
		team.addFixture(fixture3)
		team.addFixture(fixture4)
		team.addFixture(fixture5)
		team.addFixture(fixture6)
		team.addFixture(fixture7)

		result = team.getRecentPoints()
		self.assertEquals(result, 3)


	def test_RecentGF_1(self):
		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		win = ["E0","26/03/08","Bohs","Rowfus","1","0","H","0","0","H","1","1","4","1","1.1","1.2"]
		loss = ["E0","26/03/08","Bohs","St. Pauli","0","3","H","0","1","H","1","1","4","1","1.1","1.2"]

		fixture1 = Fixture(header, loss)
		fixture2 = Fixture(header, loss)
		fixture3 = Fixture(header, loss)
		fixture4 = Fixture(header, loss)
		fixture5 = Fixture(header, win)
		fixture6 = Fixture(header, win)
		fixture7 = Fixture(header, loss)

		team = Team("Bohs")
		team.addFixture(fixture1)
		team.addFixture(fixture2)
		team.addFixture(fixture3)
		team.addFixture(fixture4)
		team.addFixture(fixture5)
		team.addFixture(fixture6)
		team.addFixture(fixture7)

		result = team.getRecentGF()
		self.assertEquals(result, 2)

	def test_RecentGA_1(self):
		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		win = ["E0","26/03/08","Bohs","Rowfus","2","1","H","0","0","H","1","1","4","1","1.1","1.2"]
		loss = ["E0","26/03/08","Bohs","St. Pauli","0","3","H","0","1","H","1","1","4","1","1.1","1.2"]

		fixture1 = Fixture(header, loss)
		fixture2 = Fixture(header, loss)
		fixture3 = Fixture(header, loss)
		fixture4 = Fixture(header, loss)
		fixture5 = Fixture(header, win)
		fixture6 = Fixture(header, win)
		fixture7 = Fixture(header, loss)

		team = Team("Bohs")
		team.addFixture(fixture1)
		team.addFixture(fixture2)
		team.addFixture(fixture3)
		team.addFixture(fixture4)
		team.addFixture(fixture5)
		team.addFixture(fixture6)
		team.addFixture(fixture7)

		result = team.getRecentGA()
		self.assertEquals(result, 11)


	def test_GetForm_1(self):
		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		win = ["E0","26/03/08","Bohs","Rowfus","2","1","H","0","0","H","1","1","4","1","1.1","1.2"]
		loss = ["E0","26/03/08","Bohs","St. Pauli","0","3","H","0","1","H","1","1","4","1","1.1","1.2"]
		team = Team("Bohs")
		
		for x in xrange(0, 20):
			fixture = Fixture(header, win)
			team.addFixture(fixture)

		result = team.getForm(5)
		self.assertTrue(result > 0.999 and result < 1.0001)

	def test_GetForm_2(self):
		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		win = ["E0","26/03/08","Bohs","Rowfus","2","1","H","0","0","H","1","1","4","1","1.1","1.2"]
		loss = ["E0","26/03/08","Bohs","St. Pauli","0","3","H","0","1","H","1","1","4","1","1.1","1.2"]
		team = Team("Bohs")
		
		for x in xrange(0, 20):
			fixture = Fixture(header, loss)
			team.addFixture(fixture)

		result = team.getForm(5)
		self.assertTrue(result >= 0.0 and result < 0.0001)

	def test_GetForm_3(self):
		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		win = ["E0","26/03/08","Bohs","Rowfus","2","1","H","0","0","H","1","1","4","1","1.1","1.2"]
		loss = ["E0","26/03/08","Bohs","St. Pauli","0","3","H","0","1","H","1","1","4","1","1.1","1.2"]
		team = Team("Bohs")
		
		for x in xrange(0, 20):
			fixture1 = Fixture(header, win)
			fixture2 = Fixture(header, loss)
			team.addFixture(fixture2)
			team.addFixture(fixture1)

		result = team.getForm(5)
		self.assertTrue(result > 0.45 and result < 0.65)

	def test_GetForm_4(self):
		header = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","HST","AST","HS","AS","WHH","B365A"]
		win = ["E0","26/03/08","Bohs","Rowfus","2","1","H","0","0","H","1","1","4","1","1.1","1.2"]
		loss = ["E0","26/03/08","Bohs","St. Pauli","0","3","H","0","1","H","1","1","4","1","1.1","1.2"]
		team = Team("Bohs")
		
		fixture1 = Fixture(header, win)
		fixture2 = Fixture(header, loss)
		team.addFixture(fixture2)
		team.addFixture(fixture1)

		result = team.getForm(5)
		self.assertEquals(result, 0.0)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
