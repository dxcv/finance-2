import tkinter as tk
from Quandl import *


HEIGHT = 740
WIDTH = 600


def compute_SMA(select):
    label['text'] = SMA(select)


def compute_MPT(port):
    label['text'] = MPT(list(set(port)))


def compute_OPV():
    label_P0 = tk.Label(lower_frame, text='Initial Price of an underlying product(example 100):')
    label_P0.pack()
    entry_P0 = tk.Entry(lower_frame, font=40)
    entry_P0.place(relwidth=1, relheight=0.5)
    entry_P0.pack()
    label_PT = tk.Label(lower_frame, text='Strike price(example 120):')
    label_PT.pack()
    entry_PT = tk.Entry(lower_frame, font=40)
    entry_PT.place(relwidth=1, relheight=0.5)
    entry_PT.pack()
    label_Rft = tk.Label(lower_frame, text='Risk Free Interest Rate(example 0.05):')
    label_Rft.pack()
    entry_Rft = tk.Entry(lower_frame, font=40)
    entry_Rft.place(relwidth=1, relheight=0.5)
    entry_Rft.pack()
    label_T = tk.Label(lower_frame, text='Time Horizon in years(example 2):')
    label_T.pack()
    entry_T = tk.Entry(lower_frame, font=40)
    entry_T.place(relwidth=1, relheight=0.5)
    entry_T.pack()
    label_option = tk.Label(lower_frame, text='Call[Yes]/Put[No](example Yes):')
    label_option.pack()
    entry_option = tk.Entry(lower_frame, font=40)
    entry_option.place(relwidth=1, relheight=0.5)
    entry_option.pack()

    button_gen = tk.Button(lower_frame, text='Valuation', font=40, command=lambda: OPV(S0=entry_P0.get(), K=entry_PT.get(), r=entry_Rft.get(), T=entry_T.get(), option_type=entry_option.get()))
    button_gen.place(relx=1/3, rely= 3/7, relwidth=1/3, relheight=0.05)


root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()


def show():
    tk.Label(root, text=clicked.get()).pack()


frame = tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.05, relwidth=0.75, relheight=0.1, anchor='n')


button_SMA = tk.Button(frame, text='Algorithmic Trading', font=40, command=lambda: compute_SMA(clicked.get()))
button_SMA.place(relx=0, relwidth=1/3, relheight=1)


button_MPT = tk.Button(frame, text='Portfolio Analytics', font=40, command=lambda: compute_MPT(port))
button_MPT.place(relx=1/3, relwidth=1/3, relheight=1)


button_OPV = tk.Button(frame, text='Option Valuation', font=40, command=lambda: compute_OPV())
button_OPV.place(relx=2/3, relwidth=1/3, relheight=1)


lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
lower_frame.place(relx=0.5, rely=0.15, relwidth=0.75, relheight=0.8, anchor='n')


label = tk.Label(lower_frame, anchor='nw', justify='left')
label.place(relwidth=1, relheight=1)


clicked = tk.StringVar()
clicked.set('Select Stock')


drop = tk.OptionMenu(root, clicked, *SP500)
drop.config(font=('calibri',(15)),bg='white')
drop.pack()


port = []
def add():
    port.append(clicked.get())

portfolio = tk.Button(root, text='Add to Portfolio', command=add).pack()

root.mainloop()