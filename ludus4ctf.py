#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
# -*- coding: utf-8 -*-

from core import LudusAPI, Logger, parse_args

import json
import csv
import sys
import os


def check_csv(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if 'TeamName' not in row or 'Username' not in row:
                raise ValueError("CSV file must contain 'TeamName' and 'Username' columns")

def get_teams_from_csv(file_path):
    teams = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            team_name = row['TeamName']
            username = row['Username']
            if team_name not in teams:
                teams[team_name] = []
            teams[team_name].append(username)
    return teams

def list_users(ludus_api, logger):
    groups = ludus_api.get_groups(description_filter="ludus4ctf")
    for group in groups:
        print(f"{group.get('name')} (description: {group.get('description')})")
        users_in_group = ludus_api.get_group_users(group.get('name'))
        for user in users_in_group:
            print(f" - {user.get('name')} (userID: {user.get('userID')})")

def run(options, logger):
    ludus_api = LudusAPI(
        ludus_url=options.ludus_url,
        ludus_token=options.ludus_token,
        logger=logger
    )

    if options.command == "list":
        list_users(ludus_api, logger)
        sys.exit(0)

    if options.command == "add":
        if not options.input:
            logger.error("Input CSV file is required for 'add' command")
            sys.exit(1)
        check_csv(options.input)

        teams = get_teams_from_csv(options.input)
        existing_groups = ludus_api.get_groups(description_filter="ludus4ctf")
        existing_users = ludus_api.get_users()

        for team_name, usernames in teams.items():
            # Check if the group already exists in Ludus
            if team_name in [group.get('name') for group in existing_groups]:
                if options.force:
                    logger.warning(f"Group '{team_name}' already exists in Ludus. Deleting and recreating it")
                    # delete group and recreate it
                    ludus_api.delete_group(team_name)
                else:
                    logger.warning(f"Group '{team_name}' already exists in Ludus. Skipping group creation.")
                    continue
            
            group_details = ludus_api.create_group(team_name)

            team_userIDs = []
            for username in usernames:
                # Check if the user already exists in Ludus
                if username in [user.get('name') for user in existing_users]:
                    logger.debug(f"User '{username}' already exists in Ludus. Retrieving user details...")
                    user_details = next((user for user in existing_users if user.get('name') == username), None)
                    if options.force:
                        logger.warning(f"User '{username}' already exists in Ludus. Deleting and recreating it")
                        # delete user and recreate it
                        ludus_api.delete_user(user_details.get("userID"))
                    else:
                        print("here")
                        logger.warning(f"User '{username}' already exists in Ludus. Skipping user creation.")
                        continue
                
                user_details = ludus_api.create_user(username, team_name)
                user_id = user_details.get("userID")
                team_userIDs.append(user_id)

                logger.debug(f"User details for '{username}': {user_details}")

                file_content = ludus_api.generate_wireguard_config(user_id, options.public_ip)

                # Save the config to a file, pattern is output_folder/teamname/username_vpn.conf
                output_path = os.path.join(options.output, team_name, f"{username}_vpn.conf")
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, 'w') as config_file:
                    config_file.write(file_content)
                if options.verbose:
                    print(f"Generated WireGuard config for {username} saved to {output_path}")
            
            # Add the users to the group in Ludus
            ludus_api.add_users_to_group(team_name, team_userIDs)

if __name__ == "__main__":
    args = parse_args()
    logger = Logger("ludus4ctf", args.verbose)
    run(args, logger)