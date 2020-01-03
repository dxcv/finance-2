import tkinter as tk
from Quandl import *


HEIGHT = 800
WIDTH = 600

def clear(widget):
    if widget == 'Both':
        try:
            label.destroy()
        except (NameError, AttributeError):
            pass
        try:
            label_opv.destroy()
        except (NameError, AttributeError):
            pass

    elif widget == 'label':
        try:
            label.destroy()
        except (NameError, AttributeError):
            pass

    elif widget == 'label_opv':
        try:
            label_opv.destroy()
        except (NameError, AttributeError):
            pass


def compute_SMA(select):
    clear('Both')
    TxtBox.delete('1.0', tk.END)
    TxtBox.insert(tk.END, SMA(select))


def compute_MPT(port):
    clear('Both')
    TxtBox.delete('1.0', tk.END)
    TxtBox.insert(tk.END, MPT(list(set(port))))


def compute_OPV():

    clear('label')
    TxtBox.delete('1.0', tk.END)

    global label_opv

    label_opv = tk.Label(lower_frame, anchor='nw', justify='left')
    label_opv.place(relwidth=1, relheight=1)
    label_P0 = tk.Label(label_opv, text='\n1. Initial Price of an underlying product(example 100):')
    label_P0.place(rely=0.02)
    entry_P0 = tk.Entry(label_opv, font=40)
    entry_P0.place(relx=0.04, rely=0.08, relwidth=0.3, relheight=0.04)
    label_PT = tk.Label(label_opv, text='2. Strike Price(example 120):')
    label_PT.place(rely=0.15)
    entry_PT = tk.Entry(label_opv, font=40)
    entry_PT.place(relx=0.04, rely=0.18, relwidth=0.3, relheight=0.04)
    label_Rft = tk.Label(label_opv, text='3. Risk Free Interest Rate(example 0.05):')
    label_Rft.place(rely=0.25)
    entry_Rft = tk.Entry(label_opv, font=40)
    entry_Rft.place(relx=0.04, rely=0.28, relwidth=0.3, relheight=0.04)
    label_T = tk.Label(label_opv, text='4. Time Horizon in years(example 2):')
    label_T.place(rely=0.35)
    entry_T = tk.Entry(label_opv, font=40)
    entry_T.place(relx=0.04, rely=0.38, relwidth=0.3, relheight=0.04)
    label_option = tk.Label(label_opv, text='5. Call[Yes]/Put[No](example Yes):')
    label_option.place(rely=0.45)

    option = ['Yes', 'No']
    entry_option = tk.StringVar()
    entry_option.set(option[0])

    drop = tk.OptionMenu(label_opv, entry_option, *option)
    drop.place(relx=0.04, rely=0.48, relwidth=0.3, relheight=0.04)

    def OPV_res(S0, K, r, T, option_type):

        try:
            if float(S0) < 0:
                error_msg = tk.Label(label_opv, text='Error: 1. Initial Price needs to be a positive number!')
                error_msg.place(rely= 2/3)
                return
        except (ValueError):
            error_msg = tk.Label(label_opv, text='Error: 1. Initial Price needs to be a positive number!')
            error_msg.place(rely= 2/3)
            return

        try:
            if float(K) < 0:
                error_msg = tk.Label(label_opv, text='Error: 2. Strike Price needs to be a positive number!')
                error_msg.place(rely= 2/3)
                return
        except (ValueError):
            error_msg = tk.Label(label_opv, text='Error: 2. Strike Price needs to be a positive number!')
            error_msg.place(rely= 2/3)
            return

        try:
            if float(r) < 0:
                error_msg = tk.Label(label_opv, text='Error: 3. Risk Free Interest Rate needs to be a positive number!')
                error_msg.place(rely= 2/3)
                return
        except (ValueError):
            error_msg = tk.Label(label_opv, text='Error: 3. Risk Free Interest Rate needs to be a positive number!')
            error_msg.place(rely= 2/3)
            return

        try:
            if float(T) < 0:
                error_msg = tk.Label(label_opv, text='Error: 4. Time Horizon needs to be a positive number!')
                error_msg.place(rely= 2/3)
                return
        except (ValueError):
            error_msg = tk.Label(label_opv, text='Error: 4. Time Horizon needs to be a positive number!')
            error_msg.place(rely= 2/3)
            return


        label_opv.destroy()
        Title = 'Option Valuation with the following parameters'
        if option_type == 'Yes':
            option_display = 'Call option'
        else:
            option_display = 'Put option'


        TxtBox.insert(tk.END, Title + '\n'*2 + 'Initial Price: ' + S0 + '\n' +
                      'Strike Price: ' + K + '\n' + 'Risk Free Interest Rate: ' +
                      r + '\n' + 'Time Horizon: ' + T + '\n' + 'Option Type: ' +
                      option_display + '\n'*2)
        TxtBox.insert(tk.END, 'Stochastic differential equation: ' +
                      'dS(t) = rS(t)dt + σS(t)dZ(t)' + '\n' +
                      'Distribution method: Standard Normal Distribution' + '\n'*2)
        TxtBox.insert(tk.END, str(OPV(S0, K, r, T, option_type)))


    button_gen = tk.Button(label_opv, text='Perform Valuation', font=40,
                           command=lambda: OPV_res(S0=entry_P0.get(), K=entry_PT.get(),
                                               r=entry_Rft.get(), T=entry_T.get(),
                                               option_type=entry_option.get()))
    button_gen.place(relx=0.04, rely=0.55, relwidth=1/3, relheight=0.05)


