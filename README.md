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

## Additional work (required)
Some kindly soul could take this codebase and augment it with a number of additional features as well as 
improve the ML libraries used to predict home wins. A couple of nice features immediately come to mind, 

* Calculating the distance teams have to travel to an away game as a feature. 
* Figuring out the distribution of goals for each team, and calculating a cumulative score for the fixture.
* Improving the K-means clustering for teams in the league.
* Adding the effect usually caused by a new manager joining.
* Improving the calculation of the 'winning streak' score.  