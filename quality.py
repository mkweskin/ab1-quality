#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog
from Bio import SeqIO
import os
import re

# ************************
# Scrollable Frame Class
# ************************
# This is from: https://gist.github.com/mp035/9f2027c3ef9172264532fcd6262f3b01
# With the file dialog box from: https://web.archive.org/web/20161228115250/https://tkinter.unpythonic.net/wiki/tkFileDialog
class ScrollFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent) # create a frame (self)

        # Get the screen height and make sure the height is no larger than this (with a bit bit extra for the task bar and title bar)
        windowheight = 500
        screenheight =root.winfo_screenheight() - 125
        if screenheight < windowheight:
            windowheight = screenheight
        print (windowheight)
        
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff", height=windowheight, width=450)          #place canvas on self
        self.viewPort = tk.Frame(self.canvas, background="#ffffff")                    #place a frame on the canvas, this frame will hold the child widgets 
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self 
        self.canvas.configure(yscrollcommand=self.vsb.set)                          #attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw",            #add view port frame to canvas
                                  tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)                       #bind an event whenever the size of the viewPort frame changes.

        self.onFrameConfigure(None)                                                 #perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)            #whenever the size of the canvas changes alter the window region respectively.


class Main(tk.Frame):
    def __init__(self, root):

        tk.Frame.__init__(self, root)
        self.scrollFrame = ScrollFrame(self) # add a new scrollable frame.
        
        # options for buttons
        button_opt = {'fill': tk.BOTH, 'padx': 5, 'pady': 5}

        # define buttons
        tk.Button(self, text='Choose folder to start analysis', command=self.processdirectory).pack(**button_opt)

        # outputbox: for the display of the full output
        global outputbox
        outputbox = tk.Text(self.scrollFrame.viewPort, height=25, width=50)
        outputbox.pack()

        # reportbox: for a summary report of what was prcoessed
        global reportbox
        reportbox = tk.Text(self.scrollFrame.viewPort, height=5, width=50)
        reportbox.insert("end","Reads AB1 files in the selected folder and returns: Well, Q20 length and full length.\nQ20 length is the number of bases with quality at least 20.")
        reportbox.configure(state="disabled")
        reportbox.pack()

        # defining options for opening a directory
        global direct
        direct = ''
        self.dir_opt = options = {}
        options['initialdir'] = 'C:\\Users'
        options['mustexist'] = True
        options['parent'] = self.scrollFrame.viewPort
        options['title'] = 'Choose the folder with the AB1 files'

        # when packing the scrollframe, we pack scrollFrame itself (NOT the viewPort)
        self.scrollFrame.pack(side="top", fill="both", expand=True)
        
        
    
    def printMsg(self, msg):
        print(msg)
    
    def processdirectory(self):

        """Opens a file box to select a directory and then processes it."""
        global direct
        if direct != '':
            self.dir_opt['initialdir'] = direct
        direct = filedialog.askdirectory(**self.dir_opt)
        if direct != '':
            output = ""
            outputbox.delete(1.0, "end")
            count = 0
            for seq in os.listdir(direct):
                if seq[-4:].lower() == ".ab1":
                    record = SeqIO.read(direct+'/'+seq,'abi')
                    qual = [ord(str(val)) for val in record.annotations['abif_raw']['PCON2'].decode('utf-8')]
                    q20 = sum(1 for i in qual if i >= 20)
                    fulllength=len(qual)
                    #m = re.search('(...)\.ab1',seq)
                    #well = m.group(1)
                    well = record.annotations['sample_well'].decode('utf-8')
                    col = record.annotations['sample_well'][0:1].decode('utf-8')
                    row = record.annotations['sample_well'][1:].decode('utf-8')
                    if len(row) == 1:
                        row = "0"+row
                    output += (col+row+"	"+str(q20)+"	"+str(fulllength)+"\n")
                    count+=1
            outputbox.insert("end", output)
            reportbox.configure(state="normal")
            reportbox.delete(1.0, "end")
            reportbox.insert("end","Folder: "+direct)
            reportbox.insert("end","\nCount: "+str(count))
            reportbox.insert("end","\n\nSelect new folder for new analysis.")
            reportbox.configure(state="disabled")
        return

if __name__ == "__main__":
    root=tk.Tk()
    Main(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
