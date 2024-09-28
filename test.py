import csv

with open("lamps.csv", mode = "r") as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            print(line)