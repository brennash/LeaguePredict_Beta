# LeaguePredict
LeaguePredict is an application which models various parameters in order to predict the likelihood of a 
home win, based on a large number of games from a variety of European football leagues. The basic operation 
of LeaguePredict is to take in a CSV file providing results for a particular league, generate a number 
of team/league based metrics, and use these in a logistic regression model to predict the liklihood of 
future home wins.

## Installation
To install this application you need to edit a couple of lines in the bin/run-script.sh file. 

```
# Edit these two variables to point at the install directory and config file
LEAGUE_PREDICT_DIR="/My/Path/ToApplication/LeaguePredict"
LEAGUE_PREDICT_CONF="$LEAGUE_PREDICT_DIR/conf/config.json"
```

# How it works
Basically the application works as follows,

1. Read in some fixture data into training and evaluation datasets.
2. Create a set of features from each dataset.  
3. Build a predictive model based on the training dataset features
4. Evaluate the model on the evaluation dataset features. 

## What is predicted?
The application predicts the likelihood of a home win for a given set of fixtures, in other words, the 
(rough) probability of the home team winning, given a set of historic performance metrics and league metrics. 
The reason home wins were selected is due to the inherent home advantage bias teams tend to have, which 
tends to widen the gap between good and bad teams performances. 

## What are the outputs
The outputs of the model is an evaluation of how the model would have won or lost accumulator 
bets respectively, given a set of prior evaluation data. In the example below, three accumulator bets would have 
been placed, at best odds of 1.92, 2.44 and 3.85, winning two and losing one. In this example, assuming
the same stake on each accumulator, a total of 2.77 profit would have been generated at best and 2.45 at 
worst. 

```
=== WIN: 4/4, BEST: 1.929, WORST: 1.611 ===
2016-01-08, Paris SG 2-0 Bastia 	(0.958), 1.12, 1.07
2016-01-09, Lyon 4-1 Troyes 		(0.769), 1.40, 1.33
2016-01-09, Barcelona 4-0 Granada 	(0.988), 1.07, 1.02
2016-01-09, Real Madrid 5-0 La Coruna 	(0.944), 1.15, 1.11

=== LOST: 1/5, BEST: 2.446, WORST: 2.048 ===
2016-01-15, Sp Lisbon 2-2 Tondela 	(0.868), 1.12, 1.08
2016-01-16, Napoli 3-1 Sassuolo 	(0.794), 1.31, 1.25
2016-01-16, Torino 4-2 Frosinone 	(0.810), 1.33, 1.29
2016-01-17, Barcelona 6-0 Ath Bilbao 	(0.949), 1.15, 1.12
2016-01-17, Real Madrid 5-1 Sp Gijon 	(0.990), 1.09, 1.05

=== WIN: 7/7, BEST: 3.858, WORST: 2.843 ===
2016-01-30, Dortmund 2-0 Ingolstadt 	  (0.886), 1.22, 1.15
2016-01-30, Leverkusen 3-0 Hannover 	  (0.760), 1.35, 1.25
2016-01-30, Roma 3-1 Frosinone 		  (0.914), 1.25, 1.20
2016-01-30, Sp Lisbon 3-2 Academica 	  (0.869), 1.17, 1.12
2016-01-31, Bayern Munich 2-0 Hoffenheim  (0.985), 1.11, 1.08
2016-01-31, Real Madrid 6-0 Espanol 	  (0.984), 1.11, 1.09
2016-01-31, Napoli 5-1 Empoli 		  (0.797), 1.30, 1.25
```

## Additional work (required)
Some kindly soul could take this codebase and augment it with a number of additional features as well as 
improve the ML libraries used to predict home wins. A couple of nice features immediately come to mind, 

* Calculating the distance teams have to travel to an away game as a feature. 
* Figuring out the distribution of goals for each team, and calculating an expected cumulative score for the fixture.
* Improving the K-means clustering for teams in the league.
* Adding the effect usually caused by a new manager joining.
* Adding a 'bounce' effect for teams that have avoided relegation or recently won the league.
* Improving the calculation of the 'winning streak' score.
