__author__ = 'eladg'
import csv
import os
import datetime

fileOut = open('allTaxiData.csv', 'w')  # This will be the output file
writer = csv.writer(fileOut, delimiter=',')  # use this to write to csv output file

filePath = './NYC Taxi Data/NYC Yellow Taxi Data/2014/Trips/'  # where the data is stored
fileList = os.listdir(filePath)  # get file list
fileList = [fileList[i] for i in [9, 10, 11, 1, 2, 3]]  # Only use July-Dec files
chosenEntries = range(7, 14)  # here I pick which columns I want to use in the output csv
fileInd = 0  # file index counter, only used to indicate whether it's the first file or not (don't want to keep headers, except for the first file)
for name in fileList:  # go over all file in list
    fileInd += 1
    fileIn = open(filePath + '/' + name, 'r')
    reader = csv.reader(fileIn, delimiter=',')

    lineInd = 0
    for line in reader:  # go over all lines in a file
        lineInd += 1
        vals = [line[i] for i in chosenEntries]  # get only the desired columns
        if lineInd == 1:
            if fileInd > 1:  # don't include header except once in the beginning
                continue
            vals = [x.strip() for x in vals]
            header = ['pickup_date', 'pickup_day_of_year', 'pickup_day_of_Month', 'pickup_day_of_week', 'pickup_month', 'pickup_hour'] +\
                vals  # this will be the header line
            writer.writerow(header)
            continue

        # make pickup and dropoff dates into datetime objects
        pickupDate = datetime.datetime.strptime(line[5], '%Y-%m-%d %H:%M:%S')
        dropoffDate = datetime.datetime.strptime(line[6], '%Y-%m-%d %H:%M:%S')
        # extract date information we care about
        dayOfYear = pickupDate.timetuple().tm_yday
        dayOfWeek = pickupDate.weekday()
        dayOfMonth = pickupDate.day
        month = pickupDate.month
        hour = pickupDate.hour

        outLine = [pickupDate.strftime('%Y-%m-%d %H:%M:%S'), dayOfYear, dayOfMonth, dayOfWeek, month, hour] + vals  # generate the output line

        writer.writerow(outLine)  # write line to file
        # nOut = (len(line) - 3)/entriesPerLine
        # for outInd in xrange(0,nOut):
        #     outLine = prefix + line[outInd*entriesPerLine + 3 : (outInd+1)*entriesPerLine + 3]
        #     writer.writerow(outLine)

    fileIn.close()

fileOut.close()
