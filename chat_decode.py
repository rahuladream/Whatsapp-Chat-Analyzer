# Python code import
import re
from dateutil import parser

# Package Import
import emoji

"""
TODO:
1. Replace Bad Character
2. Is Chat Present or Blank
3. Is Message is Deleted
4. Is Message contains Attachment
5. Extract Timestamp
6. Get Words
7. Get Events if found
8. Extract emoji
9. Finally Parse Body
"""

class ChatDecode:

    def __init__(self, line="", previous_line=None, debug=False):
        self.previous_line   = previous_line
        self.line            = line
        self.line_type       = None # Chat/Event/Attachements if foudn
        self.timestamp       = None # 01/09/20, 23:27
        self.sender          = None # Name of sender maybe
        self.body            = ""
        self.is_startingline = False
        self.isfollowingline = False
        self.isdeleted_chat  = False
        self.words           = []
        self.emoji           = []
        self.domains         = []

        self.parse_line(line)

        if debug:
            print()
            for i in self.__dict__:
                print(i , ':', self.__dict__[i])
            print("----------------")