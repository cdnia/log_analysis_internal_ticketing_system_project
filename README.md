# Project title : Log Analysis of an internal ticketing system with a python script
## Description of the project
Consider an internal ticketing system that is used by serveral teams in an enterprise.This system logs
events in a file called `syslog.log`. The file `syslog.log` contains useful information about tickets
such as who submitted the ticket, the ticket type (ERROR or INFO), when it was submitted, the ticket 
message, etc.

We write a python script called `generate_reports.py` that analyze the `syslog.log` file and produce 
reports depending on the information was extracted.<br>  
## Goal of the project
The role of our script is to generate two reports from the `syslog.log` file :
- the first report is a file called `error_message.csv`. Within that file there is a record of error
messages and their corresponding counts sorted with this criteria : the most common error to the least 
common error, without referencing users.
- the second report is a file called `user_statistics.csv`.