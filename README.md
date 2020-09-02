# Whatsapp-Chat-Analyzer
Analyzing Whatsapp Chat (Personal &amp; Group)

* Current making is to analyzing the WhatsApp chat more efficiently

### Next Iteration

* Next step would be learn a model to predict the next chat 
* Automate my text in real time

https://img.shields.io/github/issues/rahuladream/Whatsapp-Chat-Analyzer

##### Supported Analysis
----------------------
- Chat Count
- Chat Avaerage
- Member/Sender Rank
- Website/URL/Link Domain Rank
- Word Count and Rank
- Most Used Word by Sender
- Emoji Usage Rank
- Most Used Emoji by Sender
- Timestamp Heatmap
- Attachment Classification (In Android, there is no difference pattern for attachment. But in iOS we can actually classify between Image, Video, Audio, GIF, Sticker, Document, and Contact Card)

### Requirements
----------------------
- Python 3.6+
```python
pip install -r requirements.txt
```
### Usage
----------------------
```
$ git clone https://github.com/rahuladream/Whatsapp-Chat-Analyzer.git

$ cd Whatsapp-Chat-Analyzer
$ python analyzer.py chat_example.txt 
```

### Package Install
```shell
pip install wanalyzer
```


```shell
usage: wanalyzer FILE [-h] [-d]

wanalyzer <file_path.txt>

Read and analyze whatsapp chat

positional arguments:
  FILE                  Chat file path

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Debug mode. Shows details for every parsed line.
```

### Preview

- Sender & Mentioned Domain
![Sender & Mentioned Domain](https://i.imgur.com/T1HpKpF.png)

- Used emoji and Favourite Emoji
![Used and Favourite Emoji](https://i.imgur.com/xa9K3Hn.png)

- Most used word and favorite word
![Most used word and favorite word](https://i.imgur.com/ckQa0V6.png)
- Chat activity heatmap
![Heatmap](https://i.imgur.com/kJ9IKWs.png)
