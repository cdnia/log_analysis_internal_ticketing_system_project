#!/usr/bin/env python3


import re
import csv


error_list, user_list = [], []

with open("syslog.log", "r") as flog:
    for i in flog:
        current_line = i.strip()  # we strip the current log line.
        my_reg_error = re.search(r"ticky: ERROR ([\w' ]*) \(([\w .]*)\)", current_line)
        my_reg_user = re.search(r"ticky: INFO ([\w ]*) \[#\d+] \(([\w .]*)\)", current_line)
        if my_reg_error is not None:
            reg_group_error, reg_group_username = my_reg_error.groups()[0].strip(), my_reg_error.groups()[1].strip()
            one_user_dict = next((j for j in user_list if j["Username"] == reg_group_username), False)
            one_error_dict = next((k for k in error_list if k["Error"] == reg_group_error), False)
            if not one_user_dict:
                perso_dict = {"Username": reg_group_username, "INFO": 0, "ERROR": 1}
                user_list.append(perso_dict)
            else:
                one_user_dict["ERROR"] += 1
            if not one_error_dict:
                error_dict = {"Error": reg_group_error, "Count": 1}
                error_list.append(error_dict)
            else:
                one_error_dict["Count"] += 1
        elif my_reg_user is not None:
            reg_group_error, reg_group_username = my_reg_user.groups()[0].strip(), my_reg_user.groups()[1].strip()
            one_user_dict = next((j for j in user_list if j["Username"] == reg_group_username), False)
            if not one_user_dict:
                perso_dict = {"Username": reg_group_username, "INFO": 1, "ERROR": 0}
                user_list.append(perso_dict)
            else:
                one_user_dict["INFO"] += 1
    error_list = sorted(error_list, key=lambda v1: v1["Count"], reverse=True)  # the reverse=True specify a descending
    # order
    user_list = sorted(user_list, key=lambda v1: v1["Username"])
    # we store the dictionaries in two different files: error_message.csv and user_statistics.csv
    with open("error_message.csv", "w", newline='') as r1, open("user_statistics.csv", "w", newline='') as r2:
        r1_fieldnames, r2_fieldnames = error_list[0].keys(), user_list[0].keys()
        r1_writer = csv.DictWriter(r1, r1_fieldnames)
        r2_writer = csv.DictWriter(r2, r2_fieldnames)
