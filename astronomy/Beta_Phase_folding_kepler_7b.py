#!/usr/bin/env

import numpy as np 
import matplotlib.pyplot as plt 


file = 'kepler-7b.txt'

time_data = np.loadtxt(file,usecols=1)
flux_data = np.loadtxt(file,usecols=2)

w,= np.where((time_data>=time_data[0])&(time_data<=time_data[-1]))      
label = np.column_stack((w,time_data[w],flux_data[w]))

time_of_mid_transit = 2454957.501

while True:
    print('example : 4.885days',',','exit=ctrl+z')
    
    try:
        transit_period = float(input('transit_period :'))
        
    except ValueError:
        continue

    time_of_mid_transit_list = []

    for i in range(0,9,1):
        time= time_of_mid_transit
        real_time = time+(transit_period*i)
        time_of_mid_transit_list.append(real_time)

    print(time_of_mid_transit_list)

    '''
    for k in time_of_mid_transit_list:
        plt.axvline(x=k,color='red',linestyle='--',alpha=0.6)
    '''

    list = np.size(time_of_mid_transit_list)

    time_phase_folding_list = [] 
    flux_phase_folding_list = []

    for j in range (list):
        center = time_of_mid_transit_list[j]
        mask = (time_data>= center -0.3 ) & (time_data<= center+0.3)

        time_phase_folding = time_data[mask] - center
        flux_phase_folding = flux_data[mask]
        
        time_phase_folding_list.append(time_phase_folding)
        flux_phase_folding_list.append(flux_phase_folding)

    plt.figure(figsize=(10,5))

    for t,f in zip(time_phase_folding_list, flux_phase_folding_list):
        plt.plot(t,f)
        
    plt.xlim(-0.3,0.3)
    plt.title('Phase folding')
    plt.xlabel('Time')
    plt.ylabel('Relative flux')
    plt.show()
    
    print("Transit period=", transit_period,"days")
    
