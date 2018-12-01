import json
import sys
import simplejson

# f = open("data/raw/reviews_Nov24.json", "r")
#
# f = open("data/raw/reviews_Nov24.json", "r")
#
#
# for line in f:
#     r = simplejson.loads(line).get('product_id')
#     print(r)


with open("data/raw/reviews_Nov24.json", "r") as f:
    newText = f.read().replace('][',',')


with open("data/raw/reviews_Nov24_modified.json", "w") as f1:
    f1.write(newText)
