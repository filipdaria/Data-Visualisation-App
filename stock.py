import tkinter as tk 
import tkinter.font as font
import yfinance as yf
import pandas as pd
import datetime as dt
import mplcursors as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from pandas import DataFrame
import datetime
import dateutil.relativedelta
from currency_converter import CurrencyConverter

# today = datetime.date.today()
# delta = dateutil.relativedelta.relativedelta(months=1)
# one_month_ago = today - delta
root = tk.Tk()
root2=tk.Tk()

date_frame="1y"
current_stock="DB"
default_currency="USD"
wanted_currency="EUR"
c = CurrencyConverter()
default_indicator=None
wind=None
#set current date 

def set_1days():
    global date_frame
    date_frame="1d"

def set_5days():
    global date_frame
    date_frame="5d"

def set_1months():
    global date_frame
    date_frame="1mo"

def set_3months():
    global date_frame
    date_frame="3mo"

def set_6months():
    global date_frame
    date_frame="6mo"

def set_1year():
    global date_frame
    date_frame="1y"

#set current state for stocks
def set_Ebay():
    global current_stock
    current_stock="EBAY"
def set_Dominos():
    global current_stock
    current_stock="DPZ"
def set_Intercont():
    global current_stock
    current_stock="IHG"
def set_Visa():
    global current_stock
    current_stock="V"
def set_DB():
    global current_stock
    current_stock="DB"
def set_Lufthansa():
    global current_stock
    current_stock="LHA.DE"
def set_Daimler():
    global current_stock
    current_stock="DAI.DE"
def set_Ryanair():
    global current_stock
    current_stock="RYAAY"
def set_Ing():
    global current_stock
    current_stock="ING"
def set_Toyota():
    global current_stock
    current_stock="TM"
def set_Usd():
    global wanted_currency
    wanted_currency="USD"
def set_Eur():
    global wanted_currency
    wanted_currency="EUR"
def set_Gbp():
    global wanted_currency
    wanted_currency="GBP"
def set_Chf():
    global wanted_currency
    wanted_currency="CHF"
def set_Ron():
    global wanted_currency
    wanted_currency="RON"

def currency_convertor(df_converted,new_currency):
     amount = df_converted["Close"]
     curr="USD"
     new_curr = c.convert(amount,curr,new_currency)
     return new_curr

def set_Rsi():
    global default_indicator
    default_indicator="RSI"
def calc_Rsi(newWindow,df_converted,ax2,figure2):
   
    # figure2 = plt.Figure(figsize=(12,7))
    # ax2 = figure2.add_subplot(111)
    # line2 = FigureCanvasTkAgg(figure2, newWindow)
    # line2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    # stock_data = yf.download(current_stock, start=date_frame["start"], end=date_frame["end"])
    # df_converted = pd.DataFrame(data=stock_data, columns=["Close","Date"])
    # df_converted=pd.DataFrame()
    # df_converted= df_converted.apply(lambda x: currency_convertor(x,wanted_currency), axis=1)
    
    window_length = 14
    delta = df_converted.diff()
    delta = delta[1:] 
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up1 = up.ewm(span=window_length).mean()
    roll_down1 = down.abs().ewm(span=window_length).mean()
    RS = roll_up1 / roll_down1
    RSI = 100.0 - (100.0 / (1.0 + RS))
    RSI.plot(kind='line', label="RSI", ax=ax2, color='b', fontsize=10)
    df_converted.plot(kind='line', label="Stock Price", ax=ax2, color='r', fontsize=10)
    figure2.legend(['RSI via EWMA',"Stock Price"])
    # ax2.set_title('Price over Time for {} in {}'.format(current_stock,wanted_currency))
    # mpl.cursor(ax2,hover=True)
   
  
def set_Mavg():
    global default_indicator
    default_indicator="MAVG"

def calc_Mavg(newWindow,df_converted,ax2,figure2):
    
    mavg = df_converted.rolling(window=20).mean()
    mavg.plot(kind='line', label="MAVG", ax=ax2, color='g', fontsize=10, legend=True)
    df_converted.plot(kind='line', label="Stock Price", ax=ax2, color='r', fontsize=10)
    figure2.legend(['MAVG',"Stock Price"])

def set_bollinger():
    global default_indicator
    default_indicator="Bollinger Bands"


def set_window(date_frame):
    global wind
    if (date_frame=="1mo" or date_frame=="3mo"):
        wind=5
    elif (date_frame=="1y" or date_frame=="6mo"):
        wind=20
    
