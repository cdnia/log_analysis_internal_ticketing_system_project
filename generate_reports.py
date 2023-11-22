#!/usr/bin/env python3


import re
import csv


error_list, user_list = [], []

with open("syslog.log", "r") as flog:
    for i in flog:
        current_line = i.strip()
