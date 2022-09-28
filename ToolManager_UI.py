from argparse import FileType
from ast import Delete
import ToolManager
from config import *
import tkinter as TK
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
from tkinter import W, Entry, Checkbutton


class ToolManagerUi():

   def __init__(self):

      self.HEADER = ['GroupNr'], ['ToolID'], ['ToolNumber'],['ToolName'], ['ToolNoseRadius'], ['isRotary'], ['ToolCounterClockwise'], ['ToolY_Stroke']

      self.TOOLMODELFILE = TOOLMODELFILE
      self.ASMOD = ASMOD

      # get all Toolproperties from the ToolManager Module
      self.groupNumber = ToolManager.ToolManager(
         self.TOOLMODELFILE, self.ASMOD).getToolData()[0]
      self.tID = ToolManager.ToolManager(
         self.TOOLMODELFILE, self.ASMOD).getToolData()[1]
      self.tOffsNumber = ToolManager.ToolManager(
         self.TOOLMODELFILE, self.ASMOD).getToolData()[2]
      self.tName = ToolManager.ToolManager(
         self.TOOLMODELFILE, self.ASMOD).getToolData()[3]
      self.tNoseRadius = ToolManager.ToolManager(
         self.TOOLMODELFILE, self.ASMOD).getToolData()[4]
      self.tIsRotary = ToolManager.ToolManager(
         self.TOOLMODELFILE, self.ASMOD).getToolData()[5]
      self.tCCW = ToolManager.ToolManager(
         self.TOOLMODELFILE, self.ASMOD).getToolData()[6]
      self.tY = ToolManager.ToolManager(
         self.TOOLMODELFILE, self.ASMOD).getToolData()[7]

      self.mainWindow()

   def mainWindow(self):

      self.window = TK.Tk()
      self.window.geometry("900x350")
      self.window.title('Tool Manager')

      menubar = TK.Menu(self.window)

      filemenu = TK.Menu(menubar)
      filemenu.add_command(label="Open", command=self.onOpen)
      filemenu.add_command(label="Save", command=self.onSave)
      filemenu.add_command(label="Quit", command=self.closeAll)

      menubar.add_cascade(label="File", menu=filemenu)
      self.window.config(menu=menubar)

      self.tree = ttk.Treeview(self.window, column=(
         "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"), show='headings', height=5)

      self.tree.column("# 1", anchor='w')
      self.tree.heading("# 1", text="GroupNr")
      self.tree.column("# 2", anchor='w')
      self.tree.heading("# 2", text="ID")
      self.tree.column("# 3", anchor='w')
      self.tree.heading("# 3", text="KorrekturNr")
      self.tree.column("# 4", anchor='w')
      self.tree.heading("# 4", text="ToolName")
      self.tree.column("# 5", anchor='w')
      self.tree.heading("# 5", text="ToolNoseRadius")
      self.tree.column("# 6", anchor='w')
      self.tree.heading("# 6", text="FräsWerkzeug")
      self.tree.column("# 7", anchor='w')
      self.tree.heading("# 7", text="CounterClockWise")
      self.tree.column("# 8", anchor='w')
      self.tree.heading("# 8", text="ToolShiftY")

      # Insert the data in Treeview widget
      self.refreshTreeViewData()
      
      # create Tool Editor child Window
      self.EditWindow = Toplevel(self.window)

      self.EditWindow.geometry("390x250")
      self.EditWindow.title('Tool Manager EditWindow')

      GroupLabel = TK.Label(self.EditWindow, text="GroupNr :")
      GroupLabel.grid(row=0, column=1, sticky=W)
      self.GroupNr = Entry(self.EditWindow, width = 20)
      self.GroupNr.grid(row=0, column=2)

      NameLabel = TK.Label(self.EditWindow, text="Tool Description :")
      NameLabel.grid(row=1, column=1, sticky=W)
      self.Name = Entry(self.EditWindow, width = 20)
      self.Name.grid(row=1, column=2)

      IDlabel = TK.Label(self.EditWindow, text="Tool ID :")
      IDlabel.grid(row=2, column=1, sticky=W)
      self.ID = Entry(self.EditWindow, width = 20)
      self.ID.grid(row=2, column=2)

      OffsetLabel = TK.Label(self.EditWindow, text="Tool Offset Number :")
      OffsetLabel.grid(row=3, column=1, sticky=W)
      self.Offset = Entry(self.EditWindow, width = 20)
      self.Offset.grid(row=3, column=2)

      ToolNoseRadiusLabel = TK.Label(self.EditWindow, text="Toolnose Radius :")
      ToolNoseRadiusLabel.grid(row=4, column=1, sticky=W)
      self.ToolNoseRadius = Entry(self.EditWindow, width = 20)
      self.ToolNoseRadius.grid(row=4, column=2)

      IsMillingToolLabel = TK.Label(self.EditWindow, text="Is it a Milling Tool? :")
      IsMillingToolLabel.grid(row=5, column=1, sticky=W)
      self.IsMillingTool = Checkbutton(self.EditWindow)
      self.IsMillingTool.grid(row=5, column=2, sticky=W)
      
      IsCCWLabel = TK.Label(self.EditWindow, text="Turningdirection CCW? :")
      IsCCWLabel.grid(row=6, column=1, sticky=W)
      self.IsCCW = Checkbutton(self.EditWindow)
      self.IsCCW.grid(row=6, column=2, sticky=W)

      ToolshiftYLabel = TK.Label(self.EditWindow, text="Toolshift in Y :")
      ToolshiftYLabel.grid(row=7, column=1, sticky=W)
      self.ToolshiftY = Entry(self.EditWindow, width = 20)
      self.ToolshiftY.grid(row=7, column=2)

      self.SaveNewToolData = TK.Button(self.EditWindow, text="Save", command=self.getDataFromEditWindow)
      self.SaveNewToolData.grid(row=8, column=2, sticky=E)

      self.window.mainloop()

   def onOpen(self):
      print(filedialog.askopenfilename(initialdir="/", title="Open File",
                                       filetypes=(("Python files", "*.TMD;*.XML"), ("All files", "*.*"))))

   def onSave(self):
      uISaveFile = filedialog.asksaveasfilename(defaultextension='.csv')
      # split the string on all "/" and turn the string into a list
      uISaveFile = str(uISaveFile).split("/")
      # get the last name, the Filename, out of the list
      finalUISaveFile = uISaveFile.pop()
      # check if the Filename is invalid. if not, send filename to the ToolManager Module.
      if uISaveFile is None:
         return None, print("No Filename entered!")
      else:
         return ToolManager.ToolManager.writeToFile(self, finalUISaveFile), print("OK!")

   def onRelease(self, event):
      self.GroupNr.delete(0, END)
      self.Name.delete(0, END)
      self.ID.delete(0, END)
      self.Offset.delete(0 ,END)
      self.ToolNoseRadius.delete(0 ,END)
      self.ToolshiftY.delete(0, END)
      self.IsMillingTool.deselect()
      self.IsCCW.deselect()

      item = self.tree.selection()
      for i in item: 
         self.GroupNr.insert(END, str(self.tree.item(i, "values")[0]))
         self.ID.insert(END, str(self.tree.item(i, "values")[1]))
         self.Offset.insert(END, str(self.tree.item(i, "values")[2]))
         self.Name.insert(END, str(self.tree.item(i, "values")[3]))
         self.ToolNoseRadius.insert(END, str(self.tree.item(i, "values")[4]))
         self.ToolshiftY.insert(END, str(self.tree.item(i, "values")[7]))
         if self.tree.item(i, "values")[5] == "true":
            self.IsMillingTool.select()
         else:
            self.IsMillingTool.deselect()

         if self.tree.item(i, "values")[6] == "true":
            self.IsCCW.select()
         else:
            self.IsCCW.deselect()


   def getDataFromEditWindow(self):
      getID = self.ID.get()
      getName = self.Name.get()
      getOffs = self.Offset.get()
      getToolNoseRadius = self.ToolNoseRadius.get()
      ToolManager.ToolManager.saveToList(self, str(getID), str(getName), str(getOffs), str(getToolNoseRadius))
      
      #funzt nicht, muss angeblich mit durch iterieren funktionieren.
      #self.tree.delete(*self.tree.get_children)

   def refreshTreeViewData(self):
      print("in rTVD")
      length = len(self.tID)
      for i in range(length):
         self.tree.insert('', 'end', text="1", values=(self.groupNumber[i],
                                                    self.tID[i],
                                                    self.tOffsNumber[i],
                                                    self.tName[i].strip("'[]'"),
                                                    self.tNoseRadius[i],
                                                    self.tIsRotary[i],
                                                    self.tCCW[i],
                                                    self.tY[i]))
      self.tree.bind('<ButtonRelease-1>', self.onRelease)
      self.tree.pack(expand=True, fill='y' )



   def closeAll(self):
      self.window.quit()



if __name__ == '__main__':
    ToolManagerUi()
