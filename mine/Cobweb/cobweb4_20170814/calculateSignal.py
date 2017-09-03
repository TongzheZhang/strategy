# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 11:34:52 2017

@author: Richard10ZTZ
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Aug 03 13:37:25 2017
calculate from one excel
@author: Richard10ZTZ
"""
import re


def caloneexcel(test_csv, tempdate):
    """find out the blank row"""
    beginrow = []
    beginrow.append(7)
    endrow = []    

    for i in range(6, len(lines)):
        if lines[i] == "\n":
            beginrow.append(i+2)
            endrow.append(i-2)
            break

    
    for i in range(beginrow[1]+2, len(lines)):
        if lines[i] == "\n":
            beginrow.append(i+2)
            endrow.append(i-2)
            break   
        
    for i in range(beginrow[2]+2, len(lines)):
        if lines[i] == "\n":
            endrow.append(i-2)
            break   
    tradecom = []
    longcom = []
    shortcom = []
    M = 30
    N = 20
    """find out the major company"""
    tradingC = []
    longC = []
    shortC = []
    for i in range(beginrow[0], endrow[0]+1):
        test = re.split('\t\t|\t', lines[i])[:4]
        try:
            if int(test[2].replace(",","")) >= M:
                tradecom.append(test)
                tradingC.append(test[1])
        except IndexError:
            return 4
                
    try:        
        for i in range(beginrow[1], endrow[1]+1):
            test = re.split('\t\t|\t', lines[i])[:4]
            longcom.append(test)
            longC.append(test[1])
    
        for i in range(beginrow[2], endrow[2]+1):
            test = re.split('\t\t|\t', lines[i])[:4]
            shortcom.append(test)
            shortC.append(test[1])
    except IndexError:
        return 4
    set1 = set(tradingC)
    set2 = set(longC)
    set3 = set(shortC)
    settotal = set1 & set2 & set3 
    settotal = list(settotal)  
    total = []

    for i in range(0, len(settotal)):
        temp = []
        temp.append(settotal[i])
        for j in range(0, len(tradingC)):
            if tradingC[j] == settotal[i]:
                temp.append(float(tradecom[j][2].replace(",","")))
                temp.append(float(tradecom[j][3].replace(",","")))
        for k in range(0, len(longC)):
            if longC[k] == settotal[i]:
                temp.append(float(longcom[k][2].replace(",","")))
                temp.append(float(longcom[k][3].replace(",","")))
        for l in range(0, len(shortC)):
            if shortC[l] == settotal[i]:
                temp.append(float(shortcom[l][2].replace(",","")))
                temp.append(float(shortcom[l][3].replace(",","")))                
        total.append(temp)
    
    for i in range(0, len(settotal)):
        stat = (total[i][3]+total[i][5])/total[i][1]
        total[i].append(stat)
    newtotal = sorted(total, key=lambda stati:stati[7], reverse=1)
    
    itotal = newtotal[:N]
    utotal = newtotal[N:]
    TSI = 0.0
    TSU = 0.0
    ITS = 0.0
    UTS = 0.0
    Icannotuse = 0
    Ucannotuse = 0
    for i in range(0, len(itotal)):
        try:
            TSI = TSI + (itotal[i][4]-itotal[i][6])/(abs(itotal[i][4])+abs(itotal[i][6]))
        except ZeroDivisionError:
            Icannotuse = Icannotuse +1 
        
    ITS = TSI/(len(itotal)-Icannotuse)
    for i in range(0, len(utotal)):
        try:
            TSU = TSU + (utotal[i][4]-utotal[i][6])/(abs(utotal[i][4])+abs(utotal[i][6]))
        except ZeroDivisionError:
            Ucannotuse = Ucannotuse +1
    try:
        UTS = TSU/(len(utotal)-Ucannotuse)    
        if ITS>UTS:
            signal = 1
        elif ITS<UTS:
            signal = 2
        else:
            signal = 3
    except ZeroDivisionError:
        print "signal is not normal"
        signal = 4
    return signal
if __name__ == '__main__':

    """read the csv file"""
    observationPeriod = 120
    recorddate = []
    recorddata = []
    for year in range(2000, 2018):
        tempyear = str(year)
        for month in range(1, 13):
            if month < 10: tempmonth = "0" + str(month)
            else: tempmonth = str(month)
            for day in range(1, 32):
                if day < 10: tempday = "0" + str(day)
                else: tempday = str(day)
                tempdate = tempyear+tempmonth+tempday
                '''修改这里!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'''
                tempname = "../jm/"+tempdate+"_jm.txt" 
                try:
                    test_txt = open(tempname,"r")  
                    lines = test_txt.readlines()#读取全部内
                    result = caloneexcel(test_txt, tempdate) 
                    recorddate.append(tempdate)
                    recorddata.append(result)
                    #print result
                except IOError:
                    print tempdate," not have this day"
                    pass
    
    """testing
              
    test_txt = open("../i/20131018_i.txt","r")  
    lines = test_txt.readlines()#读取全部内
    result = caloneexcel(test_txt, "20170818") 
    """
    
    """write data into .txt"""
    """修改这里！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！"""
    w = open("finaldata_jm.txt","w")
    for i in range(observationPeriod, len(recorddate)):
        w.write(recorddate[i][2:]+" "+str(recorddata[i])+"\n")
    w.close()
    print "finish！"
    