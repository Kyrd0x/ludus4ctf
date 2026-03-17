#!/bin/bash

# default tag is "ludus4ctf" but you can specify another tag as an argument, will be in descripion of the user
[...] --tag demo
# wrapper.sh bulk add teams.csv
ludus4ctf.py create all --csv teams.csv
# add only users without groups (teams)
ludus4ctf.py create users --csv teams.csv
# add only groups (teams) without users
ludus4ctf.py create groups --csv teams.csv

# --tag usable here, fallback to .env one or default "ludus4ctf"
ludus4ctf.py delete all
ludus4ctf.py delete users
ludus4ctf.py delete groups

# list groups/teams/ranges using default tag
ludus4ctf.py list
# list groups with sizes, using default tag
ludus4ctf.py list groups
# list ranges by team with status
ludus4ctf.py list ranges




ludus4ctf.py add --csv teams.csv
ludus4ctf.py delete
ludus4ctf.py list
ludus4ctf.py generate