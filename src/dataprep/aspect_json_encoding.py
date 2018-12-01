import json
import sys


with open("data/processed/reviews_Nov24_fullrun.json", "r") as f:
    newText = f.read().replace('][',',')

print("reading done")

with open("data/processed/reviews_Nov24_fullrun_encoding.json", "w") as f1:
    json.dump(newText,f1)

print("writing done")
