#!/bin/bash

# Edit these two variables to point at the install directory and config file
LEAGUE_PREDICT_DIR="/Users/brennash/Software/Python/LeaguePredict"
LEAGUE_PREDICT_CONF="$LEAGUE_PREDICT_DIR/conf/config.json"

# Sets the path to import the various modules
export PYTHONPATH="$PYTHONPATH:$LEAGUE_PREDICT_DIR"

if [[ -z $LEAGUE_PREDICT_DIR ]]
	then 
		echo "You need to specify the LEAGUE_PREDICT_DIR in the run-script.sh";
	else 
		if [[ -z $LEAGUE_PREDICT_CONF ]]
		then
			echo "You need to specify the LEAGUE_PREDICT_CONF configuration in the run-script.sh"
		else
			cd $LEAGUE_PREDICT_DIR
			python $LEAGUE_PREDICT_DIR/bin/LeaguePredict.py $LEAGUE_PREDICT_CONF
		fi
fi
