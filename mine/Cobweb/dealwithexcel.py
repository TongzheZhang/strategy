# -*- coding: utf-8 -*-
"""
Created on Thu Aug 03 13:37:25 2017
calculate from one excel
@author: Richard10ZTZ
"""
import csv


def caloneexcel(test_csv, tempdate, lastI, lastU, lastM):
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
    """find out the major company"""
    tradingC = []
    longC = []
    shortC = []
    for i in range(0,20):
        tradingC.append(row[beginrow+i][3])
        longC.append(row[beginrow+i][6])
        shortC.append(row[beginrow+i][9])
    set1 = set(tradingC)
    set2 = set(longC)
    set3 = set(shortC)
    settotal = set1 & set2 & set3 
    settotal = list(settotal)
    """record data of B, S, V"""
    V = []
    B = []
    S = []

    for majorname in settotal:
        for t in range(0,20):
            if row[beginrow+t][3] == majorname:
                V.append(int(row[beginrow+t][4]))
            if row[beginrow+t][6] == majorname:
                B.append(int(row[beginrow+t][7]))
            if row[beginrow+t][9] == majorname:
                S.append(int(row[beginrow+t][10]))
    Vrest = 0
    Brest = 0
    Srest = 0
    for i in range(0,20):
        if tradingC[i] not in settotal:
            Vrest = Vrest + int(row[beginrow+i][4])
        if longC[i] not in settotal:
            Brest = Brest + int(row[beginrow+i][7])
        if shortC[i] not in settotal:
            Srest = Srest + int(row[beginrow+i][10])
    V.append(Vrest)
    B.append(Brest)
    S.append(Srest)
       
    #print row[beginrow][4] 
    #print row[beginrow+19][4]
    sumV = float(sum(V))  
    sumB = sum(B) 
    sumS = sum(S)
    sumTotal = (sumB+sumS)/sumV
    Itrader = []
    Utrader = []
    for i in range(len(V)):
        if (B[i]+S[i])/float(V[i]) >= sumTotal:
            Itrader.append([V[i], B[i], S[i], (B[i]+S[i])/float(V[i])])
        else:
            Utrader.append([V[i], B[i], S[i], (B[i]+S[i])/float(V[i])])
    IB = 0
    IS = 0
    UB = 0
    US = 0
    for i in range(len(Itrader)):
        IB = IB + Itrader[i][1]
        IS = IS + Itrader[i][2]
    for i in range(len(Utrader)):
        UB = UB + Utrader[i][1]
        US = US + Utrader[i][2]
    try:
        ITS = (IB-IS)/float(IB+IS)
        UTS = (UB-US)/float(UB+US)
        print tempdate,"totalnum,",len(settotal)+1
    except ZeroDivisionError:
        print tempdate, "huanyue"
        return [lastI, lastU, lastM]
    """market sentiment difference"""
    MSD = ITS - UTS  
    return [ITS, UTS, MSD]
if __name__ == '__main__':

    """read the csv file"""
    
    recorddate = []
    recorddata = []
    lastI = 0.0
    lastU = 0.0
    lastM = 0.0
    for year in range(2010, 2018):
        tempyear = str(year)
        for month in range(1, 13):
            if month < 10: tempmonth = "0" + str(month)
            else: tempmonth = str(month)
            for day in range(1, 32):
                if day < 10: tempday = "0" + str(day)
                else: tempday = str(day)
                tempdate = tempyear+tempmonth+tempday
                tempname = "data/"+tempdate+".csv"
                try:
                    test_csv = csv.reader(open(tempname))
                    result = caloneexcel(test_csv, tempdate, lastI, lastU, lastM)
                    lastI = result[0]
                    lastU = result[1]
                    lastM = result[2]
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
        if recorddata[i][0] >= 0: tempI = "%.9f" % recorddata[i][0]
        else: tempI = "%.8f" % recorddata[i][0]
        if recorddata[i][1] >= 0: tempU = "%.9f" % recorddata[i][1]
        else: tempU = "%.8f" % recorddata[i][1]
        if recorddata[i][2] >= 0: tempM = "%.9f" % recorddata[i][2]
        else: tempM = "%.8f" % recorddata[i][2]

        w.write(recorddate[i][2:]+" "+tempI+" "+tempU+" "+tempM+"\n")
    w.close()