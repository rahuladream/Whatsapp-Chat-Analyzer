# Whatsapp-Chat-Analyzer
Analyzing Whatsapp Chat (Personal &amp; Group)

* Current making is to analyzing the WhatsApp chat more efficiently

### Next Iteration

* Next step would be learn a model to predict the next chat 
* Automate my text in real time


### Requirements
----------------------
- Python 3.6+
```python
pip install -r requirements.txt
```
### Usage
----------------------
```
$ git clone https://github.com/PetengDedet/WhatsApp-Analyzer.git

$ cd WhatsApp-Analyzer
$ python whatsapp_analyzer.py chat_example.txt --stopword indonesian 
```

```shell
usage: python whatsapp_analyzer.py FILE [-h] [-d] [-s] [-c]

Read and analyze whatsapp chat

positional arguments:
  FILE                  Chat file path

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Debug mode. Shows details for every parsed line.
```
