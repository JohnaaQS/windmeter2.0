import csv 

with open('jeweet.csv', mode='w') as csvfile:
    veldnamen = ['first_name', 'last_name']
    schrijver = csv.DictWriter(csvfile, )