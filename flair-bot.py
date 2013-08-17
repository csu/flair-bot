#!/usr/bin/env python
'''
flair-bot.py
Christopher Su
Receives commands via Reddit private message and applies flair accordingly.
'''

import praw
import logging
import os
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
        r.set_flair(sub, task[0], flair_css_class=AccountDetails.FLAIR_DICT[task[1]])

def removeFlair(sub, message_body):
    global r
    message_data = parseMessage(message_body)
    for task in message_data:
        r.delete_flair(sub, task[0])

def main():
    global r
    r = praw.Reddit(user_agent='Subot 1.0')
    r.login(AccountDetails.REDDIT_USERNAME, AccountDetails.REDDIT_PASSWORD)
    sub = AccountDetails.SUBREDDIT
    mods = r.get_moderators(sub)

    for msg in r.get_unread(limit=None):
        if msg.author in mods:
            if msg.subject == AccountDetails.ADD_COMMAND_1 or msg.subject == AccountDetails.ADD_COMMAND_2:
                setFlair(sub, msg.body)
            elif msg.subject == AccountDetails.REMOVE_COMMAND:
                removeFlair(sub, msg.body)
        msg.mark_as_read()

if __name__ == "__main__":
    dir = os.path.dirname(__file__)
    LOG_FILENAME = os.path.join(dir, 'flair-bot.log')
    logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO
    main()