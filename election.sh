#!/usr/bin/env bash

cd `dirname $0`

/usr/bin/env python3 generate_votes.py $1 > ballots.csv

sqlite3 ranked_choices.db < import.sql

/usr/bin/env python3 tabulate_results.py
