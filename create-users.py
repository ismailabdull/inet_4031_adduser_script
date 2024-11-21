#!/usr/bin/python3
#### Ismail Abdullahi
#### create-users.py
#### Program Creation Date: 11/14/2024
#### Program Last Updated Date: 11/20/2024

import os  # Used to execute system-level commands for creating users and groups.
import re  # Used for regular expressions to process and validate input data.
import sys  # Used to handle standard input (stdin) for processing input data dynamically.

def main():
    for line in sys.stdin:  # Reads each line from standard input (stdin).

        # This "regular expression" checks if the line starts with '#' (indicating a comment).
        # If a match is found, it means the line is a comment and should be skipped.
        match = re.match("^#", line)
        print("The contents of the match were: ", match)

        # This splits the input line into a list of fields using the ':' delimiter.
        # It ensures the line data can be processed into individual parts (username, password, etc.).
        fields = line.strip().split(':')

        # This IF statement checks if the line is a comment (match is not None) or
        # if the line does not contain exactly 5 fields. If either condition is true, the line is skipped.
        # It relies on the match result to skip comments and the fields split to validate input structure.
        if match or len(fields) != 5:
            continue

        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3],fields[2])
        groups = fields[4].split(',')
        print("==> Creating account for %s..." % (username))
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos,username)
        print cmd
        os.system(cmd)
        print("==> Setting the password for %s..." % (username))
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password,password,username)
        print cmd
        os.system(cmd)

        for group in groups:  # Loops through the list of groups the user should be added to.
            # This IF statement checks if the group is not '-', indicating valid group data.
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username, group))
                cmd = "/usr/sbin/adduser %s %s" % (username, group)
                print(cmd)  # Prints the command for debugging purposes.
                os.system(cmd)  # Executes the command to add the user to the group.


if __name__ == '__main__':
    main()

