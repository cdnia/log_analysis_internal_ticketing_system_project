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
                perso_dict = {"Username": reg_group_username, "INFO": 0,
                              "ERROR": 1}  # we initialize the error count to 1 and the info count to 0 because we
                # are in the case of an error
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
                perso_dict = {"Username": reg_group_username, "INFO": 1,
                              "ERROR": 0}  # we initialize the error count to 0 and the info count to 1 because we
                # are in the case of an info
                user_list.append(perso_dict)
            else:
                one_user_dict["INFO"] += 1
    error_list = sorted(error_list, key=lambda v1: v1["Count"], reverse=True)  # the reverse=True specify a descending
    # order
    user_list = sorted(user_list, key=lambda v1: v1["Username"])
    # we store the dictionaries in two different files: error_message.csv and user_statistics.csv
    with open("error_message.csv", "w", newline='') as r1, open("user_statistics.csv", "w", newline='') as r2:
        r1_fieldnames, r2_fieldnames = error_list[0].keys(), user_list[0].keys()
        r1_writer, r2_writer = csv.DictWriter(r1, r1_fieldnames), csv.DictWriter(r2, r2_fieldnames)
        r1_writer.writeheader(), r2_writer.writeheader()
        r1_writer.writerows(error_list), r2_writer.writerows(user_list)