def calc_bollingerbands(newWindow,df_converted,ax2,figure2,date_frame):
    set_window(date_frame)
    df_bollinger=pd.DataFrame()
    df_bollinger['MA'] = df_converted.rolling(window=wind).mean()
    df_bollinger['STD'] = df_converted.rolling(window=wind).std() 
    df_bollinger['MA'] = df_converted.rolling(window=wind).mean()
    df_bollinger['STD'] = df_converted.rolling(window=wind).std() 
    

    # df_bollinger['MA'] = df_converted.rolling(window=wind).mean()
    # df_bollinger['STD'] = df_converted.rolling(window=wind).std() 
    df_bollinger['Upper'] = df_bollinger['MA'] + (df_bollinger['STD'] * 2)
    df_bollinger['Lower'] = df_bollinger['MA'] - (df_bollinger['STD'] * 2)

    df_bollinger['Upper'].plot(kind='line', ax=ax2 ,fontsize=10)
    df_bollinger['Lower'].plot(kind='line', ax=ax2,fontsize=10)
    df_bollinger['MA'].plot(kind='line', ax=ax2,fontsize=10)
    df_converted.plot(kind='line', label="Stock Price", ax=ax2, color='r', fontsize=10)
    figure2.legend(['Upper','Lower','Moving Average','Stock Price'])
    plt.show()

def set_Rsi_Mavg():
    global default_indicator
    default_indicator="RSI MAVG"

def calc_Rsi_Mavg(newWindow,df_converted,ax2,figure2):
    calc_Rsi(newWindow,df_converted,ax2,figure2)
    calc_Mavg(newWindow,df_converted,ax2,figure2)

def set_Std():
    global default_indicator
    default_indicator="STD"

def calc_Std(newWindow,df_converted,ax2,figure2,date_frame):
    set_window(date_frame)
    df_std = df_converted.rolling(window=wind).std() 
    df_std.plot(kind='line', ax=ax2 ,fontsize=10, label="STD")
    df_converted.plot(kind='line', label="Stock Price", ax=ax2, color='r', fontsize=10)
    figure2.legend(['STD', 'Stock Price'])
    plt.show()
  
def generateGraph():

    newWindow = tk.Toplevel(root2) 
    newWindow.title("GraphPage") 
    newWindow.geometry('1200x730')

    figure2 = plt.Figure(figsize=(12,7))
    ax2 = figure2.add_subplot(111)
    line2 = FigureCanvasTkAgg(figure2, newWindow)
    line2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    stock_data = yf.download(current_stock, period=date_frame)
    df = pd.DataFrame(data=stock_data, columns=['Close'])
    df_converted= df.apply(lambda x: currency_convertor(x,wanted_currency), axis=1)

    if default_indicator=="RSI":
        calc_Rsi(newWindow,df_converted,ax2,figure2)
    elif default_indicator=="MAVG":
        calc_Mavg(newWindow,df_converted,ax2,figure2)
    elif default_indicator=="Bollinger Bands":
        calc_bollingerbands(newWindow,df_converted,ax2,figure2, date_frame)
        
    elif default_indicator=="RSI MAVG":
        calc_Rsi_Mavg(newWindow,df_converted,ax2,figure2)
    elif default_indicator=="STD":
        calc_Std(newWindow,df_converted, ax2, figure2, date_frame)
    else:
        df_converted.plot(kind='line', label="{} Stock Price".format(current_stock), ax=ax2, color='b', fontsize=10, legend=True)
        ax2.set_title('Price over Time for {} in {}'.format(current_stock,wanted_currency))
    mpl.cursor(ax2,hover=True)

    # newWindow = tk.Toplevel(root2) 
    # newWindow.title("GraphPage") 
    # newWindow.geometry('1200x730')
    # figure2 = plt.Figure(figsize=(12,7))
    # ax2 = figure2.add_subplot(111)
    # line2 = FigureCanvasTkAgg(figure2, newWindow)
    # line2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    # stock_data = yf.download(current_stock, start=date_frame["start"], end=date_frame["end"])
    # df_converted = pd.DataFrame(data=stock_data, columns=["Close","Date"])
    # df_converted=pd.DataFrame()
    # df_converted= df_converted.apply(lambda x: currency_convertor(x,wanted_currency), axis=1)
   
    #     RSI1.plot()
    # plt.legend(['RSI via EWMA',"Stock Price"])
    # df_converted.plot(kind='line', legend=True, ax=ax2, color='r', fontsize=10)
    # ax2.set_title('Price over Time for {} in {}'.format(current_stock,wanted_currency))
    # mpl.cursor(ax2,hover=True)

