from tkinter import *
from tkinter import ttk, filedialog
from commandWig import commandWig
import subprocess

def focus_next_window(event):
        event.widget.tk_focusNext().focus()
        return("break")

class winBuild:
    """A builder which creates a window based on a list of provided widgets.

    :param master: master of the window
    :param wigList: list of widgets necessary to complete a command window. If element in list is equal to 'optional',
    we change the current widget list to optWig and start adding widgets there. Those widgets are optional to the qiime2.

    :param reqWig: list of required widgets, used later to validate insterted values
    :type reqWig: list
    :param optWig: list of optional widgets
    :type optWig: list
    :param curMaster: parameter used to switch pages in the ttk.Notebook widget and create the "Optional" methods tab in the window
    :param optionalPage: a flag signaling if there's an "Optional" page
    :type optionalPage: bool
    """
    def __init__(self,master,wigList,key):
        self.reqWig = []
        self.optWig = []
        self.widgets = self.reqWig
        self.comLab = Label(master,text="qiime "+key)
        self.comLab.pack()
        self.notepad = ttk.Notebook(master)
        self.container = Frame(self.notepad)
        self.curMaster = self.container
        self.optionalPage = False
        ### 
        #Temporary Checkbutton, for bug testing. If it's marked, the "Proceed" button runs the command with subprocess()
        self.rcValue = IntVar()
        self.runCommand = Checkbutton(self.curMaster, text = "'Proceed' button runs the command", variable = self.rcValue, onvalue=1, offvalue = 0)
        self.runCommand.pack()
        ###
        for ele in wigList:
            if ele[0] == "combo":
                w = comboLis(self.curMaster,ele)
                w.pack(fill=BOTH)
                self.widgets.append(w)
            elif ele[0] == "fChoose":
                w = fileChoice(self.curMaster,ele)
                w.pack(fill=BOTH)
                self.widgets.append(w)
            elif ele[0] == "fName":
                w = fileName(self.curMaster,ele)
                w.pack(fill=BOTH)
                self.widgets.append(w)
            elif ele[0] == "fDir":
                w = dirName(self.curMaster,ele)
                w.pack(fill=BOTH)
                self.widgets.append(w)
            elif ele[0] == "ifSpin":
                w = intFloSpinbox(self.curMaster,ele)
                w.pack(fill=BOTH)
                self.widgets.append(w)
            elif ele[0] == "importChoose":
                w = importChoose(self.curMaster,ele)
                w.pack(fill=BOTH)
                self.widgets.append(w)
            elif ele == "optional":
                self.widgets = self.optWig
                self.newPage = Frame(self.notepad)
                self.curMaster = self.newPage
                self.optionalPage = True
        self.notepad.add(self.container,text="Required")
        if self.optionalPage:
            self.notepad.add(self.newPage, text="Optional")
        self.notepad.pack()
        self.showMe = Button(master,text='Proceed',command=lambda key=key: self.pullValues(key,master))
        self.showMe.pack()

    def pullValues(self,key,master):
        """Function to pull all values from the widgets in created window. Also checks if all required spaces are filled.
        """
        storedReq = []
        storedOpt = []
        for widg in self.reqWig:
            w = widg.getValue()
            if '' in w:
                print("Fill all required spaces!")
                return True
            storedReq.append(w)
        for widg in self.optWig:
            storedOpt.append(widg.getValue())
        flatWidgetList = [item for sublist in storedReq for item in sublist] + [item for sublist in storedOpt for item in sublist]
        finalCommand = "qiime " + key + ' ' + ' '.join(flatWidgetList)
        print(finalCommand)
        print(flatWidgetList)
        master.destroy()
        if self.rcValue.get() == 1:
            subprocess.run(finalCommand.split())
        

class comboLis(Frame):
    """Widget with a label and a combobox.
    """
    def __init__(self,master,wigList):
        super().__init__(master = master,bd = 2)
        self.cName = wigList[1]
        self.Lab = Label(self,text = self.cName,width= 25)
        self.dpList = ttk.Combobox(self,values = wigList[2],state="readonly",width = 45)
        self.dpList.current(0)
        self.Lab.pack(side = LEFT,fill = BOTH)
        self.dpList.pack(fill = BOTH,side=RIGHT,expand = True)
    
    def getValue(self):
        commandLabel,argument = self.cName,self.dpList.get()
        if argument == '':
            return ''
        else:
            return (commandLabel,argument)

class fileChoice(Frame):
    """Widget with a label, a button which allows user to choose a file, and a text box to showcase that files path
    """
    def __init__(self,master,wigList):
        super().__init__(master = master,bd = 2)
        #self.master = master
        self.cName = wigList[1]
        self.Lab = Label(self,text = self.cName,width = 25)
        self.Lab.pack(side = LEFT,fill = BOTH)
        self.fVal = ''
        self.fButton = Button(self,text='Choose file',command=self.giveFile)
        self.fText = Text(self,width=28, height = 1, wrap = NONE)
        self.fText.bind("<Tab>",focus_next_window)
        self.fText.pack(side = RIGHT,fill = BOTH, expand = True)
        self.fButton.pack(side = RIGHT)

    def giveFile(self):
        """Function for the button. Opens a dialog window where user can select a file, then inserts that files directory
        into the text box (fText)
        """
        self.fVal = filedialog.askopenfilenames(initialdir = '/', title = "Select file", filetypes = (("all files","*.*"),("txt files","*.txt")))
        if self.fVal != '':
            self.fText.delete(0.0,END)
            self.fText.insert(0.0,self.fVal)
    def getValue(self):
        commandLabel,argument = self.cName,self.fText.get(0.0,END).strip()
        if argument == '':
            return ''
        else:
            return (commandLabel,argument)

