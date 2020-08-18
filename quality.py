#!/usr/bin/env python2
import Tkinter, Tkconstants, tkFileDialog
from Bio import SeqIO
import os
import re

#Tkinter code modified from: https://tkinter.unpythonic.net/wiki/tkFileDialog
class TkFileDialogExample(Tkinter.Frame):

  def __init__(self, root):

    Tkinter.Frame.__init__(self, root)

    self.bind_class("Text","<Control-a>", self.selectall)
    self.bind_class("Text","<Command-a>", self.selectall)

    # options for buttons
    button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

    # define buttons
    Tkinter.Button(self, text='Choose folder to start analysis', command=self.askdirectory).pack(**button_opt)
    #Tkinter.Button(self, text='Select', command=self.selectall).pack(**button_opt)

    # Output box
    global outputbox
    outputbox = Tkinter.Text(root, height=50, width=50)
    outputbox.pack()

    #Report box
    global reportbox
    reportbox = Tkinter.Text(root, height=5, width=50)
    reportbox.insert("end","Reads AB1 files in the selected folder and returns: Well, Q20 length and full length.\nQ20 length is the number of bases with quality at least 20.")
    reportbox.configure(state="disabled")
    reportbox.pack()

    # defining options for opening a directory
    global direct
    direct = ''
    self.dir_opt = options = {}
    options['initialdir'] = 'E:\\AppliedBiosystems\UDC\DataCollection\data'
    options['mustexist'] = True
    options['parent'] = root
    options['title'] = 'Choose the folder with the AB1 files'


  def askdirectory(self):

    """Returns a selected directoryname."""
    global direct
    if direct != '':
        self.dir_opt['initialdir'] = direct
    direct = tkFileDialog.askdirectory(**self.dir_opt)
    if direct != '':
        output = ""
        outputbox.delete(1.0, "end")
        count = 0
        for seq in os.listdir(direct):
            if seq[-4:].lower() == ".ab1":
                record = SeqIO.read(direct+'/'+seq,'abi')
                qual = [ord(val) for val in record.annotations['abif_raw']['PCON2']]
                q20 = sum(1 for i in qual if i >= 20)
                fulllength=len(qual)
                #m = re.search('(...)\.ab1',seq)
                #well = m.group(1)
                well = record.annotations['sample_well']
                col = record.annotations['sample_well'][0:1]
                row = record.annotations['sample_well'][1:]
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

  def selectall(self, event):
    outputbox.tag_add('sel','1.0','end')
    return


if __name__=='__main__':
  root = Tkinter.Tk()
  TkFileDialogExample(root).pack()
  root.mainloop()
