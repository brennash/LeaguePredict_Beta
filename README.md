# LeaguePredict
LeaguePredict is an application which models various parameters in order to predict the likelihood of a 
home win, based on a large number of games from a variety of European football leagues. The basic operation 
of LeaguePredict is to take in a CSV file providing results for a particular league, generate a number 
of team/league based metrics, and use these in a logistic regression model to predict the liklihood of 
future home wins. 

# How it works
Basically the application works in three steps,

1. Create the set of features for each league data set provided.
2. Build a predictive model based on these features
3. Use this model to predict a number of evaluation fixtures. 


