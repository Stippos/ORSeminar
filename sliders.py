#-*- encoding: UTF-8 -*-

import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput, MultiSelect, RangeSlider
from bokeh.plotting import figure
from bokeh.models.widgets import PreText


# Set up data
N = 200
x = np.linspace(0, 4*np.pi, N)
y = np.sin(x)
source = ColumnDataSource(data=dict(x=x, y=y))


# Set up plot
plot = figure(plot_height=400, plot_width=400, title="my sine wave",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, 4*np.pi], y_range=[-2.5, 2.5])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)


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

stats = PreText(text='Lörs \n lärs \n börs \n bärs', width=100)
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


# Set up layouts and add to document
inputs = widgetbox(age, sex, latitude, lognitude, married, education, balanceLimit, currentLoan, defaultRisk)

curdoc().add_root(row(inputs, plot, stats, width=800))
curdoc().title = "Sliders"