#This code is developed to calculate directly Frequency (F) vs Resistivity (Ω) and Frequency (F) vs -phase shift (mrad) for PSIP unit. Water and sediment sample has been measured 
# with PSIP unit and the subsequent plot has been analysized to find the plots in one page.
import math
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

#Please Chnage the Data Directory
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

# Create the figure and subplots
fig, axes = plt.subplots(len(Sediment_files), 1, figsize=(8, 12), sharex=True, sharey=True)

# Set the title outside the loop
fig.suptitle('Frequency vs ρ [Ωm]', fontsize=16)

for i, (sediment_file, water_file) in enumerate(zip(Sediment_files, Water_files)):
    sediment_df = pd.read_csv(sediment_file, skiprows=28)
    water_df = pd.read_csv(water_file, skiprows=28)
    sediment_filename = os.path.splitext(os.path.basename(sediment_file))[0][:-2]
    water_filename = os.path.splitext(os.path.basename(water_file))[0][:-2]
    
    sediment_df = process_dataframe(sediment_df)
    water_df = process_dataframe(water_df)
    
    sediment_dfs.append(sediment_df)
    water_dfs.append(water_df)


    # Plot onto the corresponding subplot
    axes[i].plot(sediment_df['Frequency[Hz]'], sediment_df['rho [Ohm*m]'], label=sediment_filename, color='brown')
    axes[i].plot(water_df['Frequency[Hz]'], water_df['rho [Ohm*m]'], label=water_filename, color='blue')
    axes[i].set_xlabel('Frequency (Hz)')
    axes[i].set_ylabel('ρ (Ωm)')
    axes[i].set_xscale('log')
    axes[i].legend()
    axes[i].grid(True)
plt.tight_layout()
plt.show()


fig, axes = plt.subplots(len(Sediment_files), 1, figsize=(8, 12), sharex=True, sharey=True)

# Set the title outside the loop
fig.suptitle('Frequency vs -phase shift[mrad]', fontsize=16)

for i, (sediment_file, water_file) in enumerate(zip(Sediment_files, Water_files)):
    sediment_df = pd.read_csv(sediment_file, skiprows=28)
    water_df = pd.read_csv(water_file, skiprows=28)
    sediment_filename = os.path.splitext(os.path.basename(sediment_file))[0][:-2]
    water_filename = os.path.splitext(os.path.basename(water_file))[0][:-2]
    
    sediment_df = process_dataframe(sediment_df)
    water_df = process_dataframe(water_df)
    
    sediment_dfs.append(sediment_df)
    water_dfs.append(water_df)


    axes[i].plot(sediment_df['Frequency[Hz]'], sediment_df['neg Phase [rad]'], label=sediment_filename, color='brown')
    axes[i].plot(water_df['Frequency[Hz]'], water_df['neg Phase [rad]'], label=water_filename, color='blue')
    axes[i].set_xlabel('Frequency (Hz)')
    axes[i].set_ylabel('- φ (mrad)')
    axes[i].set_xscale('log')
    axes[i].legend()
    axes[i].grid(True)

plt.tight_layout()
plt.show()

print(sediment_dfs)
