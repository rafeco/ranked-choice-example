# ranked-choice-example

Generate ranked choice ballots and tabulate them.

To try it out, just download it and run the `election.sh` script. You can also 
pass a vote count to the script to conduct an election with a specific number of 
ballots. The candidates are hard-coded in `generate_votes.py`.

The way the election works is as follows:

* Each round, the ballots are counted, with the highest ranked candidate still in the race getting the vote on each ballot.
* If no candidate has more than 50% of the votes, the lowest vote recipient is removed, and the votes are recounted.

Requires Python 3 and SQLite 3.
