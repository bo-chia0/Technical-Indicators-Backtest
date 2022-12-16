from tokenize import String
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def visualizer(title:String):
    df = pd.read_csv('Results/'+title+'.csv', header=0, index_col=0)
    plt.figure(figsize=(24,8))
    sns.heatmap(df, annot=True, cmap='coolwarm')
    plt.title(title, fontsize=20)
    plt.savefig('Results/'+title+'.png')


# visualizer('MA_Return')
# visualizer('MA_WinRate')
# visualizer('MA_Mean_Volatility_Ratio')


for file in os.listdir(os.getcwd()+'/Results'):
    if file.endswith('.csv'):
        visualizer(file[:-4])
