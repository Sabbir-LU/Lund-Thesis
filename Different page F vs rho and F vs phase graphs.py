# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 00:22:20 2024

@author: ahmed
"""
#Final Code for Graph 1 (For Each Sample Spot)

import math
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

Sediment_path = 'D:/Thesis/Lab Measurement/Long measurement/Altered/Sediment'
Water_path = 'D:/Thesis/Lab Measurement/Long measurement/Altered/Water'

Sediment_files = glob.glob(Sediment_path + '/*.csv')
Water_files = glob.glob(Water_path + '/*.csv')

sediment_dfs = []
water_dfs = []

def process_dataframe(df):
    df = df.dropna(axis=0, how='all')  
    df = df.dropna(axis=1, how='all')  
    df = df.drop(columns=["AO_sampling_rate", "TimeStamp[Sec]", "Loop", "Seq. Loop"])
    df['neg Phase [rad]'] = df['Phase_Shift[rad]'] * (-1000)
    df['rho [Ohm*m]'] = df['Impedance[Ohms]'] * 0.006138
    df['real part conductivity [S/m]'] = (1 / df['rho [Ohm*m]']) * df['Phase_Shift[rad]'].apply(math.cos)
    df['imag part conductivity [S/m]'] = (-1 / df['rho [Ohm*m]']) * df['Phase_Shift[rad]'].apply(math.sin)
    return df

def plot_data_rho(sediment_df, water_df, sediment_filename, water_filename):
    plt.figure(figsize=(8, 6))
    plt.plot(sediment_df['Frequency[Hz]'], sediment_df['rho [Ohm*m]'], label=sediment_filename, color='brown')
    plt.plot(water_df['Frequency[Hz]'], water_df['rho [Ohm*m]'], label=water_filename, color='blue')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('rho [Ohm*m]')
    plt.title('Frequency vs ρ')
    plt.xscale('log')
    plt.legend()
    plt.grid(True)
    #plt.xlim(1e-2, 1e3)
    plt.savefig(os.path.join('D:/Thesis/Lab Measurement/Long measurement/Altered/Figure', f'{sediment_filename}_vs_{water_filename}_rho.png'))  # Save the figure
    plt.show()


def plot_data_phase(sediment_df, water_df, sediment_filename, water_filename):
    plt.figure(figsize=(8, 6))
    plt.plot(sediment_df['Frequency[Hz]'], sediment_df['neg Phase [rad]'], label=sediment_filename, color='brown')
    plt.plot(water_df['Frequency[Hz]'], water_df['neg Phase [rad]'], label=water_filename, color='blue')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('- Phase [mrad]')
    plt.title('Frequency vs Phase shift')
    plt.xscale('log')
    plt.legend()
    plt.grid(True)
    #plt.xlim(1e-2, 1e3)
    plt.savefig(os.path.join('D:/Thesis/Lab Measurement/Long measurement/Altered/Figure', f'{sediment_filename}_vs_{water_filename}_phase.png'))  # Save the figure
    plt.show()

for sediment_file, water_file in zip(Sediment_files, Water_files):
    sediment_df = pd.read_csv(sediment_file, skiprows=28)
    water_df = pd.read_csv(water_file, skiprows=28)
    
    sediment_filename = os.path.splitext(os.path.basename(sediment_file))[0]
    water_filename = os.path.splitext(os.path.basename(water_file))[0]
    print(sediment_filename, water_filename)
    
    sediment_df = process_dataframe(sediment_df)
    water_df = process_dataframe(water_df)

    sediment_dfs.append(sediment_df)
    water_dfs.append(water_df)
    
    sediment_df.to_excel(f'D:/Thesis/Lab Measurement/Long measurement/Altered/{sediment_filename}.xlsx', index=False)
    water_df.to_excel(f'D:/Thesis/Lab Measurement/Long measurement/Altered/{water_filename}.xlsx', index=False)

    plot_data_rho(sediment_df, water_df, sediment_filename, water_filename)
    plot_data_phase(sediment_df, water_df, sediment_filename, water_filename)
    
# Save all DataFrames to the same Excel file
#excel_writer.save()

print("Sediment Dataframes:", sediment_dfs)
print("Water Dataframes:", water_dfs)