def get_value(c):
    print(c.get())
    
def openCapm():

    newCapm = tk.Toplevel(bg="#F0F0F0") 
    newCapm.title("Capital Asset Pricing Modell") 
    newCapm.geometry('600x500')

    upward_label=tk.Label(newCapm,text="Choose stocks to calculate expected return for:",fg="Black",font = "Calibri",pady=3,bg="#F0F0F0", width=40)
    upward_label.grid(row=1, column=1, columnspan=5,sticky="NESW")
    
    Ckb1 = tk.IntVar() 
    Ckb2 = tk.IntVar() 
    Ckb3 = tk.IntVar() 
    Ckb4 = tk.IntVar() 
    Ckb5 = tk.IntVar() 
    Ckb6 = tk.IntVar() 
    Ckb7 = tk.IntVar() 
    Ckb8 = tk.IntVar() 
    Ckb9 = tk.IntVar() 
    Ckb10 = tk.IntVar() 
    
    Check1 = tk.Checkbutton(newCapm, text = "ING", variable = Ckb1, onvalue = 1, offvalue = 0, height = 2, width = 20, command=get_value(Ckb1)) 

    Check2 = tk.Checkbutton(newCapm, text = "Visa", variable = Ckb2, onvalue = 1, offvalue = 0, height = 2, width = 20,command=get_value(Ckb2)) 

    Check3 = tk.Checkbutton(newCapm, text = "eBay", variable = Ckb3, onvalue = 1, offvalue = 0, height = 2, width = 20,command=get_value(Ckb3)) 

    Check4 = tk.Checkbutton(newCapm, text = "Daimler", variable = Ckb4, onvalue = 1, offvalue = 0, height = 2, width = 20,command=get_value(Ckb4)) 

    Check5 = tk.Checkbutton(newCapm, text = "Toyota", variable = Ckb5, onvalue = 1, offvalue = 0, height = 2, width = 20,command=get_value(Ckb5)) 

    Check6 = tk.Checkbutton(newCapm, text = "Ryanair", variable = Ckb6, onvalue = 1, offvalue = 0, height = 2, width = 20,command=get_value(Ckb6)) 

    Check7 = tk.Checkbutton(newCapm, text = "Lufthansa", variable = Ckb7, onvalue = 1, offvalue = 0, height = 2, width = 20,command=get_value(Ckb7)) 

    Check8 = tk.Checkbutton(newCapm, text = "Deutsche Bank ", variable = Ckb8, onvalue = 1, offvalue = 0, height = 2, width = 20,command=get_value(Ckb8)) 

    Check9 = tk.Checkbutton(newCapm, text = "Domino's Pizza", variable = Ckb9, onvalue = 1, offvalue = 0, height = 2, width = 20,command=get_value(Ckb9)) 

    Check10 = tk.Checkbutton(newCapm, text = "InterContinental", variable = Ckb10, onvalue = 1, offvalue = 0, height = 2, width = 20,command=get_value(Ckb10)) 

    buttonCapm=tk.Button(newCapm,text ='Calculate CAPM', bg='#AED6F1',height=2, width=14)
    buttonCapm.grid(row=14, column=3, columnspan=2)    

    Check1.grid(row=4, column=1,columnspan=2) 
    Check2.grid(row=5,column=1,columnspan=2) 
    Check3.grid(row=6,column=1,columnspan=2) 
    Check4.grid(row=7,column=1,columnspan=2) 
    Check5.grid(row=8,column=1,columnspan=2) 
    Check6.grid(row=4,column=5,columnspan=2) 
    Check7.grid(row=5,column=5,columnspan=2) 
    Check8.grid(row=6,column=5,columnspan=2) 
    Check9.grid(row=7,column=5,columnspan=2)
    Check10.grid(row=8,column=5,columnspan=2)



