# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 10:17:46 2021

@author: Victor
"""
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import scipy.io as sio
import csv as csv
from matplotlib import pyplot as plt  






#porcentaje a grados
def porctograd (alpha_porcentaje):
    if alpha_porcentaje <0:
        return (-1)*abs(np.arctan(alpha_porcentaje/100))*360/(2*np.pi)
    else:
        return np.arctan(alpha_porcentaje/100)*360/(2*np.pi)
        


    

# Curvas ascenso velocidad descendente
    
def pend1(x):
    if x>2400:
        return 85.329
    else:    
        return 87.8 - 2.44E-3*x+5.53E-7*x**2+0.2

def pend2(x):
    if x>2300:
        return 73.25
    else:
        return 87.4-0.0126*x+2.69E-6*x**2 +0.6   

def pend3(x):
    if x>2000:
        return 60.44
    else:
        return 88.6-0.0379*x+1.73E-5*x**2-2.62E-9*x**3-0.6

def pend4(x):
    if x>2400:
        return 47.87
    else:
        return 87.8-0.0539*x+2.55E-5*x**2-4.17E-9*x**3+0.2

def pend5(x):
    if x>1200:
        return 42.15
    else:
        return 89.8-1.8 - 0.096*x+7.28E-5*x**2-2.4E-8*x**3+2.89E-12*x**4

def pend6(x):
    if x>834:
        return 37.11
    else:
        return 90.4-2.4-0.116*x+8.47E-5*x**2-2.43E-8*x**3+2.16E-12*x**4

def pend7(x):
    if x>750:
        return 32.044
    else:
        return 91.1-3.1-0.141*x+1.15E-4*x**2-3.87E-8*x**3+4.53E-12*x**4

def pend8(x):
    if x>750:
        return 27.12
    else:
        return 90.3-2.3-.163*x+1.47E-4*x**2-5.64E-8*x**3+7.83E-12*x**4

# Caso descenso velocidad ascendente
    
def pend0(x):
    if x>2250:
        return 88
    else:
        return (1- 1/(np.e**((0.00330941091482836*x)**0.374329530769291)))*100
    
def pendm1(x):
    if x>1650:
        return 88
    else:
        return (1- 1/(np.e**((0.00455755241896724*x)**0.372499460534917)))*100
    
def pendm2(x):
    if x<150:
        return x*31/75
    if x>=150 and x<750:
        return x*13/300 + 111/2
    else:
        return 88
def pendm3(x):
    if x<150:
        return x*32/75
    if x>=150 and x<620:
        return x*23/450 + 169/3
    else:
        return 88

def pendm4(x):
    if x<150:
        return x*34/75
    if x>=150 and x<520:
        return x*2/37 + 2216/37 
    else:
        return 88   
    
def pendm5(x):
    if 0<=x<150:
        return x*72/150
    if x>=150 and x<450:
        return x*4/75+64
    if x>=450:
        return 88    
    
def pendm6(x):
    if x<150:
        return x*74.5/150
    if x>=150 and x<450:
        return x*0.045 + 67.75
    else:
        return 88      

def pendm7(x):
    if x<150:
        return x*77.7/150
    if x>=150 and x<300:
        return x*0.06313 + 68.23
    else:
        return 88     
    
def pendm8(x):
    if x<150:
        return x*80.9/150
    if x>=150 and x<300:
        return x*0.04733 + 73.8
    else:
        return 88  
    
def penda1(x):
    if x==0:
        return 0
    if x>0:
        return -3.29+10.6*np.log(x)
    if x>3600:
        return 83.51
    
def penda2(x):
    if x==0:
        return 0
    if x>0:
        return 3.5+8.44*np.log(x)
    if x>2100:
        return 68.06 
    
def penda3(x):
    if x==0:
        return 0
    if x>0:
        return 6.39+6.91*np.log(x)
    if x>2026:
        return 59.001
    
def penda4(x):
    if x==0:
        return 0
    if x>0:
        return 7.24+5.92*np.log(x)
    if x>980:
        return 48.0143 
    
def penda5(x):
    if x==0:
        return 0
    if x>0:
        return 11.4+4.49*np.log(x)   
    if x>920:
        return 42.041 
    
def penda6(x):
    if 0<=x<=75:
        return x/3
    if 75<x<=150:
        return 19+2*x/25
    if 150<x<=300:
        return 29+x/75
    if 300<x<=450:
        return 29+x/75
    if 450<x<=600:
        return 32+x/150
    if 600<x<=1050:
        return 104/3+x/450
    if x>1050:
        return 37
    
def penda7(x):
    if x==0:
        return 0
    if  0<x<=150:
        return -1.11+5.14*np.log(x)
    if 150<x<=300:
        return 0.02906*x+20.28
    if 300<x<=450:
        return 25+x/75
    if 450<x<=750:
        return 59/2+x/300
    if x>750:
        return 32
        
def penda8(x):
    if x==0:
        return 0
    if 0<x<=75:
        return -2.77+4.64*np.log(x)  
    if 75<x<=285:
        return x*0.03653+14.52  
    if 285<x<=450:
        return 23+x/150
    if 450<x<=750:
        return 49/2+x/300
    if x>750:
        return 27    
    
    

#GRAFICANDO PERFIL DE CONDUCCIÓN       
x = range(0,3600)
y1 = [pendm5(i) for i in x]
y2 = [pendm4(i) for i in x]
y3 = [pendm3(i) for i in x]
y4 = [pendm2(i) for i in x]
y5 = [pendm1(i) for i in x]
y6 = [pend0(i) for i in x]
y7 = [penda1(i) for i in x]
y8 = [penda2(i) for i in x]
y9 = [penda3(i) for i in x]
y10 = [penda4(i) for i in x]
y11 = [penda5(i) for i in x]
y12 = [penda6(i) for i in x]
y13 = [penda7(i) for i in x]
y14 = [penda8(i) for i in x]

plt.plot(x,y1,'-',linewidth=2,color='b',label='-5%')

plt.plot(x,y2,'-',linewidth=2,color='g',label='-4%')

plt.plot(x,y3,'-',linewidth=2,color='r',label='-3%')

plt.plot(x,y4,'-',linewidth=2,color='c',label='-2%')

plt.plot(x,y5,'-',linewidth=2,color='m',label='-1%')

plt.plot(x,y6,'-',linewidth=2,color='y',label='0%')

plt.plot(x,y7,'-',linewidth=2,color='k',label='1%')

plt.plot(x,y8,'-',linewidth=2,color='lawngreen',label='2%')

plt.plot(x,y9,'-',linewidth=2,color='coral',label='3%')

plt.plot(x,y10,'-',linewidth=2,color='sienna',label='4%')

plt.plot(x,y11,'-',linewidth=2,color='darkslategrey',label='5%')

plt.plot(x,y12,'-',linewidth=2,color='fuchsia',label='6%')

plt.plot(x,y13,'-',linewidth=2,color='pink',label='7%')

plt.plot(x,y14,'-',linewidth=2,color='g',label='8%')
plt.grid()
# plt.axis('equal')
plt.xlabel('Distancia de la pendiente [m]')
plt.ylabel('Velocidad [km/h]')
plt.title('Velocidad de operación en función de la pendiente')
plt.xlim(0,3600)
plt.ylim(0,90)
plt.legend()
plt.show()

# x = range(0,3600)
# z1 = [pend1(i) for i in x]
# z2 = [pend2(i) for i in x]
# z3 = [pend3(i) for i in x]
# z4 = [pend4(i) for i in x]
# z5 = [pend5(i) for i in x]
# z6 = [pend6(i) for i in x]
# z7 = [pend7(i) for i in x]
# z8 = [pend8(i) for i in x]
# plt.plot(x,z1,'-',linewidth=2,color='b',label='1%')

# plt.plot(x,z2,'-',linewidth=2,color='g',label='2%')

# plt.plot(x,z3,'-',linewidth=2,color='r',label='3%')

# plt.plot(x,z4,'-',linewidth=2,color='c',label='4%')

# plt.plot(x,z5,'-',linewidth=2,color='m',label='5%')

# plt.plot(x,z6,'-',linewidth=2,color='y',label='6%')

# plt.plot(x,z7,'-',linewidth=2,color='k',label='7%')

# plt.plot(x,z8,'-',linewidth=2,color='lawngreen',label='8%')
# plt.grid()
# # plt.axis('equal')
# plt.xlabel('Distancia de la pendiente [m]')
# plt.ylabel('Velocidad [km/h]')
# plt.title('Velocidad de operación en función de la pendiente')
# plt.xlim(0,3600)
# plt.ylim(0,90)
# plt.legend()
# plt.show() 

        

        
             
                