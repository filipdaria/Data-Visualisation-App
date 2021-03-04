import tkinter as tk 
import tkinter.font as font
import yfinance as yf
import pandas as pd
import mplcursors as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from pandas import DataFrame
import datetime
import dateutil.relativedelta
from currency_converter import CurrencyConverter
import numpy as np

root = tk.Tk()
root2=tk.Tk()

date_frame="1y"
current_stock="DB"
default_currency="USD"
wanted_currency="EUR"

current_label = None
c = CurrencyConverter()
default_indicator=None
wind=None

symbol_to_name = {'ING': 'ING', 'V': 'Visa', 'DB': 'Deutsche Bank', 'EBAY':'eBay','DAI.DE':'Daimler', 'LHA.DE':'Lufthansa','DPZ':"Domino's Pizza", 'IHG':'Intercontinental Hotels','RYAAY':'Ryanair', 'TM':'Toyota'}
index_to_symbol = {0: 'ING', 1: 'V', 2: 'EBAY', 3: 'DAI.DE',4: 'TM',5: 'RYAAY',6: 'LHA.DE',7: 'DB',8: 'DPZ',9: 'IHG'}

#set time frame

def set_1days():
    global date_frame
    date_frame="1d"
    update_text()

def set_5days():
    global date_frame
    date_frame="5d"
    update_text()

def set_1months():
    global date_frame
    date_frame="1mo"
    update_text()

def set_3months():
    global date_frame
    date_frame="3mo"
    update_text()

def set_6months():
    global date_frame
    date_frame="6mo"
    update_text()

def set_1year():
    global date_frame
    date_frame="1y"
    update_text()

#set stock

def set_ebay():
    global current_stock
    current_stock="EBAY"
    update_text()

def set_dominos():
    global current_stock
    current_stock="DPZ"
    update_text()

def set_intercont():
    global current_stock
    current_stock="IHG"
    update_text()

def set_visa():
    global current_stock
    current_stock="V"
    update_text()

def set_db():
    global current_stock
    current_stock="DB"
    update_text()

def set_lufthansa():
    global current_stock
    current_stock="LHA.DE"
    update_text()

def set_daimler():
    global current_stock
    current_stock="DAI.DE"
    update_text()
    
def set_ryanair():
    global current_stock
    current_stock="RYAAY"
    update_text()

def set_ing():
    global current_stock
    current_stock="ING"
    update_text()

def set_toyota():
    global current_stock
    current_stock="TM"
    update_text()

#set currency

def set_usd():
    global wanted_currency
    wanted_currency="USD"
    update_text()
    

def set_eur():
    global wanted_currency
    wanted_currency="EUR"
    update_text()

def set_gbp():
    global wanted_currency
    wanted_currency="GBP"
    update_text()

def set_chf():
    global wanted_currency
    wanted_currency="CHF"
    update_text()

def set_ron():
    global wanted_currency
    wanted_currency="RON"
    update_text()


def currency_converter(df_converted,new_currency):
     amount = df_converted["Close"]
     curr="USD"
     new_curr = c.convert(amount,curr,new_currency)
     return new_curr

#set window for standard deviation and bollinger bands

def set_window(date_frame):
    global wind
    if (date_frame=="1mo" or date_frame=="3mo"):
        wind=5
    elif (date_frame=="1y" or date_frame=="6mo"):
        wind=20

#set indicator

def set_rsi():
    global default_indicator
    default_indicator="RSI"

def set_mavg():
    global default_indicator
    default_indicator="MAVG"

def set_bollinger():
    global default_indicator
    default_indicator="Bollinger Bands"

def set_std():
    global default_indicator
    default_indicator="STD"

#calculate indicators

