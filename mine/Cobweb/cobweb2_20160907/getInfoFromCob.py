# -*- coding: utf-8 -*-
"""
Created on Thu Aug 03 13:37:25 2017
calculate from one excel
@author: Richard10ZTZ
"""
import csv


def getInfoFromCob(test_csv, tempdate):
    #print "entry caloneexcel"
    row = []
    for temprow in test_csv:
        row.append(temprow)
    """find out the blank row"""
    flagblank = 0
    beginrow = 0    
    while flagblank == 0:
        for i in range(0, 10):
            if row[i] == []:
                beginrow = i+3
                flagblank = 1
    """record data of B, S"""
    Bincre = 0
    Sincre = 0

    for t in range(0,20):
        Bincre = Bincre + int(row[beginrow+t][8])
        Sincre = Sincre + int(row[beginrow+t][11])
    return [Bincre, Sincre]

"""main function"""
if __name__ == '__main__':

    """read the csv file"""
    
    recorddate = []
    recorddata = []
    lastB = 0.0
    lastS = 0.0
    for year in range(2010, 2018):
        tempyear = str(year)
        for month in range(1, 13):
            if month < 10: tempmonth = "0" + str(month)
            else: tempmonth = str(month)
            for day in range(1, 32):
                if day < 10: tempday = "0" + str(day)
                else: tempday = str(day)
                tempdate = tempyear+tempmonth+tempday
                tempname = "../IFdata/"+tempdate+".csv"
                try:
                    test_csv = csv.reader(open(tempname))
                    result = getInfoFromCob(test_csv, tempdate)
                    lastB = result[0]
                    lastS = result[1]
                    recorddate.append(tempdate)
                    recorddata.append(result)
                    #print result
                except IOError:
                    print tempdate," not have this day"
                    pass
    
    """   testing              
    test_csv = csv.reader(open("data/20120418.csv"))
    result = caloneexcel(test_csv, "20170417", 0.0, 0.0, 0.0)               
    """
    
    """write data into .txt"""
    w = open("finaldata.txt","w")
    for i in range(0, len(recorddate)):
        key = 0
        if recorddata[i][0]>0 and recorddata[i][1]<0:
            key = 1
        elif recorddata[i][0]<0 and recorddata[i][1]>0:
            key = 2
        else: key = 3
        w.write(recorddate[i][2:]+" "+str(key)+"\n")
    w.close()
    