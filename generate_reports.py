#!/usr/bin/env python3
"""
Log Analysis Tool for Internal Ticketing System.

This script analyzes syslog files from an internal ticketing system and
generates two CSV reports:
1. error_message.csv - Error messages sorted by frequency (descending)
2. user_statistics.csv - User statistics sorted by username (ascending)

Usage:
    python generate_reports.py
"""

# Standard library imports
import csv
import re
import sys

from pathlib import Path

# Define file paths using pathlib
log_file = Path("syslog.log")
error_csv = Path("error_message.csv")
user_csv = Path("user_statistics.csv")

error_list, user_list = [], []


ERROR_PATTERN = r"ticky: ERROR ([\w' ]*) \(([\w .]*)\)"
INFO_PATTERN = r"ticky: INFO ([\w ]*) \[#\d+] \(([\w .]*)\)"


if __name__ == '__main__':
    # Validate that log file exists before processing
    if not log_file.exists():
        print(f"Error: Log file '{log_file}' not found!")
        sys.exit(1)
        
    with log_file.open("r", encoding="utf-8") as flog:
        for line in flog:
            current_line = line.strip()  # Remove leading/trailing whitespace
            # we declare two regex variables respectively for error and info patterns.
            error_match = re.search(ERROR_PATTERN, current_line)
            info_match = re.search(INFO_PATTERN, current_line)
            if error_match is not None:
                message, username = error_match.groups()[0].strip(), error_match.groups()[1].strip()
                one_user_dict = next((j for j in user_list if j["Username"] == username), False)
                one_error_dict = next((k for k in error_list if k["Error"] == message), False)
                if not one_user_dict:
                    perso_dict = {"Username": username, "INFO": 0,
                                "ERROR": 1}
                    user_list.append(perso_dict)
                else:
                    one_user_dict["ERROR"] += 1
                if not one_error_dict:
                    error_dict = {"Error": message, "Count": 1}
                    error_list.append(error_dict)
                else:
                    one_error_dict["Count"] += 1
            elif info_match is not None:
                message, username = info_match.groups()[0].strip(), info_match.groups()[1].strip()
                one_user_dict = next((j for j in user_list if j["Username"] == username), False)
                if not one_user_dict:
                    perso_dict = {"Username": username, "INFO": 1,
                                "ERROR": 0}
                    user_list.append(perso_dict)
                else:
                    one_user_dict["INFO"] += 1
                    error_list = sorted(error_list, key=lambda v1: v1["Count"], reverse=True)
        user_list = sorted(user_list, key=lambda v1: v1["Username"])
        # we store the dictionaries in two different files: error_message.csv and user_statistics.csv
        with error_csv.open("w", newline='', encoding="utf-8") as error_file, user_csv.open("w", newline='', encoding="utf-8") as user_file:
            error_fieldnames, user_fieldnames = error_list[0].keys(), user_list[0].keys()
            error_writer, user_writer = csv.DictWriter(error_file, error_fieldnames), csv.DictWriter(user_file, user_fieldnames)
            error_writer.writeheader(), user_writer.writeheader()
            error_writer.writerows(error_list), user_writer.writerows(user_list)
