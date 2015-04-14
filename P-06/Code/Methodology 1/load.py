import simplejson

def parse(filename):
  f = open(filename, 'r')
  entry = {}
  for l in f:
    l = l.strip()
    colonPos = l.find(':')
    if colonPos == -1:
      yield entry
      entry = {}
      continue
    eName = l[:colonPos]
    rest = l[colonPos+2:]
    entry[eName] = rest
  yield entry

for e in parse("Cell_Phones_&_Accessories.txt"):
    f = open('data.json','a')
    f.write(simplejson.dumps(e)+'\n')
