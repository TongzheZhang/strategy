# -*- coding: utf-8 -*-
"""
Created on Thu Aug 03 13:37:25 2017
calculate from one excel
@author: Richard10ZTZ
"""
import csv


def getInfoFromCob3(test_csv, tempdate):
    #print "entry caloneexcel"
    row = []
    for temprow in test_csv:
        row.append(temprow)
        
    """find out the blank row and we can get the first line"""
    flagblank = 0
    beginrow = []   
    endrow = len(row)
    while flagblank != 1:
        for i in range(0, 10):
            if row[i] == []:
                #print "blank row is:",i
                if flagblank == 0: beginrow.append(i+3)
                flagblank = 1
    #print "the first row is:", beginrow[0]," ",flagblank
    """record the # of sheets"""
    sheetsnum = 1
    for i in range(beginrow[0]+1, endrow):
        if row[i][2] == "1":
            beginrow.append(i)
            sheetsnum = sheetsnum + 1
    #print "# of sheets:",sheetsnum
    beginrow.append(endrow)

    """which one is better"""
    bestSheet = 0
    tempV = 0
    SheetsV = []
    for i in range(sheetsnum-1): 
        tempT = 0
        for j in range(beginrow[i], beginrow[i+1]):
           tempT = tempT + int(row[j][4])
        SheetsV.append(tempT)
    tempT = 0
    for i in range(beginrow[sheetsnum-1], endrow):
        tempT = tempT + int(row[i][4])
    #print tempT
    SheetsV.append(tempT)
    for i in range(len(SheetsV)):
        if SheetsV[i] > tempV:
            tempV = SheetsV[i]
            bestSheet = i
    
    #print "di", i+1, "sheet is better"
    
    """record data of B, S"""
    Bincre = 0
    Sincre = 0
    Bnum = 0
    Snum = 0
    Vnum = 0
    signal = 0
    
    for t in range(beginrow[bestSheet],beginrow[bestSheet+1]):
        if int(row[t][4]) != 0:
            Vnum = Vnum+1
        if int(row[t][7]) != 0:
            Bnum = Bnum+1
        if int(row[t][10]) != 0:
            Snum = Snum+1
        Bincre = Bincre + int(row[t][8])
        Sincre = Sincre + int(row[t][11])
    
    if Bincre - Sincre > 0:
        signal = 1
    elif Bincre - Sincre < 0:
        signal = 2
    if Bnum<20 or Snum< 20 or Vnum<20:
        signal = 3
  
    #if endrow-beginrow < 20: signal = 4
    #print "signal:", signal
    return [Bincre, Sincre, signal, Vnum, Bnum, Snum, SheetsV,  beginrow]
    
"""main function"""
if __name__ == '__main__':

    """read the csv file"""
    
    recorddate = []
    recorddata = []
    for year in range(2010, 2018):
        tempyear = str(year)
        for month in range(1, 13):
            if month < 10: tempmonth = "0" + str(month)
            else: tempmonth = str(month)
            for day in range(1, 32):
                if day < 10: tempday = "0" + str(day)
                else: tempday = str(day)
                tempdate = tempyear+tempmonth+tempday
                tempname = "../TFdata/"+tempdate+".csv"
                try:
                    test_csv = csv.reader(open(tempname))
                    result = getInfoFromCob3(test_csv, tempdate)
                    signal = result[2]
                    recorddate.append(tempdate)
                    recorddata.append(signal)
                    #print result
                except IOError:
                    print tempdate," not have this day"
                    pass
    
    """   testing             
    test_csv = csv.reader(open("../TFdata/20170609.csv"))#20170712
    result = getInfoFromCob3(test_csv, "20170609")       #20131212    20170807
    """ 
    
    """write data into .txt"""
    w = open("finaldata.txt","w")
    for i in range(0, len(recorddate)):
        w.write(recorddate[i][2:]+" "+str(recorddata[i])+"\n")
    w.close()
    