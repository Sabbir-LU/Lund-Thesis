import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import viridis
from matplotlib.colors import Normalize
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Chnge this path for data
path = 'D:/Thesis/Lab Measurement/Long measurement/Altered/Final Data/Sediment rho CC and other plot.csv'


df = pd.read_csv(path)
df.columns = df.columns.str.strip() #remove white space

fig, axs = plt.subplots(3, 2, figsize=(12, 15))

parameters = ["σ'(S/m)", "σ''(S/m)", 'ρ10(Ωm)', 'Φ10(mrad)', 'ρCC(Ωm)', 'mDD']

cmap = viridis
norm = Normalize(vmin=0, vmax=len(df))

for i, param in enumerate(parameters): #subplot index
    row = i // 2
    col = i % 2
    
    for index, row_data in df.iterrows():
        sample_name = row_data['Sample']
        fe = row_data['Fe(mg/kg)']
        param_value = row_data[param]
        color = cmap(norm(index))
        
        axs[row, col].scatter(fe, param_value, label=sample_name, color=color)
        axs[row, col].text(fe + 0.5, param_value, sample_name, fontsize=10, ha='left', va='center', color='black')
        
        # Add subplot annotation like a), b), c), d)
        subplot_annotation = chr(97 + i)
        axs[row, col].text(0.1, 0.9, f"({subplot_annotation})", transform=axs[row, col].transAxes,
                           fontsize=14, va='top', ha='right')

        X = np.array(df['Fe(mg/kg)']).reshape(-1, 1)
        y = np.array(df[param])
        model = LinearRegression().fit(X, y)
        y_pred = model.predict(X)
        axs[row, col].plot(X, y_pred, color='gray', linestyle='--', markersize=4)

        r2 = r2_score(y, y_pred) #for r2
        axs[row, col].text(0.98, 0.75, f'R-squared: {r2:.2f}', transform=axs[row, col].transAxes,
                           fontsize=14, ha='right', va='top', color='black',
                           bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))


    axs[row, col].set_title(param, fontsize=16)
    axs[row, col].set_xlabel('Fe(mg/kg)', fontsize=16)
    axs[row, col].set_ylabel(param, fontsize=16)
plt.tight_layout()

plt.show()
