# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 17:27:25 2022

@author: Victor Toro Lara
"""
#this function returns the speed of the truck dependin on the RPM and some features depending on the wheel, gear and the axle. 
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import scipy.io as sio
import csv as csv
from matplotlib import pyplot as plt  

def rpmtokmh(p,pd,rpm,dneuma):
    return  rpm*2*np.pi*60*(dneuma*0.0245/2)/(1000*p*pd)

ps=[14.94,11.28,9.04,7.09,5.54,4.35,3.44,2.7,2.08,1.63,1.27,1]

for x in ps:
    print(x)
    print( rpmtokmh(x,2.64,1000,41.8))
    
