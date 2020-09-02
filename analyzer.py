#!/usr/bin/env python

# Python core import
import argparse
import io
import collections as Counter
import sys

# Package Import
import emoji

# Local Import
from chat_decode import ChatDecode



"""
CLI Parser
"""
parser = argparse.ArgumentParser(
    description='Read and Analyze WhatsApp Chat',
    usage='python3 analyzer.py FILE [-h] [-d] [-s] [-c]'
)

stop_words = ["english"]

parser.add_argument('file',
 metavar='FILE',
 help='Chat File Path'
)

parser.add_argument(
    '-d',
    '--debug',
    required=False,
    help='Debug mode',
    action='store_true'
)

args = parser.parse_args()

"""
READ CHAT FILE
"""
try:
    with io.open(args.file, "r", encoding="utf-8") as file:
        lines = file.readlines()

except IOError as e:
    print("File \{} not found. Please recheck file location and permissions".format(args.file))
    sys.exit()

"""
PARSING AND COUNTING
"""

chat_counter = {
    'chat_count': 0,
    'deleted_chat_count': 0,
    'event_count': 0,
    'senders': [],
    'timestamps': [],
    'words': [],
    'domains': [],
    'emojis': [],
    'fav_emojis': [],
    'fav_words': []
}

previous_line = None

for line in lines:
    chatline = ChatDecode(line=line, previous_line=previous_line)
    previous_line = chatline

    # Counter & Setter

    if chatline.line_type == 'Chat':
        chat_counter['chat_count'] += 1
    
    if chatline.line_type == 'Event':
        chat_counter['event_count'] += 1
    
    if chatline.is_deleted:
        chat_counter['deleted_chat_count'] += 1
    

    if chatline.sender is not None:
        chat_counter['senders'].append(chatline.sender)
        for i in chatline.emojis:
            chat_counter['fav_emojis'].append((chatline.sender, i))
        
        for i in chatline.words:
            chat_counter['fav_words'].append((chatline.sender, i))

    if chatline.timestamp:
        chat_counter['timestamps'].append(chatline.timestamp)

    if len(chatline.words) > 0:
        chat_counter['words'].extend(chatline.words)

    if len(chatline.emojis) > 0:
        chat_counter['emojis'].extend(chatline.emojis)

    if len(chatline.domains) > 0:
        chat_counter['domains'].extend(chatline.domains)


"""
REDUCE AND ORDER DATA
"""

def reduce_and_sort(data):
    return sorted(
        dict(
            zip(
                Counter(data).keys(),
                Counter(data).values()
            )
        ).items(), key=lambda x: x[1],
        reverse=True
    )

# import pdb; pdb.set_trace()
print(reduce_and_sort(chat_counter))