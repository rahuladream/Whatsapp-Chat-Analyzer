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
        
    def replace_bad_characters(self, line=""):
        # https://stackoverflow.com/questions/20078816/replace-non-ascii-characters-with-a-single-space
        return line.strip().replace(u"\u202a", "").replace(u"\u200e", "").replace(u"\u202c", "").replace(u"\xa0", " ")
    

    def is_startingline(self, line=""):
        """
        Starting line mean a line that started with date time
        Because there are multiple chat.

        The Rule is:
        <datetime><seprator><Contact>
        """
        pattern = r"""
            (\[?)       #Zero or one open square bracket '['
            (((\d{1,2})   #1 to 2 digit date
            (/|-)       #'/' or '-' separator
            (\d{1,2})   #1 to 2 digit month
            (/|-)       #'/' or '-' separator
            (\d{2,4}))   #2 to 4 digit of year
            (,?\s)      #Zero or one comma ',' and ingle space
            ((\d{1,2})  #1 to 2 digit of hour
            (:|\.)      #Colon ':' or dot '.' separator
            (\d{2})     #2 digit of minute
            (\.|:)?     #Zero or one of dot '.' or colon ':'
            (\d{2})?    #Zero or one of 2 digits of second
            (\s[AP]M)?))  #Zero or one of ('space', 'A' or 'P', and 'M'
            (\]?\s-?\s?\s?)#Zero or one close square bracket ']', Zero or one (space and '-'), zero or one space
            (.+)        #One or more character of chat member phone number or contact name
        """
        match = re.match(re.compile(pattern, re.VERBOSE), line)
        if match:
            return match
        
        return None

    def is_chat(self, body=""):
        """
        Is Chat means the body of line is not an event
        May contains attachment
        
        The rule is:
        <contact><separator><message body>
        """
        pattern = r"""
                ([^:]+)#Chat member
                (:)   #Colon separator
                (.+)  #One or more charachter of message content
        """
        match = re.match(re.compile(pattern, re.VERBOSE), body)
        if match:
            return match
        
        return None
    
    def is_deleted(self, body):
        """
        Is message deleted from chat
        """
        pattern = [
            r".*This message was deleted$"
        ]

        for p in p:
            match = re.match(p, body)
            if match:
                return body
        return None
    
    def contains_attachment(self, body=""):
        """
        Classify attachement
        """
        pattern = [
            r".*<Media omitted>$",
            r".*image omitted$",
            r".* video omitted$",
             r".*document omitted$",
            r".*Contact card omitted$",
            r".*audio omitted$",
            r".*GIF omitted$",
            r".*sticker omitted$"
        ]

        for p in pattern:
            if re.match(p, body):
                return body
        return None
    
    def extract_timestamp(self, time_string=""):
        """
        Extract Timestamp
        """
        timestamp = parser.parse(time_string)
        return timestamp


    def extract_url(self, body=""):
        """
        Check if chat contais a url
        """
        # pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
        pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,6}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        
        return re.findall(pattern, body)
    
    def get_domain(self, url=""):
        domain = url[0].replace("http://", '')
        domain = domain.replace("https://", '')
        domain = domain.split("/")
        return domain[0]

    def get_words(self, string=""):
        
        #remove dirty content
        regex = re.sub(r"[^a-z\s]+", "", string.lower())
        regex = re.sub(r'[^\x00-\x7f]',r'', regex)
        words = re.sub(r"[^\w]", " ",  string).split()
        
        return words

        