#!/usr/bin/python3
# -*- coding: UTF8 -*-
'''
@created: 27-09-2024 09:51:55
@author: rafael
@description: finestra de numeració automàtica

requisits:
   sudo apt-get install python3-tk
'''

import tkinter as tk
from tkinter import ttk

def next():
   global seq_num, seq_text, orange
   if seq_num % 5 == 0 and not orange:
      seq_text.config(fg='white', bg='orange')
      seq_text.config(text=frmt(seq_num))
      orange = True
   else:
      orange = False
      seq_num = seq_num + 1
      seq_text.config(fg='white', bg='blue')
      seq_text.config(text=frmt(seq_num))

def espai():
   espai = tk.Label(root, text="\n")
   espai.config(font=("Sans",20),justify="center")
   espai.pack()

def frmt(n):
   return " "+str(n)+" "

root = tk.Tk()
root.geometry("800x800")
root.title = "número actual"

espai()
orange = False
seq_num = 1
seq_text = tk.Label(root, text=frmt(seq_num))
seq_text.config(font=("Ubuntu Mono",400), justify="center", fg='white', bg='blue')
seq_text.pack()
espai()

ttk.Button(root, text="següent", command=next).pack()

root.mainloop()