def calc_rsi(new_window,df_converted,ax1,fig_graph, symbol_to_name):
   
    window_length = 14
    delta = df_converted.diff()
    delta = delta[1:] 
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up1 = up.ewm(span=window_length).mean()
    roll_down1 = down.abs().ewm(span=window_length).mean()
    rs = roll_up1 / roll_down1
    rsi = 100.0 - (100.0 / (1.0 + rs))
    rsi.plot(kind='line', label="RSI", ax=ax1, color='r', fontsize=10, legend=True)
    df_converted.plot(kind='line', label="Stock Price", ax=ax1,secondary_y=True ,color='b', fontsize=10, legend=True)
    ax1.set_title('Price over Time for {} in {}'.format(symbol_to_name[current_stock],wanted_currency))
    ax2 = ax1.twinx()
    ax1.set_ylabel('RSI', color='r')
    ax2.set_ylabel('Price in {}'.format(wanted_currency),color='b')
    ax2.plot(df_converted, color='b')
    

def calc_mavg(new_window,df_converted,ax1,fig_graph,symbol_to_name):
    
    mavg = df_converted.rolling(window=20).mean()
    mavg.plot(kind='line', label="MAVG", ax=ax1, color='g', fontsize=10, legend=True)
    df_converted.plot(kind='line', label="Stock Price", ax=ax1,secondary_y=True ,color='b', fontsize=10, legend=True)
    ax1.set_title('Price over Time for {} in {}'.format(symbol_to_name[current_stock],wanted_currency))
    ax2 = ax1.twinx()
    ax1.set_ylabel('MAVG', color='g')
    ax2.set_ylabel('Price in {}'.format(wanted_currency),color='b')
    ax2.plot(df_converted, color='b')
    
   
def calc_bollinger(new_window,df_converted,ax1,fig_graph,date_frame,symbol_to_name):
    set_window(date_frame)
    df_bollinger=pd.DataFrame()
    df_bollinger['MA'] = df_converted.rolling(window=wind).mean()
    df_bollinger['STD'] = df_converted.rolling(window=wind).std() 
    df_bollinger['MA'] = df_converted.rolling(window=wind).mean()
    df_bollinger['STD'] = df_converted.rolling(window=wind).std() 
    
    df_bollinger['Upper'] = df_bollinger['MA'] + (df_bollinger['STD'] * 2)
    df_bollinger['Lower'] = df_bollinger['MA'] - (df_bollinger['STD'] * 2)

    df_bollinger['Upper'].plot(kind='line', ax=ax1 ,fontsize=10, color='g',label='Upper', legend=True)
    df_bollinger['Lower'].plot(kind='line', ax=ax1,fontsize=10, color='r',label='Lower', legend=True)
    df_bollinger['MA'].plot(kind='line', ax=ax1,fontsize=10, color='#FFFF00',label='MAVG', legend=True)
    df_converted.plot(kind='line', label="Stock Price", ax=ax1,secondary_y=True ,color='b', fontsize=10, legend=True)
    ax1.set_title('Price over Time for {} in {}'.format(symbol_to_name[current_stock],wanted_currency))
    ax2 = ax1.twinx()
    ax1.set_ylabel('Bollinger Bands', color='g')
    ax2.set_ylabel('Price in {}'.format(wanted_currency),color='b')
    ax2.plot(df_converted, color='b')
    plt.show()


def calc_std(new_window,df_converted,ax1,fig_graph,date_frame,symbol_to_name):
    set_window(date_frame)
    df_std = df_converted.rolling(window=wind).std() 
    df_std.plot(kind='line', ax=ax1 ,fontsize=10, label="STD", legend=True, color='g')
    df_converted.plot(kind='line', label="Stock Price", ax=ax1,secondary_y=True ,color='b', fontsize=10, legend=True)
    ax1.set_title('Price over Time for {} in {}'.format(symbol_to_name[current_stock],wanted_currency))
    ax2 = ax1.twinx()
    ax1.set_ylabel('STD', color='g')
    ax2.set_ylabel('Price in {}'.format(wanted_currency),color='b')
    ax2.plot(df_converted, color='b')

#updates text according to selected options  
  
def update_text():
    global current_stock
    global wanted_currency
    global date_frame
    global current_label
    current_label.delete(0.0, 4.0)
    current_label.insert(tk.END, "Selected stock:{}\n Currency:{} \n Time selected for {}".format(current_stock,wanted_currency,date_frame))
    current_label.tag_configure("center", justify='center')
    current_label.insert("1.0", "")
    current_label.tag_add("center", "1.0", "end")    

