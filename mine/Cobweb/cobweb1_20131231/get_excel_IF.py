# -*- coding: utf-8 -*-
"""
Created on Wed Aug 02 15:51:43 2017
get excel of trading information, begin from 2011.4.16
@author: Richard10ZTZ
"""


from time import sleep
import urllib2

def downloadexcel(url, year, month, day):
    u=urllib2.urlopen(url)
    data=u.read()
    #print data
    if "DOCTYPE" in data:
        print "haven't this day", url
    else:
        #print "have this day"
        newname = "data/"+year+month+day+".csv"
        f=open(newname,'wb')
        f.write(data)
        f.close()   
  
if __name__ == "__main__":


    for years in range(2013, 2018):
        tempyear = str(years)
        for monthes in range(1, 13):
            if monthes < 10:
                tempmonth = "0"+ str(monthes)
            else:
                tempmonth = str(monthes)
            for days in range(1, 32):
                if days < 10:
                    tempday = "0"+ str(days)
                else:
                    tempday = str(days)
                useurl = "http://www.cffex.com.cn/sj/ccpm/"+tempyear+tempmonth+"/"+tempday+"/IF_1.csv"
                downloadexcel(useurl, tempyear, tempmonth, tempday)

        
