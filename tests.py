 #!/usr/bin/env python
"""
CSCI 4152 Project - Tests
"""

import app

COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RED = "\033[91m"
COLOR_END = "\033[0m"

INPUT = []
OUTPUT = []
ACTUAL = []

CORRECT = 0
AMBIGUOUS = 0
INCORRECT = 0

def correct(test, expected, actual, str_rep):
    print COLOR_GREEN
    common(test, expected, actual, str_rep)

def ambiguous(test, expected, actual, str_rep):
    print COLOR_YELLOW
    common(test, expected, actual, str_rep)

def incorrect(test, expected, actual, str_rep):
    print COLOR_RED
    common(test, expected, actual, str_rep)

def common(test, expected, actual, str_rep):
    print "Test:", test
    print "Expected:", expected
    print "Actual:", actual
    print "Representation:", str_rep
    print COLOR_END

with open("tests.in") as f:
    INPUT = f.readlines()

with open("tests.out") as f:
    OUTPUT = f.readlines()

NUM_TESTS = min(len(INPUT), len(OUTPUT))

for i in range(0, len(INPUT)):
    INPUT[i] = INPUT[i].strip()

for i in range(0, len(OUTPUT)):
    OUTPUT[i] = OUTPUT[i].strip()

for i in range(0, NUM_TESTS):
    test = INPUT[i]
    expected = OUTPUT[i]
    actual, str_rep = app.get_value(INPUT[i])
    if len(actual) == 1 and abs(actual[0] - float(expected)) < 0.01:
        CORRECT += 1
        correct(test, expected, actual, str_rep)
    elif float(expected) in actual:
        AMBIGUOUS += 1
        ambiguous(test, expected, actual, str_rep)
    else:
        INCORRECT += 1
        incorrect(test, expected, actual, str_rep)

print COLOR_GREEN, "CORRECT:", CORRECT, COLOR_END
print COLOR_YELLOW, "AMBIGUOUS:", AMBIGUOUS, COLOR_END
print COLOR_RED, "INCORRECT:", INCORRECT, COLOR_END
