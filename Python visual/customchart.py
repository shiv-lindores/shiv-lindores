#the following code has been sanitized to exclude company sensitive data 

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter
from matplotlib.font_manager import FontProperties

font = FontProperties(weight = 'bold')

column_map = {
    'SHIPMENT FY': 'SHIPMENT',
    'DPPM FOR ALL FY': 'DPPM',
    'RPPM FOR ALL FY': 'RPPM', 
    'RETURN FOR ALL FY': 'INCIDENT' 
}

colors = {
    'DPPM FOR ALL FY': '#FFE135',
    'RPPM FOR ALL FY': '#00FFFF', 
    'RETURN FOR ALL FY': '#FA9A85' 
}

decimal_numbers = ['DPPM FOR ALL FY', 'RPPM FOR ALL FY']
decimal_numbers = [col for col in decimal_numbers if col in dataset.columns] #conditional formatting - if DPPM/RRPM aren't in dataset then don't apply
dataset[decimal_numbers] = dataset[decimal_numbers].round(2) #rounding numbers to 2 decimal places

def millions(x, pos):
    return '%1.0fM' % (x * 1e-6)

def format_tick(val, pos):
     return f'{val: .0f}'

formatter = FuncFormatter(millions)
formatter2 = FuncFormatter(format_tick)

fig, (ax1, ax2) = plt.subplots(2,1, figsize=(20,10), gridspec_kw={'height_ratios': [3,1]})

primary_y_cols = ['SHIPMENT FOR ALL FY']
secondary_y_cols = ['DPPM FOR ALL FY', 'RPPM FOR ALL FY', 'RETURN FOR ALL FY']

if primary_y_cols[0] in dataset.columns:
    ax1.bar(dataset['Year/Quarter'], dataset[primary_y_cols[0]], align='center', width=0.35, color='#5D009F', label=column_map[primary_y_cols[0]])
    ax1.set_ylabel('SHIPMENT', fontsize=20, color='#573B92', fontproperties=font)
    ax1.yaxis.set_major_formatter(formatter)
    ax1.xaxis.set_visible(False)
    ax1.tick_params(axis='y', labelsize=17)

ax3 = ax1.twinx()

max_vals = []
for col in secondary_y_cols:
    if col in dataset.columns:
        ax3.plot(dataset['Year/Quarter'], dataset[col], marker='o', label=column_map[col], linewidth=4, markersize=10, color=colors[col])
        max_vals.append(dataset[col].max())
        ax3.tick_params(axis='y', labelsize=17)

if max_vals:
    max_y = max(max_vals)
    ax3.yaxis.set_major_formatter(formatter2)
    ax3.set_ylim(0, max_y * 1.1)

handles1, labels1 = ax1.get_legend_handles_labels()
handles3, labels3 = ax3.get_legend_handles_labels()
ax3.legend(handles1 + handles3, labels1 + labels3, loc='upper left', fontsize=14)

ax1.set_xlabel('')
ax1.set_xticklabels(dataset['Year/Quarter'], rotation=0)
ax1.tick_params(axis='x', which='both', length=0)
ax3.set_ylabel('DPPM, RPPM and INCIDENT', fontsize=20, color='#573B92', fontproperties=font)

def format_numbers(value):
    value_float = float(value)
    if value_float >= 1000000:
        return f'{value / 1000000:.1f}M'
    elif value_float >= 1000:
        return f'{value / 1000:.1f}K'
    else:
        return str(value_float)

if 'SHIPMENT FOR ALL FY' in dataset.columns:
    dataset['SHIPMENT FOR ALL FY'] = dataset['SHIPMENT FOR ALL FY'].apply(format_numbers)

renamed_columns = {key: column_map[key] for key in column_map if key in dataset.columns}

table_dataset = dataset.rename(columns=renamed_columns)

transposed_dataset = table_dataset.set_index('Year/Quarter').transpose()

table = ax2.table(cellText=transposed_dataset.values, rowLabels=transposed_dataset.index, colLabels=transposed_dataset.columns, loc='center',cellLoc='center', rowLoc='center')
ax2.axis('off')
ax2.set_position([0,0.03,1,0.2])

cellDict = table.get_celld()


for (row, col), cell in cellDict.items():
    if row == 0:
        cell.set_facecolor('#5D009F')
        cell.set_height(0.16)
        cell.set_text_props(color = '#FFFFFF', fontproperties=font)
        cell.set_edgecolor('blue')
    elif col == -1:
        cell.set_text_props(color = '#5D009F', fontproperties=font)
        cell.set_height(0.15)
        cell.visible_edges = 'R'  
        cell.set_edgecolor('blue')
    else:
        cell.set_text_props(color = '#5D009F', fontproperties=font)
        cell.set_height(0.15) 
        cell.visible_edges = 'horizontal'
        cell.set_edgecolor('#E5E5E5')  
    cell.set_text_props(horizontalalignment='center', verticalalignment='center', fontsize=17)
    
    
plt.tight_layout()

plt.show()