class importChoose(Frame):
    """Widget for 'qiime tools import' command, which requires an option to choose a file OR directory
    """
    def __init__(self,master,wigList):        
        super().__init__(master = master,bd = 2)
        self.cName = wigList[1]
        self.Lab = Label(self,text = self.cName,width = 25)
        self.Lab.pack(side = LEFT,fill = BOTH)
        self.fVal = ''
        self.fButton = Button(self,text='Choose file',command=self.giveFile)
        self.dirButton = Button(self,text='Choose dir',command=self.giveDir)
        self.fText = Text(self,width=28, height = 1, wrap = NONE)
        self.fText.bind("<Tab>",focus_next_window)
        self.fButton.pack(side = LEFT)
        self.dirButton.pack(side = LEFT)
        self.fText.pack(side = BOTTOM, fill = BOTH, expand = True) 

    def giveFile(self):
        """Function for the button. Opens a dialog window where user can select a file, then inserts that files directory
        into the text box (fText)
        """
        self.fVal = filedialog.askopenfilenames(initialdir = '/', title = "Select file", filetypes = (("all files","*.*"),("txt files","*.txt")))
        if self.fVal != '':
            self.fText.delete(0.0,END)
            self.fText.insert(0.0,self.fVal)      
    
    def giveDir(self):
        """Function for the button. Opens a dialog window where user can choose a directory
        """
        self.fVal = filedialog.askdirectory()
        self.fText.delete(0.0,END)
        self.fText.insert(0.0,self.fVal)
    
    def getValue(self):
        commandLabel,argument = self.cName,self.fText.get(0.0,END).strip()
        if argument == '':
            return ''
        else:
            return (commandLabel,argument)


class fileName(Frame):
    """Widget with a label and a text box.
    """
    def __init__(self,master,wigList):
        super().__init__(master = master,bd = 2)
        self.cName = wigList[1]
        self.Lab = Label(self,text = self.cName,width = 25)
        self.Lab.pack(side = LEFT,fill = BOTH)
        self.fText = Text(self,width=28, height = 1, wrap = NONE)
        self.fText.bind("<Tab>",focus_next_window)
        self.fText.pack(side = RIGHT,fill = BOTH, expand = True)

    def getValue(self):
        commandLabel,argument = self.cName,self.fText.get(0.0,END).strip()
        if argument == '':
            return ''
        else:
            return (commandLabel,argument)

class dirName(Frame):
    """Widget with a label, a button which allows user to choose a directory, and a text box which shows that dirs path
    """
    def __init__(self,master,wigList):
        super().__init__(master = master,bd = 2)
        self.cName = wigList[1]
        self.Lab = Label(self,text = self.cName,width = 25)
        self.Lab.pack(side = LEFT,fill = BOTH)
        self.fDir = ''
        self.fButton = Button(self,text = "Choose directory", command = self.giveDir)
        self.fButton.pack(side = LEFT,fill = BOTH, expand = True)
        self.fText = Text(self,width=28, height = 1, wrap = NONE)
        self.fText.bind("<Tab>",focus_next_window)
        self.fText.pack(side = RIGHT,fill = BOTH, expand = True)

    def giveDir(self):
        """Function for the button. Opens a dialog window where user can choose a directory
        """
        self.fDir = filedialog.askdirectory()
        self.fText.delete(0.0,END)
        self.fText.insert(0.0,self.fDir)

    def getValue(self):
        commandLabel,argument = self.cName,self.fText.get(0.0,END).strip()
        if argument == '':
            return ''
        else:
            return (commandLabel,argument)

class intFloSpinbox(Frame):
    """Widget with a spinbox that only allows numbers. Numbers can be int of float type.
    """
    def __init__(self,master,wigList):
        super().__init__(master = master,bd = 2)
        self.cName = wigList[1]
        self.Lab = Label(self,text = self.cName,width = 25)
        self.Lab.pack(side = LEFT,fill = BOTH)
        var = StringVar(self)
        if wigList[2]:
            var.set(wigList[3])
            self.sBox = Spinbox(self,from_=0,to=1000000000, textvariable=var)
        else:
            var.set(wigList[3])
            self.sBox = Spinbox(self,from_=0,to=1000000000, textvariable=var,increment=0.1, format="%.1f")
        self.sBox.pack(side = RIGHT,fill = BOTH, expand = True)
    
    def getValue(self):
        commandLabel,argument = self.cName,self.sBox.get()
        if argument == '':
            return ''
        else:
            return (commandLabel,argument)

if __name__ == "__main__":
    root = Tk()
    test = (["combo","--combo-box",["ele1","ele2"]],
    ["fChoose","--file-choose"],
    ["fName","--file-name"],
    ["fDir","--directory-choose"],
    ["ifSpin","--spinbox-float",False,"2.0"],
    ["ifSpin","--spinbox-interger",True,1],
    ["importChoose","--import-choose"],
    "optional",
    ["fChoose","--file-choose-test"],
    ["fName","--file-name-test"],
    ["fDir","--directory-choose-test"],
    ["ifSpin","--spinbox-test",False,"2.0"],
    ["importChoose","--import-choose-test"])
    wind = winBuild(root,test,"test")
    root.mainloop()

