#!/usr/bin/env python
"""
CSCI 4152 Project
"""

import nltk
from nltk.parse import pchart
from nltk.stem import WordNetLemmatizer

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

GRAMMAR = nltk.PCFG.fromstring("""
    S -> S OP S                         [0.25]
    S -> OP S 'and' S                   [0.25]
    S -> 'subtract' S                   [0.25]
    S -> THOU                           [0.25]

    OP -> 'add'                         [0.25]
    OP -> 'subtract'                    [0.25]
    OP -> 'multiply'                    [0.25]
    OP -> 'divide'                      [0.25]

    THOU -> HUN                         [0.25]
    THOU -> CD 'thousand' HUN           [0.25]
    THOU -> CD 'thousand' 'and' HUN     [0.25]
    THOU -> CD 'thousand'               [0.25]

    HUN -> TEEN                         [0.25]
    HUN -> CD 'hundred' TEEN            [0.25]
    HUN -> CD 'hundred' 'and' TEEN      [0.25]
    HUN -> CD 'hundred'                 [0.25]

    TEEN -> CD                          [0.076923077]
    TEEN -> TEN CD                      [0.076923077]
    TEEN -> TEN                         [0.076923077]

    TEEN -> 'ten'                       [0.076923077]
    TEEN -> 'eleven'                    [0.076923077]
    TEEN -> 'twelve'                    [0.076923077]
    TEEN -> 'thirteen'                  [0.076923077]
    TEEN -> 'fourteen'                  [0.076923077]
    TEEN -> 'fifteen'                   [0.076923077]
    TEEN -> 'sixteen'                   [0.076923077]
    TEEN -> 'seventeen'                 [0.076923077]
    TEEN -> 'eighteen'                  [0.076923077]
    TEEN -> 'nineteen'                  [0.076923077]

    TEN -> 'twenty'                     [0.125]
    TEN -> 'thirty'                     [0.125]
    TEN -> 'forty'                      [0.125]
    TEN -> 'fifty'                      [0.125]
    TEN -> 'sixty'                      [0.125]
    TEN -> 'seventy'                    [0.125]
    TEN -> 'eighty'                     [0.125]
    TEN -> 'ninety'                     [0.125]

    CD -> 'zero'                        [0.1]
    CD -> 'one'                         [0.1]
    CD -> 'two'                         [0.1]
    CD -> 'three'                       [0.1]
    CD -> 'four'                        [0.1]
    CD -> 'five'                        [0.1]
    CD -> 'six'                         [0.1]
    CD -> 'seven'                       [0.1]
    CD -> 'eight'                       [0.1]
    CD -> 'nine'                        [0.1]
""")

# PARSER = nltk.ChartParser(GRAMMAR)
# PARSER = nltk.ViterbiParser(GRAMMAR)
PARSER = pchart.InsideChartParser(GRAMMAR)

LEMMATIZER = WordNetLemmatizer()

def add(one, two):
    """
    returns one + two
    """
    return one + two

def subtract(one, two):
    """
    returns one - two
    """
    return one - two

def divide(one, two):
    """
    returns one / two as floating point division
    """
    return one / (two * 1.0)

def multiply(one, two):
    """
    returns one * two
    """
    return one * two

def calc(operation, args):
    """
    If we have 1 arg, we add a 0 to the head so that
    'subtract' [1] results in -1
    otherwise, get the function from above and apply it to the args
    """
    if len(args) == 1:
        args = [0, args[0]]

    if operation == "add":
        func = add
    elif operation == "subtract":
        func = subtract
    elif operation == "divide":
        func = divide
    elif operation == "multiply":
        func = multiply

    result = args[0]
    for arg in args[1:]:
        result = func(result, arg)

    return result

def parse_s(tree):
    """
    S -> S OP S | OP S 'and' S | 'subtract' S | THOU
    tree is the result of the parsing in the grammar
    S can just be a value, so if we find the THOU child we return its value
    otherwise, grab the operation and the args and return the result
    this will calculate the value recursively
    """
    args = []
    operation = ""
    for subtree in tree:
        if subtree == "subtract":
            operation = "subtract"
        elif subtree == "and":
            continue
        elif subtree.label() == "S":
            args.append(parse_s(subtree))
        elif subtree.label() == "OP":
            operation = parse_op(subtree)
        elif subtree.label() == "THOU":
            return parse_thousands(subtree)
    return calc(operation, args)

def parse_thousands(tree):
    """
    THOU -> HUN
    THOU -> CD 'thousand' HUN
    THOU -> CD 'thousand' 'and' HUN
    THOU -> CD 'thousand'
    thousands are always composites, so we immediately traverse the tree
    ignore the terminals 'thousand' and 'and'
    when we parse a CD as a child, it represents the number of thousands
    """

    result = 0

    for subtree in tree:
        if subtree == "thousand" or subtree == "and":
            continue
        elif subtree.label() == "HUN":
            result += parse_hundreds(subtree)
        elif subtree.label() == "CD":
            result += (parse_ones(subtree) * 1000)

    return result

def parse_hundreds(tree):
    """
    HUN -> TEEN
    HUN -> CD 'hundred' TEEN
    HUN -> CD 'hundred' 'and' TEEN
    HUN -> CD 'hundred'
    hundreds are always composites, so we immediately traverse the tree
    ignore the terminals 'hundred' and 'and'
    when we parse a CD as a child, it represents the number of hundreds
    """

    result = 0

    for subtree in tree:
        if subtree == "hundred" or subtree == "and":
            continue
        elif subtree.label() == "TEEN":
            result += parse_teens(subtree)
        elif subtree.label() == "CD":
            result += (parse_ones(subtree) * 100)

    return result

def parse_teens(tree):
    """
    TEEN -> CD | TEN CD | TEN
    TEEN -> 'ten' | 'eleven' | ...
    so either the child is a member of TEENS, or it is a
    combination of TEN and CD substrings
    """

    mapping = {
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
        "seventeen": 17,
        "eighteen": 18,
        "nineteen": 19
    }

    if tree[0] in mapping.keys():
        return mapping[tree[0]]

    result = 0

    for subtree in tree:
        if subtree.label() == "CD":
            result += parse_ones(subtree)
        elif subtree.label() == "TEN":
            result += parse_tens(subtree)

    return result

def parse_tens(tree):
    """
    TEN -> 'twenty' | 'thirty' | ...
    so just return the child, which is our value
    """

    mapping = {
        "twenty": 20,
        "thirty": 30,
        "forty": 40,
        "fifty": 50,
        "sixty": 60,
        "seventy": 70,
        "eighty": 80,
        "ninety": 90
    }

    return mapping[tree[0]]

def parse_ones(tree):
    """
    CD -> 'zero' | 'one' | 'two' | ...
    so just return the child, which is our value
    """

    mapping = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9
    }

    return mapping[tree[0]]

def parse_op(tree):
    """
    OP -> 'add' | 'subtract' | 'multiply' | 'divide'
    so just return the child, which is our operation
    """
    return tree[0]

def get_value(utterance):
    """
    For a given utternace, return the possible values from the parsing
    """
    tokens = nltk.word_tokenize(utterance)
    for i in range(0, len(tokens)):
        tokens[i] = LEMMATIZER.lemmatize(tokens[i], pos="v")

    utterance = " ".join(tokens)
    for operation in OPERATION_ORDER:
        for variant in OPERATIONS[operation]:
            utterance = utterance.replace(variant, operation)
    tokens = nltk.word_tokenize(utterance)

    possibles = []

    for tree in PARSER.parse(tokens):
        print tree
        possibles.append(parse_s(tree))

    return possibles
