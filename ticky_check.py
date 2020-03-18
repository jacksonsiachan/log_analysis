#!/usr/bin/env python3

import re
import csv
import operator
import sys


source_file = sys.argv[1]

error = {}
per_user = {}


with open(source_file, "r") as f:
    for line in f.readlines():
        result = re.search(r"ticky: (INFO|ERROR) ([\w' ]*).*\(([\w.]*)\)", line) 
        if result != None:
           if result[1] == 'INFO':
              if result[3] not in per_user:
                 per_user[result[3]] = [1, 0]
              else:
                 per_user[result[3]][0]+=1  
           if result[1] == 'ERROR':  
              if result[3] not in per_user:
                 per_user[result[3]] = [0, 1]
              else:
                 per_user[result[3]][1]+=1     
              if result[2] not in error:   
                 error[result[2]] = 1
              else:
                 error[result[2]] += 1 
        

sort_error = sorted(error.items(), key = operator.itemgetter(1), reverse=True)
sort_user = sorted(per_user.items(), key = operator.itemgetter(0))

sort_error.insert(0, ("Error", "Count"))

with open('error_message.csv', 'w') as error:
     writer = csv.writer(error)
     writer.writerows(sort_error)

header = ["Username", "Info", "Error"]
with open('user_statistics.csv', 'w') as user:
     writer = csv.writer(user)
     writer.writerow(header)
     for row in sort_user:
         user, stats = row 
         line = (user, stats[0], stats[1])
         writer.writerow(line)
