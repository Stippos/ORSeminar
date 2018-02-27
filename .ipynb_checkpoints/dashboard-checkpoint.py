#-*- encoding: UTF-8 -*-
import fi

import numpy as np
import pandas as pd 


from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput, MultiSelect, RangeSlider
from bokeh.plotting import figure
from bokeh.models.widgets import PreText

data_pd = pd.read_csv("dataset_raw.csv")
data_org = np.array(data_pd)

data = data_org

households = 2200000
ccAccountsPerHousehold = 0.85
fractionOfActiveCCAccounts = 0.6
avgCCsPerAccount = 1.3
avgAnnualPV = 5000
opexRate = 0.05
avgInterchangeRate = 0.02
shareOfPVOutstanding = 0.3
spreadMargin = 0.0125
cashAdvanceFee = 0.05
rewardRate = 0.05
latePaymentFee = 20
annualCCFee = 75
avgCashAdvanceVol = 300
#the amount of money recovered in default
collectionEfficiency = 0.1
defaultBiasModifier = 3

totalAccounts = households * ccAccountsPerHousehold
activeAccounts = totalAccounts * fractionOfActiveCCAccounts
totalCards = totalAccounts * avgCCsPerAccount 

# Set up data
N = 200
x = np.linspace(0, 4*np.pi, N)
y = np.sin(x)
source = ColumnDataSource(data_pd)


# Set up plot
plot = figure(plot_height=600, plot_width=600, title="my sine wave",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[20, 80], y_range=[0, 35000])

plot.vbar('ID','Age', source=source, line_width=3, line_alpha=0.6)


# Set up widgets
age = RangeSlider(title = "Age", start = 21, end = 79, value = (21, 79))
sex = MultiSelect(title = "Sex", value = ["Female"], options = ["Female", "Male"])
latitude = RangeSlider(title = "Latitude", start = 30, end = 50, value = (30, 50))
lognitude = RangeSlider(title = "Lognitude", start = -100, end = -75, value = (-100, -75))
married = MultiSelect(title = "Marital status", value = ["Married"], options = ["Married", "Single", "Other"])
education = MultiSelect(title = "Education", value = ["Graduate school"], options = ["Gradute School", "University", "High School", "Other"])
balanceLimit = RangeSlider(title = "Balance Limit", start = 300, end = 32300, value = (300, 32300))
currentLoan = RangeSlider(title = "Current Loan", start = 0, end = 31200, value = (0, 31200))
defaultRisk = RangeSlider(title = "Default Risk", start = 0, end = 100, value = (0, 100))


text = TextInput(title="title", value='my sine wave')
offset = Slider(title="offset", value=0.0, start=-5.0, end=5.0, step=0.1)
amplitude = Slider(title="amplitude", value=1.0, start=-5.0, end=5.0, step=0.1)
phase = Slider(title="phase", value=0.0, start=0.0, end=2*np.pi)
freq = Slider(title="frequency", value=1.0, start=0.1, end=5.1, step=0.1)


# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)

def update_data(attrname, old, new):

    # Get the current slider values
    a = amplitude.value
    b = offset.value
    w = phase.value
    k = freq.value

    # Generate the new curve
    x = np.linspace(0, 4*np.pi, N)
    y = a*np.sin(k*x + w) + b

    source.data = dict(x=x, y=y)

for w in [offset, amplitude, phase, freq]:
    w.on_change('value', update_data)

def update_features(attrname, old, new):
    a = age.value
    s = sex.value
    lat = latitude.value
    log = lognitude.value
    m = married.value
    e = education.value
    b = balanceLimit.value
    c = currentLoan.value
    d = defaultRisk.value

    update_dataset(a, s, lat, log, m, e, b, c, d)
    
for w in [age, sex, latitude, lognitude, married, education, balanceLimit, currentLoan, defaultRisk]:
    w.on_change('value', update_features)
    
def update_dataset(age, sex, latitude, lognitude, married, education, balanceLimit, currentLoan, defaultRisk):
    print(age)
    print(sex)
    print(latitude)
    print(lognitude)
    print(married)
    print(education)
    print(balanceLimit)
    print(currentLoan)
    print(defaultRisk)    
    
def description(dataset):
    impacts = []

    for i in range(0,len(dataset)):
        impacts.append(fi.impact(dataset[i,6:25]))
    
    #When active cards are filtered out it is also generalizesd for the entire population
    scaledActiveCards = 1683000 * len(dataset) / (30000) 
    
    impacts = np.array(impacts)
    
    activeCards = "Active cards: " + str(scaledActiveCards) + "\n"
    profit = "Total profit from data set: " + str(sum(impacts)) + "\n"
    avgProfit = "Average profit per customer: " + str(np.mean(impacts)) + "\n"
    medProfit = "Median profit: " + str(np.median(impacts)) + "\n"
    gains = "Number of gains: " + str(len(np.where(impacts > 0)[0])) + "\n"
    losses = "Number of losses: "+ str(len(np.where(impacts < 0)[0])) + "\n"
    avgGain = "Average gain: " + str(np.mean(impacts[np.where(impacts > 0)]))+ "\n"
    avgLoss = "Average loss: " + str(np.mean(impacts[np.where(impacts < 0)]))+ "\n"
    largestGain = "Largest gain: " + str(max(impacts))    + "\n"
    largestLoss = "Largest loss: " + str(min(impacts))+ "\n"
    nibt = "NIBT based on data: " + str(sum(impacts) / len(dataset) * scaledActiveCards + 75 * (totalCards - scaledActiveCards))+ "\n"
    
    return activeCards + profit + avgProfit + medProfit + gains + losses + avgGain + avgLoss + largestGain + largestLoss + nibt
    
stats = PreText(text=description(data), width=400)
    
# Set up layouts and add to document
inputs = widgetbox(age, sex, latitude, lognitude, married, education, balanceLimit, currentLoan, defaultRisk)

curdoc().add_root(row(inputs, plot, stats, width=800))
curdoc().title = "Kuutti Dashboard"