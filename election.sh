#!/usr/bin/env bash

cd `dirname $0`

/usr/bin/env python generate_votes.py > ballots.csv

sqlite3 ranked_choices.db < import.sql

/usr/bin/env python tabulate_results.py
