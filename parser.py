import json

fname = "example_output.json"

with open(fname,"r") as fp:
        raw = fp.read()

data = json.loads(raw)

print data