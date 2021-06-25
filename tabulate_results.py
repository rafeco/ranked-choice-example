#!/usr/bin/env python3

import generate_votes
import sqlite3

db = sqlite3.connect('./ranked_choices.db')
dbc = db.cursor()

def candidate_filter_clause(remaining_candidates):
    candidates_clause = ''

    if len(remaining_candidates) < len(generate_votes.candidates):
        candidates_clause = "WHERE candidate IN {}".format(tuple(remaining_candidates))

    return candidates_clause

def calculate_padding(remaining_candidates):
    l = -1

    for n in remaining_candidates:
        if len(n) > l:
            l = len(n)

    return l

def show_vote_totals(remaining_candidates):
    candidates_clause = candidate_filter_clause(remaining_candidates)

    padding = calculate_padding(remaining_candidates)

    sql = """WITH current_highest_rank AS (
	    SELECT ballot_id, MIN(rank) AS rank
	    FROM ranked_choices
        {}
	    GROUP BY ballot_id)
        SELECT candidate, COUNT(*) 
        FROM ranked_choices rc JOIN current_highest_rank c
        WHERE rc.ballot_id = c.ballot_id
        AND rc.rank = c.rank
        GROUP BY 1 ORDER BY 2 DESC""".format(candidates_clause)

    for row in dbc.execute(sql):
        print(f'{row[0]:<{padding}}  {row[1]}')

def remove_last_place_candidate(remaining_candidates):
    sql = """WITH current_highest_rank AS (
	    SELECT ballot_id, MIN(rank) AS rank
	    FROM ranked_choices
        {}
	    GROUP BY ballot_id)
        SELECT candidate, COUNT(*) AS votes
        FROM ranked_choices rc JOIN current_highest_rank c
        WHERE rc.ballot_id = c.ballot_id
        AND rc.rank = c.rank
        GROUP BY 1 ORDER BY 2 LIMIT 1""".format(candidate_filter_clause(remaining_candidates))

    dbc.execute(sql)
    row = dbc.fetchone()

    last_place = row[0]

    print(f"Removing last place finisher: {last_place}")
    remaining_candidates.remove(last_place)

    return remaining_candidates

def is_there_a_winner(remaining_candidates):
    sql = """WITH current_highest_rank AS (
	    SELECT ballot_id, MIN(rank) AS rank
	    FROM ranked_choices
        {}
	    GROUP BY ballot_id)
        SELECT candidate, COUNT(*) AS votes
        FROM ranked_choices rc JOIN current_highest_rank c
        WHERE rc.ballot_id = c.ballot_id
        AND rc.rank = c.rank
        GROUP BY 1 ORDER BY 2 DESC LIMIT 1""".format(candidate_filter_clause(remaining_candidates))

    dbc.execute(sql)
    row = dbc.fetchone()

    leader_votes = row[1]
    leader = row[0]

    sql = """WITH current_highest_rank AS (
	    SELECT ballot_id, MIN(rank) AS rank
	    FROM ranked_choices
        {}
	    GROUP BY ballot_id)
        SELECT COUNT(*) AS votes
        FROM ranked_choices rc JOIN current_highest_rank c
        WHERE rc.ballot_id = c.ballot_id
        AND rc.rank = c.rank
        LIMIT 1""".format(candidate_filter_clause(remaining_candidates))

    dbc.execute(sql)
    row = dbc.fetchone()

    total_votes = row[0]

    leader_percentage = float(leader_votes)/float(total_votes)

    if leader_percentage > 0.5:
        print(f'*** {leader} won the election with {leader_votes} of {total_votes} votes ({100 * leader_percentage:.2f}% of the total)')
        return True
    else:
        return False

def execute_round(remaining_candidates, round_number):
    print("\nStarting round number {}".format(str(round_number)))

    election_concluded = True

    show_vote_totals(remaining_candidates)

    election_concluded = is_there_a_winner(remaining_candidates)

    if not election_concluded:
        round_number = round_number + 1
        remaining_candidates = remove_last_place_candidate(remaining_candidates)
        execute_round(remaining_candidates, round_number)

def db_test():
    for row in dbc.execute('SELECT COUNT(*) FROM ranked_choices'):
        print(row)

def main():
    execute_round(list(generate_votes.candidates), 1)

if __name__ == "__main__":
    main()
