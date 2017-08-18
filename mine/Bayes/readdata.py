# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 16:40:18 2017

@author: Richard10ZTZ
"""

from WindPy import *
data=w.wsi("AU.SHF","open, high", "2017-08-17 8:58:00", "2017-08-17 15:01:00")
getdata = data.Data
field = data.Fields
time = data.Times

