 #!/usr/bin/env python
"""
CSCI 4152 Project - Tests
"""

INPUT = []
OUTPUT = []
ACTUAL = []

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
    print "Test: %s" % INPUT[i]
    print "Expected: %s" % OUTPUT[i]
    print "Actual:"
    print "\n"
