#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
# -*- coding: utf-8 -*-

from core import Ludus, Logger, parse_args

import json
import csv
import sys
import os
import re


def check_csv(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if 'TeamName' not in row or 'Username' not in row:
                raise ValueError("CSV file must contain 'TeamName' and 'Username' columns")

def add_users_from_csv(ludus, logger, file_path):
    teams = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            team_name = row['TeamName']
            username = row['Username']
            if team_name not in teams:
                teams[team_name] = []
            teams[team_name].append(username)

    existing_groups = ludus.list_groups()
    existing_users = ludus.list_users()

    for team_name, usernames in teams.items():
        if any(group.get('name') == team_name for group in existing_groups):
            logger.warning(f"Group '{team_name}' already exists, skipping creation.")
        else:
            ludus.create_group(team_name)
            logger.success(f"Created group '{team_name}'")

        user_ids_to_add = []
        for username in usernames:
            user_id = ludus.generate_userid_from_username(username)
            if any(user.get('userID') == user_id for user in existing_users):
                logger.warning(f"User '{username}' (userID: {user_id}) already exists, skipping creation.")
            else:
                ludus.create_user(username)
                logger.debug(f"Created user '{username}' with userID '{user_id}'")
            
            user_ids_to_add.append(user_id)

        ludus.add_users_to_group(team_name, user_ids_to_add)
        logger.info(f"Added users {user_ids_to_add} to group '{team_name}'")

def generate_wireguard_configs(ludus, logger, output_dir, public_ip=None):
    os.makedirs(output_dir, exist_ok=True)

    logger.info(f"Generating WireGuard configs in '{output_dir}'")

    groups = ludus.list_groups()
    for group in groups:
        # Make a group subfolder
        group_folder = os.path.join(output_dir, group.get('name'))
        os.makedirs(group_folder, exist_ok=True)

        users_in_group = ludus.get_group_users(group.get('name'))
        for user in users_in_group:
            config = ludus.get_user_wireguard_config(user.get('userID'), public_ip)
            # write config to file named <username>.conf in output_dir/group_name/
            if config:
                config_path = os.path.join(group_folder, f"{user.get('name')}.conf")
                with open(config_path, 'w') as config_file:
                    config_file.write(config)
                logger.success(f"Generated WireGuard config at '{config_path}'")
            else:
                logger.error(f"Failed to get WireGuard config for user '{user.get('name')}' from group '{group.get('name')}' (userID: {user.get('userID')})")

if __name__ == "__main__":
    options = parse_args()
    logger = Logger(verbose=options.verbose)

    ludus = Ludus(
        ludus_url=options.ludus_url,
        ludus_token=options.ludus_token,
        tag=options.tag,
        logger=logger
    )

    if options.command == "list":
        groups = ludus.list_groups()
        for group in groups:
            print(f"{group.get('name')} (description: {group.get('description')})")
            users_in_group = ludus.get_group_users(group.get('name'))
            for user in users_in_group:
                print(f" - {user.get('name')} (userID: {user.get('userID')})")

        sys.exit(0)

    if options.command == "delete":
        groups = ludus.list_groups()
        for group in groups:
            ludus.delete_group(group.get('name'))
            logger.debug(f"Deleted group '{group.get('name')}'")

        sys.exit(0)

    if options.command == "add":
        if not options.csv:
            logger.error("Input CSV file is required for 'add' command")
            sys.exit(1)
        check_csv(options.csv)
        add_users_from_csv(ludus, logger, options.csv)

    if options.command == "generate":
        generate_wireguard_configs(ludus, logger, options.output, options.public_ip)