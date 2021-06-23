#!/usr/bin/env python

import generate_votes
import sqlite3

db = sqlite3.connect('./ranked_choices.db')
dbc = db.cursor()

def db_test():
    for row in dbc.execute('SELECT COUNT(*) FROM ranked_choices'):
        print(row)

def main():
    candidates = generate_votes.candidates

    db_test();

if __name__ == "__main__":
    main()
