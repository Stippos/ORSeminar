import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression as LR
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
from sklearn.metrics import confusion_matrix

data = pd.read_csv("dataset_raw.csv")
data_na = np.array(data)
payments = data.iloc[:,6:24]

payments.head()

data_plus = data

data_plus.insert(loc = 12, column = "Overdraft", value = data_na[:,1] - data_na[:,12])

plt.hist(data["Default"] + 2)

defaults = data_na[np.where(data_na[:,1] - data_na[:,12] < 0), 24]
defaults = defaults[0]

print("Ratio of overdrafted defaulters: " + str(np.sum(defaults) / len(defaults)))
print("Ratio of all defaulters: " + str(np.sum(data["Default"].values) / len(data["Default"].values)))
print(defaults)

penalties = 0
for j in range(6,24):
    for i in range(0,30000):
        if(data_na[i,j] > 0){
            penalties = penalties + 1
        }

penalties 
#financial impact
#the bank recieves 2% of every transaction
#late payment penalty 20
#interchange rate 2%
#annual credit card fee 75
#cash advance fee 5%
#average cash advance volume 300

#NIBT
# Annual fees = number of credit cards * annual fee = 75 * 2200000 * 1.3
# Annual cash advance volume * average fee = Annual volume *
