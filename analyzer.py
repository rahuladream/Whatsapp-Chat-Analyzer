#!/usr/bin/env python

# Python core import
import argparse
import io
import collections as Counter
import sys

# Package Import
import emoji

# Local Import



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
