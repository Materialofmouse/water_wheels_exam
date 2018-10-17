import csv

#writting data to csv
f = open('test.csv', 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerow(list)

f.close()
