#!/usr/bin/env python3


import re
import csv


error_list, user_list = [], []

with open("syslog.log", "r") as flog:
    for i in flog:
        current_line = i.strip()
        my_reg_error = re.search(r"ticky: ERROR ([\w' ]*) \(([\w .]*)\)", current_line)
        my_reg_user = re.search(r"ticky: INFO ([\w ]*) \[#\d+] \(([\w .]*)\)", current_line)
