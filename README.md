# Ludus 4 CTF

## What is it

Take a user file, formatted to : 

```csv
TeamName;Username
Team1;Toto
Team1;Tata
Team2;Tutu
...
```

Create the associated ludus users and config files :
- 1 Range per team
- 1 user per user

Gather the user wireguard config, option to edit the endpoint IP to a custom one/

## Setup

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

./ludus4ctf.py --help
```

## How to use

```sh
#todo
```

## References

- https://api-docs.ludus.cloud/
