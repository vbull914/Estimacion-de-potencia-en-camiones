# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 18:55:04 2022

@author: Victor Toro Lara
"""
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import scipy.io as sio
import csv as csv
from matplotlib import pyplot as plt  


#Estos modelos buscan entregar el consumo de combustible de distintos motores en función de la potencia demandada. 

def consumomerce238(hp):
    if hp<=0:
        return 0
    if 0<hp<87.1:
        #return 0.291 + -1.53E-03*hp + 4.9E-06*hp**2
        return 0.305 + -1.79E-03*hp + 6.04E-06*hp**2
    if 87.1<=hp<120.6:
        return -0.00053*hp+0.24134
    if 120.6<=hp<144.72:
        return -0.00014*hp+0.193364
    if 144.72<=hp<167.5:
        return -0.00003*hp+0.17820
    if 167.5<=hp<194.3:
        return 0.00003*hp+0.165975
    if 194.3<=hp<238:
        return 0.00042*hp+0.09047
    
    if 238<=hp:
        print(hp,'¡EXCEDE POTENCIA MÁXIMA!')  
        return 200   


#Ecuaciones de consumo       
def consumomerce306(hp):
    if hp<=0:
        return 0
    if 0<hp<103.18:
        return 0.259 + -7.89E-04*hp + 1.83E-06*hp**2
    if 103.18<=hp<150.08:
        return -0.00028*hp+0.226111
    if 150.08<=hp<234.5:
        return -0.0001*hp+0.19924
    if 234.5<=hp<270.68:
        return 0.00007*hp+0.15631
    if 270.68<=hp<306:
        return 0.0004*hp+0.06707
    if 306<=hp:
        print(hp,'¡EXCEDE POTENCIA MÁXIMA!')  
        return 200
        
def consumomerce354(hp):
    if hp<=0:
        return 0
    if 0<hp<201:
        #return 0.292 + -9.41E-04*hp + 1.71E-06*hp**2
        #return 0.357 + -1.47E-03*hp + 2.78E-06*hp**2
        return 0.335 + -1.29E-03*hp + 2.43E-06*hp**2
    
    if 201<=hp<247.9:
        return -0.00017*hp+0.20721
    if 247.9<=hp<288.1:
        return -0.00002*hp+0.16964
    if 288.1<=hp<325.62:
        return 0.00014*hp+0.12246
    if 325.62<=hp<341.7:
        return 0.00055*hp-0.011325
    if 341.7<=hp<354:
        return 0.001*hp-0.16645
    
    if 354<=hp:
        print(hp,'¡EXCEDE POTENCIA MÁXIMA!')    
        return 200
    
def consumocummins350(hp):
    if hp<=0:
        return 0
    if 0<hp<281.4:
        #return 0.292 + -7.64E-04*hp + 1.19E-06*hp**2
        return 0.372 + -1.29E-03*hp + 2.06E-06*hp**2
    if 281.4<=hp<309.54:
        return -0.00006*hp+0.18855
    if 309.54<=hp<335:
        return (-1*1.96386E-7*hp)+0.16897
    if 335<=hp<349.74:
        return 0.00036*hp+0.04709
    if 349.74<=hp<352.42:
        return 0.002*hp-0.526515
    
    if 352.42<=hp:
        print(hp,'¡EXCEDE POTENCIA MÁXIMA!')   
        return 200    
    
def consumocummins460(hp):
    if hp<=0:
        return 0
    if 0<hp<341.7:
        #return 0.305 + -7.4E-04*hp + 9.68E-07*hp**2
        return 0.39 + -1.18E-03*hp + 1.54E-06*hp**2
    if 341.7<=hp<381.9:
        return -0.00002*hp+0.17299
    if 381.9<=hp<458.28:
        return 0.00004*hp+0.14664
    if 458.28<=hp<460.96:
        return 0.00334*hp-1.363989

    
    
    if 460.96<=hp:
        print(hp ,'¡EXCEDE POTENCIA MÁXIMA!')  
        return 200 
        
#%% Este es pa consumo especifico    
x1 = range(1,238)
x2 = range(1,306)
x3 = range(1,354)
x4 = range(1,350)
x5 = range(1,460)

y1 = [consumomerce238(i) for i in x1] 
y2 = [consumomerce306(i) for i in x2]
y3 = [consumomerce354(i) for i in x3]
y4 = [consumocummins350(i) for i in x4]
y5 = [consumocummins460(i) for i in x5]
   

#plt.plot(x1,y1,'-',linewidth=2,color='b',label='A 238 [hp]')
#plt.plot(x2,y2,'-',linewidth=2,color='r',label='A 306 [hp]')
#plt.plot(x3,y3,'-',linewidth=2,color='g',label='A 354 [hp]')
#plt.plot(x4,y4,'-',linewidth=2,color='m',label='B 350 [hp]')
#plt.plot(x5,y5,'-',linewidth=2,color='y',label='B 460 [hp]')

# plt.xlabel('Potencia [hp]')
# plt.ylabel('Consumo específico [L/hp h]')
# plt.title('Consumo específico de combustible frente a potencia')
# plt.xlim(0,460)
# plt.ylim(0,0.4)
# plt.legend()
# plt.show()

# #%%Este es pa consumo
x1 = range(1,238)
x2 = range(1,306)
x3 = range(1,354)
x4 = range(1,350)
x5 = range(1,460)

y1 = [consumomerce238(i)*i for i in x1] 
y2 = [consumomerce306(i)*i for i in x2]
y3 = [consumomerce354(i)*i for i in x3]
y4 = [consumocummins350(i)*i for i in x4]
y5 = [consumocummins460(i)*i for i in x5]
   

#plt.plot(x1,y1,'-',linewidth=2,color='b',label='A 238 [hp]')
#plt.plot(x2,y2,'-',linewidth=2,color='r',label='A 306 [hp]')
#plt.plot(x3,y3,'-',linewidth=2,color='g',label='A 354 [hp]')
plt.plot(x4,y4,'-',linewidth=2,color='m',label='B 350 [hp]')
plt.plot(x5,y5,'-',linewidth=2,color='y',label='B 460 [hp]')

plt.xlabel('Potencia [hp]')
plt.ylabel('Consumo [L/h]')
#plt.title('Consumo de combustible frente a potencia')

plt.legend()
plt.show()
