# -*- coding: utf-8 -
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


import yfinance as yf

from bokeh.io import output_file, output_notebook, curdoc
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.layouts import row, column, gridplot
from bokeh.models.widgets import Tabs, Panel


from bokeh.models import CheckboxButtonGroup, CheckboxGroup, CustomJS, Dropdown, Select

output_notebook()

output_file('first_glyphs.html', title='Companies Stock Price')



stock = yf.Ticker("aapl")
stock = stock.history(period="1y")

        
data = ColumnDataSource(data = {'Ticker Open': stock['Open'],
                                'Ticker Close': stock['Close'],
                                'Ticker': stock['Close'],
                                'Date': stock.index})


# Create and configure the figure
fig = figure(x_axis_type='datetime',
             plot_height=300, plot_width=600,
             title='Stocks Value',
             x_axis_label='Date', y_axis_label='Price',
             toolbar_location=None)


#lineClose = fig.line('Date','Open',source=data, color='red', alpha=0.5)
#lineOpen = fig.line('Date','Close',source=data, color='navy', alpha=0.5)
# Move the legend to the upper left corner
#fig.legend.location = 'top_left'

lineClose = fig.line(x='Date', y='Ticker Open', source=data, color='red', alpha=0.5)
lineOpen = fig.line(x='Date', y='Ticker Close', source=data, color='navy', alpha=0.5)

#lineClose.visible=False
#lineOpen.visible=False

menu = Select(options=['AAPL', 'MSFT', 'AMZN', 'TSLA', 'FB',
                       'GOOG', 'PYPL', 'CMSCA', 'ADBE'], 
              value='AAPL', title='Company')
lines = ["Open", "Close"]

checkbox = CheckboxGroup(labels=lines, active=[0,1])
# Add callback to widgets
def callback(attr, old, new):
    if new == 'AAPL': 
        stock = yf.Ticker("aapl")
    elif new == 'MSFT': 
        stock = yf.Ticker("msft")
    elif new == 'AMZN': 
        stock = yf.Ticker("amzn")
    elif new == 'TSLA': 
        stock = yf.Ticker("tsla")
    elif new == 'FB': 
        stock = yf.Ticker("fb")
    elif new == 'GOOG': 
        stock = yf.Ticker("goog")
    elif new == 'PYPL': 
        stock = yf.Ticker("pypl")
    elif new == 'CMCSA': 
        stock = yf.Ticker("cmcsa")
    elif new == 'ADBE': 
        stock = yf.Ticker("adbe")
    
    stock = stock.history(period="1y")
    data.data = {'Ticker Open': stock['Open'],
                                'Ticker Close': stock['Close'],
                                'Date': stock.index}


def callback2(attr, old, new):
    if checkbox.active == [0]:
        lineClose.visible = False
        lineOpen.visible = True
    elif checkbox.active == [1]:
        lineOpen.visible = False
        lineClose.visible = True
    elif checkbox.active == [0,1]:
        lineOpen.visible = True
        lineClose.visible = True
    else:
        lineOpen.visible = False
        lineClose.visible = False
        
        
        

# Arrange plots and widgets in layouts

# Render the race as step lines
checkbox.on_change('active', callback2)
menu.on_change('value', callback)

layout = row(menu, fig, checkbox) 

curdoc().add_root(layout)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(debug=False)
