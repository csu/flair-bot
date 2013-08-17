#!/usr/bin/env python
'''
flair-bot.py
Christopher Su
Receives tasks via Reddit private message and applies flair accordingly.
'''

import praw
import AccountDetails

# global
r = None

def parseMessage(message_body):
    import StringIO
    import csv
    f = StringIO.StringIO(message_body)
    reader = csv.reader(f, delimiter=',')
    rowdata = []
    for row in reader:
        rowdata.append(row)
    return rowdata

def setFlair(sub, message_body):
    global r
    message_data = parseMessage(message_body)
    for task in message_data:
        r.set_flair(sub, task[0], AccountDetails.FLAIR_DICT[task[1]])

def main():
    global r
    r = praw.Reddit(user_agent='KCABot 1.0')
    r.login(AccountDetails.REDDIT_USERNAME, AccountDetails.REDDIT_PASSWORD)
    sub = AccountDetails.SUBREDDIT
    mods = r.get_moderators(sub)

    for msg in r.get_unread(limit=None):
        if msg.author in mods:
            if msg.subject == AccountDetails.ADD_COMMAND_1 or AccountDetails.ADD_COMMAND_2:
                setFlair(sub, msg.body)
            elif msg.subject == AccountDetails.REMOVE_COMMAND:
                removeFlair(sub, msg.body)

if __name__ == "__main__":
    main()