############################################################################
#This program takes as input Mallet topics file, with file name and 100
#topics per file, in the form of a .csv file,
#for Whitney Arnold's autobiography project within UCLA's DRC
#and converts it to a .csv giving the per-year average weight for each topic.
#
#Author: Benjamin Niedzielski (bniedzie@ucla.edu)
#Last Modified: 5/20/2020
#
#This code may be used or reproduced in part or full so long as this license
#and the original author are left intact.
############################################################################
import re;
import sys;
import csv;

#The input files are specified here
readFile = 'topics_100';
yearsFile = 'AutobiographyList.csv';

################################################
#Parses a csv file to generate a dictionary
#mapping the ID of each volume to the year
#it was written in.
#
#Output: a dictionary mapping volume to year
################################################
def mapVolumesToYears():
    #This dictionary will map volume ID to year for fast lookup later
    volumeToYear = {};

    #Determine the year for each volume
    fp = open(yearsFile, 'r', encoding='utf-8', errors='ignore');
    readCSV = csv.reader(fp, delimiter=',');
    for row in readCSV:
        if len(row) > 12:
            volumeID = row[12];
            year = row[6];
            volumeToYear[volumeID] = year;
    fp.close();

    return volumeToYear;

################################################
#Parses a csv file of topics per page to
#generate a dictionary mapping year to a list
#of topic weights.
#
#Input: a dictionary mapping volume to year
#Output: a dictionary mapping year to a list
#     of topic weights for each page in the year
################################################
def extractTopicTotals(volumeToYear):
    yearTotals = {};

    #Read each line in the input file
    fp = open(readFile, 'r', encoding='cp932', errors='ignore');
    readCSV = csv.reader(fp, delimiter='\t');

    for row in readCSV:
        topicTotals = [0] * 100;

        fileinfo = row[1].split('/')[6].split('.')[0].split('_');
        volName = fileinfo[0];
        year = volumeToYear[volName];

        for ii in range(2, len(row)):
            if row[ii].find('E') != -1:
                row[ii] = 0;
            topicTotals[ii - 2] = float(row[ii]);

        #If this is the first page from this year, set up the dict
        #We use a list so we can store each page's values and average
        #them at the end
        if not year in yearTotals.keys():
            yearTotals[year] = [topicTotals]
        else:
            yearTotals[year].append(topicTotals);

    fp.close();
    return yearTotals;

################################################
#Given a list of lists of the same dimension,
#returns the average of the lists.
#
#Input: a list of lists of the same size
#Output: a list with the average of these lists
#       or an empty list if the input is empty
################################################
def reduce2DListToAverage(list):
    length = len(list);
    if length == 0:
        return [];

    sumList = [];
    for item in list:
        if len(sumList) == 0:
            sumList = item;
        else:
            for ii in range(0, len(item)):
                sumList[ii] = sumList[ii] + item[ii];

    return [x/length for x in sumList];

################################################
#Given a dictionary mapping year to average
#topic weights, writes the results to a csv.
#
#Input: a dictionary of year to topic weight avg
################################################
def writeAverages(yearWeights):
    #Open the file to write
    fw = open((readFile+'_test.csv'), 'w', encoding='cp932', errors='ignore', newline='');
    writeCSV = csv.writer(fw, delimiter=',');

    toWrite = ["Year"];
    for kk in range(1, 101):
        toWrite.append("Topic " + str(kk));
    writeCSV.writerow(toWrite);

    for year in yearWeights.keys():
        toWrite = [year];
        for topicAvg in yearWeights[year]:
            toWrite.append(topicAvg);
        writeCSV.writerow(toWrite);

    fw.close();

volumeToYear = mapVolumesToYears();
yearTotals = extractTopicTotals(volumeToYear);
for year in yearTotals:
    yearTotals[year] = reduce2DListToAverage(yearTotals[year]);
writeAverages(yearTotals);