#generate graph window

def generateGraph(symbol_to_name):

    new_window = tk.Toplevel(root2) 
    new_window.title("GraphPage") 
    new_window.geometry('1200x730')

    fig_graph = plt.Figure(figsize=(12,7))
    ax1 = fig_graph.add_subplot(111)
    line = FigureCanvasTkAgg(fig_graph, new_window)
    line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    stock_data = yf.download(current_stock, period=date_frame)
    df = pd.DataFrame(data=stock_data, columns=['Close'])
    df_converted= df.apply(lambda x: currency_converter(x,wanted_currency), axis=1)

    if default_indicator=="RSI":
        calc_rsi(new_window,df_converted,ax1,fig_graph, symbol_to_name)
    elif default_indicator=="MAVG":
        calc_mavg(new_window,df_converted,ax1,fig_graph,symbol_to_name)
    elif default_indicator=="Bollinger Bands":
        calc_bollinger(new_window,df_converted,ax1,fig_graph, date_frame,symbol_to_name)
    elif default_indicator=="STD":
        calc_std(new_window,df_converted, ax1, fig_graph, date_frame,symbol_to_name)
    else:
        df_converted.plot(kind='line', label="Stock Price", ax=ax1, color='b', fontsize=10, legend=True)
        ax1.set_title('Price over Time for {} in {}'.format(symbol_to_name[current_stock],wanted_currency))
    mpl.cursor(ax1,hover=True)

#calculate capm
   
def daily_return(df):
    df_daily_return = df.copy()
    for i in df.columns[1:]:
        for j in range(1, len(df)):
            df_daily_return[i][j] = ((df[i][j]- df[i][j-1])/df[i][j-1]) * 100
        df_daily_return[i][0] = 0
    return df_daily_return

