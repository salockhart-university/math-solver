 #!/usr/bin/env python
"""
CSCI 4152 Project
"""

import nltk
from nltk.stem import WordNetLemmatizer

UTTERANCES = []

OPERATION_ORDER = [
    "add",
    "subtract",
    "divide",
    "multiply"
]

OPERATIONS = {
    "add": [
        "add",
        "plus",
        "sum"
    ],
    "subtract": [
        "subtract",
        "minus",
        "difference of",
        "negative"
    ],
    "divide": [
        "divide by",
        "divide",
        "over"
    ],
    "multiply": [
        "multiply by",
        "time",
        "multiply",
        "product of",
        "by"
    ]
}

with open("tests.in") as f:
    UTTERANCES = f.readlines()

GRAMMAR = nltk.CFG.fromstring("""
    S -> S OP S | OP S 'and' S | 'subtract' THOU | THOU
    OP -> 'add' | 'subtract' | 'multiply' | 'divide'
    THOU -> HUN | CD 'thousand' HUN | CD 'thousand' 'and' HUN | CD 'thousand'
    HUN -> TEEN | CD 'hundred' TEEN | CD 'hundred' 'and' TEEN | CD 'hundred'
    TEEN -> CD | TEN CD | TEN
    TEEN -> 'ten' | 'eleven' | 'twelve' | 'thirteen' | 'fourteen' | 'fifteen' | 'sixteen' | 'seventeen' | 'eighteen' | 'nineteen'
    TEN -> 'twenty' | 'thirty' | 'forty' | 'fifty' | 'sixty' | 'seventy' | 'eighty' | 'ninety'
    CD -> 'zero' | 'one' | 'two' | 'three' | 'four' | 'five' | 'six' | 'seven' | 'eight' | 'nine'
""")

PARSER = nltk.ChartParser(GRAMMAR)

LEMMATIZER = WordNetLemmatizer()

for utterance in UTTERANCES:
    tokens = nltk.word_tokenize(utterance)
    for i in range(0, len(tokens)):
        tokens[i] = LEMMATIZER.lemmatize(tokens[i], pos="v")
    utterance = " ".join(tokens)
    for operation in OPERATION_ORDER:
        for variant in OPERATIONS[operation]:
            utterance = utterance.replace(variant, operation)
    tokens = nltk.word_tokenize(utterance)
    print tokens
    for tree in PARSER.parse(tokens):
        print tree
    print