def IMF_Data():
    clear('label_opv')
    TxtBox.delete('1.0', tk.END)

    global label
    label = tk.Label(lower_frame, anchor='nw', justify='left')
    label.place(relwidth=1, relheight=1)


    imf_data = tk.StringVar()
    imf_data.set('Select Country')

    imf_data_drop = tk.OptionMenu(label, imf_data, *ISO3)
    imf_data_drop.config(font=('helvetica'))
    imf_data_drop.pack()

    raw = []
    def add_country():
        raw.append(imf_data.get())

    def clear_country():
        raw.clear()


    country_button = tk.Button(label, text='Add Country', command=add_country).place(relx=0.5, rely=0.06, anchor='e')
    country_clear = tk.Button(label, text='Clear Country', command=clear_country()).place(relx=0.5, rely=0.06, anchor='w')

    def economic_indicator(raw, data_type):
        IMF_Release(raw, data_type)

    label_populatiom = tk.Label(label, text='For census purposes, the total population of the country consists of all\n'
                                                  'persons falling within the scope of the census. In the broadest sense, the\n'
                                                  'total may comprise either all usual residents of the country or all persons\n'
                                                  'present in the country at the time of the census.').place(relx=0, rely=0.12, relwidth=1, anchor='nw')

    country_population = tk.Button(label, text='Display Population', command=lambda: economic_indicator(raw, 'population')).place(relx=0, rely=0.1, anchor='w')

    label_GDP = tk.Label(label, text='Values are based upon GDP in national currency converted to U.S. dollars\n'
                                     'using market exchange rates (yearly average). Exchange rate projections are\n'
                                     'provided by country economists for the group of other emerging market and\n'
                                     'developing countries. Exchanges rates for advanced economies are established\n'
                                     'in the WEO assumptions for each WEO exercise. Expenditure-based GDP is total\n'
                                     'final expenditures at purchasers prices (including the f.o.b. value of exports\n'
                                     'of goods and services), less the f.o.b. value of imports of goods and services.').place(relx=0, rely=0.3, relwidth=1, anchor='nw')


    country_gdp = tk.Button(label, text='Display National GDP', command=lambda: economic_indicator(raw, 'gdp')).place(relx=0, rely=0.28, anchor='w')
    label_imexport = tk.Label(label, text='Percent change of volume of imports and exports of goods refer to\n'
                                          'the aggregate change in the quantities of imports/exports of goods\n'
                                          'whose characteristics are unchanged. The goods and their prices are held\n'
                                          'constant, therefore changes are due to changes in quantities only.').place(relx=0, rely=0.57, relwidth=1, anchor='nw')

    country_import = tk.Button(label, text='Display Import details', command=lambda: economic_indicator(raw, 'import')).place(relx=0, rely=0.55, anchor='w')
    country_export = tk.Button(label, text='Display Export details', command=lambda: economic_indicator(raw, 'export')).place(relx=0.28, rely=0.55, anchor='w')

    label_unemployment = tk.Label(label, text='The OECD harmonized unemployment rate gives the number of unemployed\n'
                                              'persons as a percentage of the labor force (the total number of people\n'
                                              'employed plus unemployed). [OECD Main Economic Indicators, OECD, monthly]\n'
                                              'As defined by the International Labour Organization, unemployed workers\n'
                                              'are those who are currently not working but are willing and able to work\n'
                                              'for pay, currently available to work, and have actively searched for work.').place(relx=0, rely=0.75, relwidth=1, anchor='nw')

    country_unemployment = tk.Button(label, text='Display Unemployment Rate', command=lambda: economic_indicator(raw, 'unemployment')).place(relx=0, rely=0.73, anchor='w')


root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()


frame = tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.05, relwidth=0.9, relheight=0.1, anchor='n')


button_SMA = tk.Button(frame, text='Algorithmic Trading', font=40, command=lambda: compute_SMA(clicked.get()))
button_SMA.place(relx=0, relwidth=1/4, relheight=1)


button_MPT = tk.Button(frame, text='Portfolio Analytics', font=40, command=lambda: compute_MPT(port))
button_MPT.place(relx=1/4, relwidth=1/4, relheight=1)


button_OPV = tk.Button(frame, text='Option Valuation', font=40, command=lambda: compute_OPV())
button_OPV.place(relx=2/4, relwidth=1/4, relheight=1)


button_CA = tk.Button(frame, text='Economic Indicators', font=40, command=lambda: IMF_Data())
button_CA.place(relx=3/4, relwidth=1/4, relheight=1)


lower_frame = tk.Frame(root, bg='#80c1ff', bd=6)
lower_frame.place(relx=0.5, rely=0.15, relwidth=0.9, relheight=0.8, anchor='n')


SBar = tk.Scrollbar(lower_frame)
SBar.pack(side=tk.RIGHT, fill='y')

TxtBox = tk.Text(lower_frame, height=HEIGHT, width=WIDTH, yscrollcommand=SBar.set, font='helvetica')
TxtBox.pack(expand=0, fill=tk.BOTH)

SBar.config(command=TxtBox.yview)


clicked = tk.StringVar()
clicked.set('Select Stock')


drop = tk.OptionMenu(root, clicked, *SP500)
drop.place(relx=0.4, rely=0.97, anchor='e')

port = []
def add():
    port.append(clicked.get())

def port_clear():
    port.clear()

portfolio = tk.Button(root, text='Add to Portfolio', command=add).place(relx=0.4, rely=0.97, anchor='w')
portfolio_clear = tk.Button(root, text='Clear Portfolio', command=port_clear).place(relx=0.58, rely=0.97, anchor='w')



root.mainloop()
