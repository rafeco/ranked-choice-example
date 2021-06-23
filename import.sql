CREATE TABLE IF NOT EXISTS ranked_choices (
   	ballot_id INTEGER NOT NULL,
	rank INTEGER NOT NULL,
	candidate TEXT NOT NULL
);

DELETE FROM ranked_choices;

.mode csv
.import ballots.csv ranked_choices
SELECT COUNT(*) FROM ranked_choices
