# LeaguePredict
Predicts the outcome of a various football league games, input as a series of individual games in a CSV format. 
The application basically performs a couple of tasks, 

* Reads in results data from a CSV file for a particular league
* Generates the league table and a number of team-specific metrics 
* Builds and trains a model on this data
* Uses the next set of team/league data to generate an evaluation feature set
* Performs an evaluation on this feature set

# Development
This application was the result of a long period of on-and-off development work. In fact, most people who've 
heard about it are probably sick of me yakking on about it at this stage. It was developed to test the concept 
of automatic market prediction (i.e., arbitrage) using real-time betting markets. However, the results of the 
model itself were good enough to make reasonable predictions in themselves before the match kicked off. 
