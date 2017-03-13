test_input = []
test_output = []
test_actual = []

with open("tests.in") as f:
    test_input = f.readlines();

with open("tests.out") as f:
    test_output = f.readlines();

num_tests = min(len(test_input), len(test_output));

for i in range(0, len(test_input)):
    test_input[i] = test_input[i].strip()

for i in range(0, len(test_output)):
    test_output[i] = test_output[i].strip()

for i in range(0, num_tests):
    print "Test: %s" % test_input[i]
    print "Expected: %s" % test_output[i]
    print "Actual:"
    print "\n"
