# -*- coding: utf-8 -
from flask import Flask, render_template, request, redirect


import yfinance as yf
import requests
from bokeh.io import output_file, output_notebook, curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.layouts import row, column, gridplot
from bokeh.models.widgets import Tabs, Panel
from bokeh.embed import components


from bokeh.models import CheckboxButtonGroup, CheckboxGroup, CustomJS, Dropdown, Select



def make_plot(tick, val_opn, val_clse):
    stock = yf.Ticker(tick)
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
    
    #menu = Select(options=['AAPL', 'MSFT', 'AMZN', 'TSLA', 'FB',
     #                      'GOOG', 'PYPL', 'CMSCA', 'ADBE'], 
      #            value='AAPL', title='Company')
    #lines = ["Open", "Close"]
    
    #checkbox = CheckboxGroup(labels=lines, active=[0,1])
    # Add callback to widgets
    #def callback(attr, old, new):
     #   if new == 'AAPL': 
      #      stock = yf.Ticker("aapl")
       # elif new == 'MSFT': 
   #         stock = yf.Ticker("msft")
    #    elif new == 'AMZN': 
     #       stock = yf.Ticker("amzn")
      #  elif new == 'TSLA': 
       #     stock = yf.Ticker("tsla")
   #     elif new == 'FB': 
    #        stock = yf.Ticker("fb")
     #   elif new == 'GOOG': 
      #      stock = yf.Ticker("goog")
       # elif new == 'PYPL': 
        #    stock = yf.Ticker("pypl")
   #     elif new == 'CMCSA': 
    #        stock = yf.Ticker("cmcsa")
     #   elif new == 'ADBE': 
      #      stock = yf.Ticker("adbe")
    stock = yf.Ticker(tick)    
    stock = stock.history(period="1y")
    data.data = {'Ticker Open': stock['Open'],
                 'Ticker Close': stock['Close'],
                 'Date': stock.index}
    
    
   # def callback2(attr, old, new):
    #    if checkbox.active == [0]:
     #       lineClose.visible = False
      #      lineOpen.visible = True
       # elif checkbox.active == [1]:
        #    lineOpen.visible = False
         #   lineClose.visible = True
#        elif checkbox.active == [0,1]:
 #           lineOpen.visible = True
  #          lineClose.visible = True
   #     else:
    #        lineOpen.visible = False
     #       lineClose.visible = False
            
            
    # Arrange plots and widgets in layouts
    
    # Render the race as step lines
   # checkbox.on_change('active', callback2)
    #menu.on_change('value', callback)
    
    #layout = row(menu, fig, checkbox) 
    #curdoc().add_root(layout)
    if val_opn == 'open' and val_clse != 'close':
        lineClose.visible = False
    if val_opn != 'open' and val_clse == 'close':
        lineOpen.visible = False
    if val_opn != 'open' and val_clse != 'close':
        lineOpen.visible = False
        lineClose.visible = False
    
    script, div = components(fig)
   # print(div)
    
    return script, div

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

ticker = 'AAPL'

@app.route('/', methods=['POST'])
def index2():
    # request was a POST
    global ticker
    global open_
    global close_
    ticker = request.form['ticker']
    if request.form.get('open') and not request.form.get('close'):
        open_ = 'open'
        close_ = 'open'
    if request.form.get('open') and request.form.get('close'):
        open_ = 'open'
        close_ = 'close'
    if not request.form.get('open') and request.form.get('close'):
        open_ = 'close'
        close_ = 'close'  
    if not request.form.get('open') and not request.form.get('close'):
        open_ = 'nothing'
        close_ = 'nothing'     
    #close_ = request.form['close']
    return redirect('/dashboard')

@app.route('/dashboard', methods=['GET', 'POST'])
def show_dashbaord(): 
    script, div = (make_plot(ticker, open_, close_))
    return render_template('dashboard.html', script=script, div=div)


if __name__ == '__main__':
  app.run(debug=True)