def calc_capm(checkbox_values, index_to_symbol, date_frame, newCapm, text_capm, text_camp_portfolio, symbol_to_name):
    
    checked_options = []
    for i in range(len(checkbox_values)):
        if checkbox_values[i].get() == True:
            checked_options.append(index_to_symbol[i])
    checked_options.append('^GSPC')
 
    size=len(checked_options)
    stock_data = yf.download(checked_options, period=date_frame)
    df= pd.DataFrame(data=stock_data.iloc[:,size:2*size])
    stocks_return = daily_return(df)
    
    beta = {}
    alpha = {}
    for i in stocks_return.iloc[:,:-1]:
        b, a = np.polyfit(stocks_return.iloc[:,-1], stocks_return[i], 1)
        beta[i] = b    
        alpha[i] = a  
    
    ER = {}
    rf = 0 
   
    rm = stocks_return.iloc[:,-1].mean() * 252
    print(checked_options)
    first_label_text = []
    for i in checked_options[:-2]:
        ER[i] = rf + (beta[('Close', i)] * (rm - rf))
        first_label_text.append('{} ({})  |  '.format(symbol_to_name[i], round(ER[i], 2)))
    
    i = checked_options[-2]
    print(i)
    ER[i] = rf + (beta[('Close', i)] * (rm - rf))
    first_label_text.append('{} ({})'.format(symbol_to_name[i], round(ER[i], 2)))

    if len(first_label_text) > 4:
        first_label_text.insert(len(first_label_text) // 2, '\n')
    portfolio_weights = 1 / (size - 1) * np.ones(size-1) 
    ER_portfolio = sum(list(ER.values()) * portfolio_weights)
    
    text_capm.config(text=''.join(first_label_text))
    text_camp_portfolio.config(text='Expected return based on CAPM portfolio is {}'.format(round(ER_portfolio, 2)))
    text_capm.grid(row=26, column=2, columnspan=10, rowspan=2)
    text_camp_portfolio.grid(row=30, column=2, columnspan=10, rowspan=2)

#generate capm window
    
def openCapm():

    newCapm = tk.Toplevel(bg="#F0F0F0") 
    newCapm.title("Capital Asset Pricing Modell") 
    newCapm.geometry('600x500')

    upward_label=tk.Label(newCapm,text="Choose stocks to calculate expected return for:",fg="Black",font = "Calibri",pady=3,bg="#F0F0F0", width=40)
    upward_label.grid(row=1, column=1, columnspan=5,sticky="NESW")

    checkbox_values = [tk.BooleanVar() for _ in range(10)]
    
    Check1 = tk.Checkbutton(newCapm, text = "ING", var = checkbox_values[0], onvalue = 1, offvalue = 0, height = 2, width = 18) 

    Check2 = tk.Checkbutton(newCapm, text = "Visa  ", var = checkbox_values[1], onvalue = 1, offvalue = 0, height = 2, width = 19)

    Check3 = tk.Checkbutton(newCapm, text = "eBay  ", var = checkbox_values[2], onvalue = 1, offvalue = 0, height = 2, width = 19) 

    Check5 = tk.Checkbutton(newCapm, text = "Toyota", var = checkbox_values[4], onvalue = 1, offvalue = 0, height = 2, width = 20)

    Check6 = tk.Checkbutton(newCapm, text = "Ryanair", var = checkbox_values[5], onvalue = 1, offvalue = 0, height = 2, width = 13)

    Check8 = tk.Checkbutton(newCapm, text = "Deutsche Bank   ", var = checkbox_values[7], onvalue = 1, offvalue = 0, height = 2, width = 20)

    Check9 = tk.Checkbutton(newCapm, text = "Domino's Pizza  ", var = checkbox_values[8], onvalue = 1, offvalue = 0, height = 2, width = 20)

    Check10 = tk.Checkbutton(newCapm, text = "Intercontinental", var = checkbox_values[9], onvalue = 1, offvalue = 0, height = 2, width = 20)

    text_capm= tk.Label(newCapm,fg="Black", bg="#F0F0F0",pady=30)
    text_camp_portfolio=tk.Label(newCapm,fg="Black",bg="#F0F0F0", pady=30)

    buttonCapm=tk.Button(newCapm,text ='Calculate CAPM', bg='#AED6F1',height=2, width=14, command= lambda: calc_capm(checkbox_values, index_to_symbol, date_frame, newCapm, text_capm, text_camp_portfolio, symbol_to_name))
    buttonCapm.grid(row=14, column=3, columnspan=2)    

    Check1.grid(row=4, column=1,columnspan=2,sticky='W') 
    Check2.grid(row=5,column=1,columnspan=2, sticky='W') 
    Check3.grid(row=6,column=1,columnspan=2, sticky='W') 
    Check5.grid(row=7,column=1,columnspan=2, sticky='W') 
    Check6.grid(row=4,column=5,columnspan=2,sticky='W') 
    Check8.grid(row=5,column=5,columnspan=2,sticky='W') 
    Check9.grid(row=6,column=5,columnspan=2,sticky='W')
    Check10.grid(row=7,column=5,columnspan=2,sticky='W')

#open menu page

def open_new_window(symbol_to_name): 
    global current_label
    new_window = tk.Toplevel(root2,bg="white") 
    new_window.title("MenuPage") 
    new_window.geometry('600x500')
    
   
    menubar = tk.Menu(new_window)
    stockmenu=tk.Menu(menubar, tearoff=0)

    stockmenu.add_command(label ="eBay", command=set_ebay)
    stockmenu.add_command(label ="Domino's Pizza", command=set_dominos)
    stockmenu.add_command(label ="Intercontinental Hotels", command=set_intercont)
    stockmenu.add_command(label ="Visa", command=set_visa)
    stockmenu.add_command(label ="Deutsche Bank", command=set_db)
    stockmenu.add_command(label ="Deutsche Lufthansa", command=set_lufthansa)
    stockmenu.add_command(label ="Daimler", command=set_daimler)
    stockmenu.add_command(label ="Ryanair", command=set_ryanair)
    stockmenu.add_command(label ="ING", command=set_ing)
    stockmenu.add_command(label ="Toyota Motors", command=set_toyota)
    
    menubar.add_cascade(label="Stock", menu=stockmenu)

    dataframe= tk.Menu(menubar, tearoff=0)
    dataframe.add_command(label="1 day", command=set_1days)
    dataframe.add_command(label="5 days", command=set_5days)
    dataframe.add_command(label="1 month", command=set_1months)
    dataframe.add_command(label="3 months", command=set_3months)
    dataframe.add_command(label="6 months", command=set_6months)
    dataframe.add_command(label="1 year", command=set_1year)
    menubar.add_cascade(label="Time Frame", menu=dataframe)

    currency=tk.Menu(menubar, tearoff=0)
    currency.add_command(label="USD", command=set_usd)
    currency.add_command(label="EUR", command=set_eur)
    currency.add_command(label="GBP", command=set_gbp)
    currency.add_command(label="CHF", command=set_chf)
    currency.add_command(label="RON", command=set_ron)
    menubar.add_cascade(label="Currency", menu=currency)

    indicator=tk.Menu(menubar, tearoff=0)
    indicator.add_command(label="RSI", command=set_rsi)
    indicator.add_command(label="Standard Deviation", command=set_std)
    indicator.add_command(label="MAVG", command=set_mavg)
    indicator.add_command(label="Bollinger Bands", command=set_bollinger)
    menubar.add_cascade(label="Indicator", menu=indicator)

    capm=tk.Menu(menubar, tearoff=0)
    capm.add_command(label="Go to CAPM", command=openCapm)
    menubar.add_cascade(label="CAPM", menu=capm)

    buttonGenerate = tk.Button(new_window, text ='Generate Graph', bg='#AED6F1', command=lambda: generateGraph(symbol_to_name))
    buttonGenerate.place(relx=0.4, rely=0.6, relwidth=0.17, relheight=0.08)

    text_frame = tk.Frame(new_window, bg='white', bd=0)
    text_frame.place(relx=0.47, rely= 0.2, relwidth=0.4, relheight=0.4, anchor='n')


    label_selected = tk.Text(text_frame, bg='white', bd=0, wrap='word', font="Calibri")
    label_selected.pack()
    label_selected.insert(tk.END, "Selected stock:{}\n Currency:{} \nSelected time for {}".format(current_stock,wanted_currency,date_frame))  
    label_selected.tag_configure("center", justify='center')
    label_selected.insert("1.0", "")
    label_selected.tag_add("center", "1.0", "end")
    current_label = label_selected
    new_window.config(menu=menubar)
    new_window.mainloop()

def closePage():
    root.withdraw()

def closeOpen(symbol_to_name):
    closePage()
    open_new_window(symbol_to_name)

#define start page

root.geometry('1200x730')
root.title('DataVizz')
root.resizable(False,False)
root.iconbitmap(default="logo2.ico")

canvas = tk.Canvas(root, width=1200, height=800, bd=-2, highlightthickness=0, relief='ridge')
canvas.place(relwidth=1, relheight=1)

background_image= tk.PhotoImage(file='newimg.png')
background_label= tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

lower_frame = tk.Frame(root, bg='blue', bd=0)
lower_frame.place(relx=0.5, rely= 0.65, relwidth=0.21, relheight=0.2, anchor='n')

labelFont = font.Font(family='Calibri', size=15)
label = tk.Text(lower_frame, bg='white', bd=0, wrap='word')
label['font']=labelFont
label.pack()
label.insert(tk.END, "This is a stock visualisation app which offers you details about a limited amount of stocks")  
label.tag_configure("center", justify='center')
label.insert("1.0", "")
label.tag_add("center", "1.0", "end")
label.config(state='disabled')
buttonFont = font.Font(family='Calibri', size=10)
button = tk.Button(lower_frame, text ='Get Started', bg='#AED6F1',command =lambda: closeOpen(symbol_to_name))
button['font']=buttonFont
button.place(relx=0.35, rely=0.7 ,relwidth=0.3 ,relheight=0.25, )

root2.withdraw()

root.mainloop()
