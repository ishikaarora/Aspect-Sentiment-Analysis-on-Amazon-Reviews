import json
import sys



def run(file_in, file_out):
    with open(file_in, "r") as f:
        newText = f.read().replace('][',',')

    js = json.loads(newText)
    print("reading done")

    with open(file_out, "w") as f1:
        json.dump(js,f1)

    print("writing done")
