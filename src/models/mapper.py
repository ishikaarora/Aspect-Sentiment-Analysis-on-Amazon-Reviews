import json
import sys

from time import time
import ijson


def map(file_input, file_output):
    time1 =  time()
    with open(file_input, "r") as f:
        newText = f.read().replace('][',',')


    js = json.loads(newText)
    time2 = time()

    new_js = []
    mapper = {}
    counter = 0
    reviews = 0
    for item in js:
        reviews = reviews + 1
        #print(new_js)
        # print(mapper)
        # print(counter)
        prod_id = item.get('product_id')
        dic = {'review_id' : item.get('review_id'), 'aspect_pairs' :  item.get('aspect_pairs')}

        if prod_id in mapper:
            #print(prod_id)
            index = mapper.get(prod_id)
            new_js[index][prod_id].append(dic)

        else:
            prod_dic = {prod_id : []}
            prod_dic[prod_id].append(dic)
            #print(prod_dic)
            new_js.append(prod_dic)
            mapper.update({prod_id : counter})
            counter = counter + 1
    time3 = time()


    with open(file_output, "w") as f1:
        json.dump(new_js,f1)
    time4 = time()

    print(counter)
    print(reviews)

    print("Time for loads json: {0:.2}s".format(time2-time1))
    print("Time for loads mapping: {0:.2}s".format(time3-time2))
    print("Time for loads mapping: {0:.2}s".format(time4-time3))




# with open("data/interim/reviews_Nov24_productid.json", "r") as f:
#     newText = f.read().replace('][',',')
#
#
# with open("data/interim/reviews_Nov24_productid_modified.json", "w") as f1:
#     f1.write(newText)
