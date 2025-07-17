#!/usr/bin/env

import numpy as np 
import matplotlib.pyplot as plt 

# File name (must be in the same directory as this script)
file = 'kepler-7b.txt'  

# Load time and flux data from the file
time_data = np.loadtxt(file, usecols=1)
flux_data = np.loadtxt(file, usecols=2)

# Label the data by combining index, time, and flux into a single array
w, = np.where((time_data >= time_data[0]) & (time_data <= time_data[-1]))      
label = np.column_stack((w, time_data[w], flux_data[w]))

# Print the total number of data points
print("Index size =", np.size(time_data))

# Repeatedly ask the user for a range of indices until they choose to exit
while True:
    print('example type 150')
    min_index_input = input("min_index_value: ")
    if min_index_input.lower() == 't':
        print('byebye')
        break

    print('example type 250')
    max_index_input = input("max_index_value: ")
    if max_index_input.lower() == 't':
        print('byebye')
        break
    
    try:
        time_min_value = int(min_index_input)
        time_max_value = int(max_index_input)
    except ValueError:
        print('Please type a number or "t" to exit.')
        continue
    
    # Select the subset of data within the specified index range
    subset = label[time_min_value : time_max_value]

    # Find the point of minimum flux in the selected range (likely mid-transit)
    min_row = subset[np.argmin(subset[:, 2])]
    estimated_t0 = min_row[1]  # Time of minimum flux

    # Define a window around the estimated mid-transit time (±0.3 days)
    mask = (time_data > estimated_t0 - 0.3) & (time_data < estimated_t0 + 0.3)
    time_cut_data = time_data[mask]
    flux_cut_data = flux_data[mask]

    # Compute the gradient of flux with respect to time
    d_flux_dt = np.gradient(flux_cut_data, time_cut_data)
    value = 0.01  # Threshold to detect steep changes

    # Identify ingress and egress points based on gradient threshold
    first_flux_index = np.where(d_flux_dt < -value)[0][0]
    final_flux_index = np.where(d_flux_dt > value)[0][-1]

    # Get the times of the ingress and egress points
    time_first = time_cut_data[first_flux_index]
    time_final = time_cut_data[final_flux_index]

    # Estimate mid-transit time as the midpoint between ingress and egress
    estimated_time_of_mid_transit = (time_first + time_final) / 2

    ''' 
    # Uncomment to show additional information about the minimum point
    print("Minimum flux value =", min_row[2])
    print("Index of minimum flux =", min_row[0])                                    
    print("Time of minimum flux =", min_row[1])
    
    # Plot the selected range and mark the minimum flux point
    plt.plot(subset[:, 1], subset[:, 2])                                      
    plt.plot(min_row[1], min_row[2], 'ro', label="Minimum Value", markersize=7)
    '''

    # Plot the trimmed light curve and highlight the key points
    plt.plot(time_cut_data, flux_cut_data, label='Flux')
    plt.plot(time_first, flux_cut_data[first_flux_index], 'bo', label='first point')
    plt.plot(time_final, flux_cut_data[final_flux_index], 'go', label='final point')

    # Draw a vertical line at the estimated mid-transit time
    plt.axvline(estimated_time_of_mid_transit, color='red', linestyle='--', label='Estimated t₀')

    plt.xlabel('Time')
    plt.ylabel('Relative Flux')
    plt.title('Transit Light Curve with Mid-Transit Estimation')
    plt.legend()

    # Print the key timing values
    print("First (ingress) point =", time_first)
    print("Final (egress) point =", time_final)
    print("Estimated mid-transit time =", estimated_time_of_mid_transit)
    plt.show()

    print('To analyze another range, enter new index values.')
    print('To exit, type "t".')
