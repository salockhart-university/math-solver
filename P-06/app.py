 #!/usr/bin/env python
"""
CSCI 4152 Project
"""

import nltk

UTTERANCES = []

OPERATIONS = {
    "add": [
        "add",
        "plus",
        "sum"
    ],
    "subtract": [
        "subtract",
        "minus",
        "difference"
    ],
    "times": [
        "times",
        "multiply",
        "product",
        "by"
    ],
    "divide": [
        "divide",
        "over"
    ],
    "negative": [
        "negative",
        "minus"
    ]
}

with open("tests.in") as f:
    UTTERANCES = f.readlines()

for utterance in UTTERANCES:
    tokens = nltk.word_tokenize(utterance)
    print tokens
    tagged = nltk.pos_tag(tokens)
    print tagged
    print
