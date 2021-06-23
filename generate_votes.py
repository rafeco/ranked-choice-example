#!/usr/bin/env python

import random

candidates = ["Eric Adams", "Maya Wiley", "Kathryn Garcia", "Andrew Yang", "Scott Stringer", 
        "Dianne Morales", "Raymond McGuire", "Shaun Donovan", "Aaron Fondenauer", 
        "Art Chang", "Paperboy Prince", "Joycelyn Taylor", "Isaac Wright"]

def make_ballot():
    return random.sample(candidates, k=random.randint(1, 5))

def format_ballot(ballot):
    records = []
    for i, name in enumerate(ballot):
        records.append(str(i + 1) + "," + name)
    return records

def main():
    for n in range(0, 10000):
        ballot = make_ballot()

        records = format_ballot(ballot)

        for r in records:
            print(str(n) + "," + r)

if __name__ == "__main__":
    main()