def openNewWindow(): 
      
    newWindow = tk.Toplevel(root2,bg="white") 
    newWindow.title("MenuPage") 
    newWindow.geometry('600x500')
    
    #symbol=[EBAY,DPZ,IHG,V,DB,LHA.DE,DAI.DE,RYAAY, ING,TM]
    menubar = tk.Menu(newWindow)
   
    stockmenu=tk.Menu(menubar, tearoff=0)

    # stock=["eBay","Domino's Pizza","InterContinental Hotels","Visa","Deutsche Bank","Deutsche Lufthansa AG","Daimler AG ","Ryanair Holdings","ING Groep","Toyota Motor Corporation"]
    # show_stock=[stockmenu.add_command(label="{}".format(stock[i])) for i in range(len(stock))]
    stockmenu.add_command(label ="eBay", command=set_Ebay)
    stockmenu.add_command(label ="Domino's Pizza", command=set_Dominos)
    stockmenu.add_command(label ="InterContinental Hotels", command=set_Intercont)
    stockmenu.add_command(label ="Visa", command=set_Visa)
    stockmenu.add_command(label ="Deutsche Bank", command=set_DB)
    stockmenu.add_command(label ="Deutsche Lufthansa", command=set_Lufthansa)
    stockmenu.add_command(label ="Daimler", command=set_Daimler)
    stockmenu.add_command(label ="Ryanair", command=set_Ryanair)
    stockmenu.add_command(label ="ING", command=set_Ing)
    stockmenu.add_command(label ="Toyota Motors", command=set_Toyota)
    
    menubar.add_cascade(label="Stock", menu=stockmenu)

    dataframe= tk.Menu(menubar, tearoff=0)
    # time=['1 day','1 week','1 month','3 months','6 months','1 year']
    # show_time=[dataframe.add_command(label="{}".format(time[j])) for j in range(len(time))]
    dataframe.add_command(label="1 day", command=set_1days)
    dataframe.add_command(label="5 days", command=set_5days)
    dataframe.add_command(label="1 month", command=set_1months)
    dataframe.add_command(label="3 months", command=set_3months)
    dataframe.add_command(label="6 months", command=set_6months)
    dataframe.add_command(label="1 year", command=set_1year)
    menubar.add_cascade(label="Time Frame", menu=dataframe)

    currency=tk.Menu(menubar, tearoff=0)
    currency.add_command(label="USD", command=set_Usd)
    currency.add_command(label="EUR", command=set_Eur)
    currency.add_command(label="GBP", command=set_Gbp)
    currency.add_command(label="CHF", command=set_Chf)
    currency.add_command(label="RON", command=set_Ron)
    menubar.add_cascade(label="Currency", menu=currency)

    indicator=tk.Menu(menubar, tearoff=0)
    indicator.add_command(label="RSI", command=set_Rsi)
    indicator.add_command(label="Standard Deviation", command=set_Std)
    indicator.add_command(label="MAVG", command=set_Mavg)
    indicator.add_command(label="Bollinger Bands", command=set_bollinger)
    indicator.add_command(label="RSI-MAVG", command=set_Rsi_Mavg)
    menubar.add_cascade(label="Indicator", menu=indicator)

    forecast =tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Forecast", menu=forecast)

    capm=tk.Menu(menubar, tearoff=0)
    capm.add_command(label="Go to CAPM", command=openCapm)
    menubar.add_cascade(label="CAPM", menu=capm)

    clear=tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Clear", menu=clear)

    buttonGenerate = tk.Button(newWindow, text ='Generate Graph', bg='#AED6F1', command=generateGraph)
    buttonGenerate.place(relx=0.4, rely=0.6, relwidth=0.17, relheight=0.08)

    text_frame = tk.Frame(newWindow, bg='white', bd=0)
    text_frame.place(relx=0.47, rely= 0.2, relwidth=0.4, relheight=0.4, anchor='n')
    #labelFont = font.Font(family='Calibri', size=15)
    label = tk.Text(text_frame, bg='white', bd=0, wrap='word', font="Calibri")
    #label['font']=labelFont

    label.pack()
    label.insert(tk.END, "Selected stock:{}\n Currency:{} \nSelected time for {}".format(current_stock,wanted_currency,date_frame))  
    label.tag_configure("center", justify='center')
    label.insert("1.0", "")
    label.tag_add("center", "1.0", "end")

    newWindow.config(menu=menubar)
    newWindow.mainloop()

def closePage():
    root.withdraw()

def closeOpen():
    closePage()
    openNewWindow()


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

buttonFont = font.Font(family='Calibri', size=10)
button = tk.Button(lower_frame, text ='Get Started', bg='#AED6F1',command =closeOpen)
button['font']=buttonFont
button.place(relx=0.35, rely=0.7 ,relwidth=0.3 ,relheight=0.25, )


root2.withdraw()
# bg='#ffff99' colour background

root.mainloop()
