import csv

start_urls = []
csv_file = csv.reader(open('urls.csv', 'r'))
for i,rows in enumerate(csv_file):
    if i != 0:
        start_urls.append(rows[1])
print(start_urls)