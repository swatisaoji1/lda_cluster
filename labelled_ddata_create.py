import pandas as pd
from pymongo import MongoClient
import csv

import IPython.core.display as di
# This line will hide code by default when the notebook is exported as HTML
di.display_html('<script>jQuery(function() {if (jQuery("body.notebook_app").length == 0) { jQuery(".input_area").toggle(); jQuery(".prompt").toggle();}});</script>', raw=True)


conn = MongoClient("localhost", 27017)
db = conn['tweet_db']

print (db)
collection_name = "AmericanCrime_tweets"
collection = db[collection_name]

cursor = collection.find().limit(20000)
df = pd.DataFrame(list(cursor))
print(df[:20])

list_of_hashtags = ['#politics' ,'#art', '#music',
                    '#tech', '#money', '#business', '#food','#sport', '#tv']
print("Hashtag used")
print(list_of_hashtags)

group_user = df.groupby('user_id')
count = 0
out = 'data_comparison.csv'
writer = csv.writer(open(out, 'w', newline=''))
for each_group, content in group_user:
    count_per_user = 0
    for each_entry, data in content.iterrows():
        for each_ht in list_of_hashtags:
            if each_ht in data[3]:
                row = []
                row.append(each_group)  # user_id
                row.append(data[1])
                row.append(data[3])
                row.append(each_ht)
                print(row)
                writer.writerow(row)
                count_per_user += 1
            break
    count += 1
    if count == 20:
        break