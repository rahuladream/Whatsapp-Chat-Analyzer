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
        self.emojis          = []
        self.domains         = []

        self.parse_line(line)

        if debug:
            print()
            for i in self.__dict__:
                print(i , ':', self.__dict__[i])
            print("----------------")
        
    def replace_bad_character(self, line=""):
        # https://stackoverflow.com/questions/20078816/replace-non-ascii-characters-with-a-single-space
        return line.strip().replace(u"\u202a", "").replace(u"\u200e", "").replace(u"\u202c", "").replace(u"\xa0", " ")
    

    def is_starting_line(self, line=""):
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

        for p in pattern:
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
    
    def extract_emojis(self, string=""):
        emj = []
        for c in string:
            if c in emoji.UNICODE_EMOJI:
                emj.append(c)
        return emj 

    
    def is_event(self, body=""):
        """Detect wether the body of chat is event log.
        If the body if an event, it won't be count and the body of the message will not analized
        Event log means note of event.
        Below are known event log patterns in difference language
        - Group created
        - User joining group
        - User left group
        - Adding group member
        - Removing group member
        - Security code changed
        - Phone number changed
        -
        Feel free to add similar pattern for other known pattern or language
        Keyword arguments:
        body -- body of exported chat
        The Rule is:
        Match the known event message
        """
        pattern_event = [
            # Welcoming message
            r"Messages to this group are now secured with end-to-end encryption\.$",  # EN
            # User created group
            r".+\screated this group$",  # EN
            # User left group
            r".+\sleft$",  # EN
            r".+\skeluar$",  # ID
            # User join group via inviation link
            r".+\sjoined using this group's invite link$",  # EN
            r".+\stelah bergabung menggunakan tautan undangan grup ini$",  # ID
            # Admin adds member
            r".+\sadded\s.+",  # EN
            r".+\smenambahkan\s.+",  # ID
            # Admin removes member
            r".+\sremoved\s.+",  # EN
            # Member's security code changed
            r".+'s security code changed\.$",  # EN
            # Member changes phone number
            r".*changed their phone number to a new number. Tap to message or add the new number\.$"  # EN
            r".*telah mengganti nomor teleponnya ke nomor baru. Ketuk untuk mengirim pesan atau menambahkan nomor baru\.$",  # ID
        ]

        for p in pattern_event:
            match = re.match(p, body)
            if match:
                return match
        return None
    

    def parse_line(self, line=""):
        line = self.replace_bad_character(line)
        # Check wether the line is starting line or following line
        starting_line = self.is_starting_line(line)

        if starting_line:
            # Set startingline
            self.is_startingline = True

            # Extract timestamp
            dt = self.extract_timestamp(starting_line.group(2).replace(".", ":"))
            # Set timestamp
            if dt:
                self.timestamp = dt

            # Body of the chat separated from timestamp
            body = starting_line.group(18)
            self.parse_body(body)

        else:
            # The line is following line
            # Set following
            self.is_followingline = True

            # Check if previous line has sender
            if self.previous_line and self.previous_line.sender:
                # Set current line sender, timestamp same to previous line
                self.sender = self.previous_line.sender
                self.timestamp = self.previous_line.timestamp
                self.line_type = "Chat"

            body = line
            self.body = line
            self.parse_body(body, following=True)
    

    def parse_body(self, body="", following=False):
        # Check wether the starting line is a chat or an event
        chat = self.is_chat(body)

        if chat or following:
            # Set line type, sender and body
            self.line_type = "Chat"
            message_body = body
            if not following:
                self.sender = chat.group(1)
                message_body = chat.group(3)

            self.body = message_body

            has_attachment = self.contains_attachment(message_body)
            
            if has_attachment:
                # Set chat type to attachment
                self.line_type = "Attachment"
                
            else:
                if self.is_deleted(message_body):
                    # Set deleted
                    self.is_deleted_chat = True
                else:
                    words = message_body

                    #URL & Domain
                    urls = self.extract_url(message_body)
                    if urls:
                        for i in urls:
                            # Exclude url from words
                            words = words.replace(i[0], "")

                            # Set domains
                            self.domains.append(self.get_domain(i))
                    
                    # Set Words
                    self.words = self.get_words(words)

                    #Emoji
                    emjs = self.extract_emojis(message_body)
                    if emjs:
                        self.emojis = emjs

        elif self.is_event(body):
            # Set line_type
            self.line_type = "Event"