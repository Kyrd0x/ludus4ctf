# Ludus4CTF

## What is it

Take a user file, formatted to : 

```csv
Teamame;Username
Team1;Toto
Team1;Tata
Team2;Tutu
```

Create the associated ludus groups and users :
- 1 Range per team
- 1 user per user

Gather the user wireguard config, option to edit the endpoint IP to a custom one/

## Setup

Install ludus client following the official [doc](https://docs.ludus.cloud/docs/quick-start/using-cli-locally#setting-up-the-ludus-client-locally)

```sh
git clone https://github.com/Kyrd0x/ludus4ctf.git
cd ludus4ctf/

python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# Then register argcomplete
eval "$(register-python-argcomplete ludus4ctf)"

# Rename env file template and edit it
mv .env.template .env

# Edit your ludus host url in the config, default might be straight good
mv config.yml.template config.yml

./ludus4ctf.py --help
```

## How to use

```sh
ludus4ctf.py add --csv teams.csv
ludus4ctf.py delete
ludus4ctf.py list
ludus4ctf.py generate
```

## References

- https://api-docs.ludus.cloud/
