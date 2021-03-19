from winBuilder import *
from os import path, makedirs

TREE_COMMAND_INDEX = 0 #Index for pipeline-tree widget, used to mark each command's key so multiple same commands can be in the tree
SAVE_PATH = "pipelines"

try:
    makedirs(SAVE_PATH)
except FileExistsError:
    pass

class emptyClass():
    def __init__(self):
        self.key = ''
        self.optValues = ''
        self.reqValues = ''

pipelineTreeContent = emptyClass()

def popupWig(master,widget,key):
    """Uses winBuild to create a pop-up window with instructions from widget and key.

    :param widget: a nested list of widgets used in the pop-up window for that command
    :type widget: tuple

    :param key: name of the command 
    :type key: str 
    """
    newWindow = Toplevel(master)
    newWindow.title("New Window")
    global pipelineTreeContent
    pipelineTreeContent = winBuild(newWindow,widget,key)

root = Tk()
root.title("Main Menu")
root.geometry("500x400")
menuBar = Menu(root)

commands = Menu(menuBar,tearoff=0)
for package in commandWig.keys():
    subMenu = Menu(commands,tearoff=0)
    for key in commandWig[package]:
        subMenu.add_command(label="{}".format(key),command=lambda packKey=(package,key): popupWig(subMenu,commandWig[packKey[0]][packKey[1]],packKey[1]))
    commands.add_cascade(label="{}".format(package),menu=subMenu,underline=0)
menuBar.add_cascade(label = "Commands",menu = commands)

root.config(menu=menuBar)

### Pipeline - tree section ### 
tree = ttk.Treeview(root, columns = ("Stuff"))
tree.heading("#0", text = "Command")
tree.heading("#1", text = "Content")
tree.pack() 

def addCommandToTree(key,reqWidgets,optWidgets):
    global TREE_COMMAND_INDEX
    commandKey = key + "$" + str(TREE_COMMAND_INDEX)
    TREE_COMMAND_INDEX+=1
    tree.insert(parent = "", index = "end", iid = commandKey, text = key, values = "")
    print("iid: ", commandKey, "\nkey: ", key, "\nreqWidgets: ",reqWidgets,"\noptWidgets: ",optWidgets)
    for parameter,value in reqWidgets:
        tree.insert(parent = commandKey, index = "end", text = parameter, values = value)
    if optWidgets:
        optIID = commandKey + "optional"
        tree.insert(parent = commandKey, index = "end", iid = optIID, text = "Optional")
        for parameter,value in optWidgets:
            tree.insert(parent = optIID, index = "end", text = parameter, values = value)

def selectbranch(event):
    """Double-click event; when you doubleclick after selecting a cell with content, 
    it creates an Edit Window, where you can change the selected value.
    """
    #Create editWindow only for columns with content
    clmn = tree.identify_column(event.x)
    if clmn != "#1":
        return False
    content = tree.selection()
    try:
        #print("here")
        treeItem = tree.item(content)
        treeItemValue = treeItem["values"][0]
    except IndexError:
        return False
    #print("content: ",content, "\ntreeItem: ", treeItem)
    editWindow = Toplevel(root)
    editWindow.title("Edit parameter")
    eW_Label = Label(editWindow, text = treeItem['text'])
    eW_TextWindow = Text(editWindow, height = 1, width = 50)
    eW_TextWindow.insert(INSERT, treeItemValue)
    eW_Label.pack()
    eW_TextWindow.pack()
    def replaceValue():
        tree.set(content, column= clmn, value = str(eW_TextWindow.get(0.0,END)).strip())
        editWindow.destroy()
    eW_Button = Button(editWindow, text = "Save", command = replaceValue)
    eW_Button.pack()

tree.bind('<Double-1>', selectbranch)

def handleCommand():
    """Function for the button; uses addCommandToTree to add command to tree, then resets pipelineTreeContent to empty state 
    """
    global pipelineTreeContent
    if pipelineTreeContent.key:
        addCommandToTree(pipelineTreeContent.key,pipelineTreeContent.reqValues,pipelineTreeContent.optValues)
        pipelineTreeContent = emptyClass()

showMeContentForTree = Button(master = root, text = "Add last command to pipeline", command = handleCommand)
showMeContentForTree.pack()

### Get children ###
def runTree():
    """Function for "Run pipeline" button in the pipeline widget. Pull all functions and parameters in the tree and passes them to bash.
    Currently only prints commands instead of running in bash.
    """
    mainBranches = tree.get_children()
    commandsInPipeline = []
    #print(mainBranches)
    for commandIds in mainBranches:
        subprocessPrintOut = 'qiime ' + commandIds.split("$")[0]
        print(commandIds.split("$")[0])
        command = tree.get_children(commandIds)
        print("Required:")
        for ids in command:
            parameter = tree.item(ids)
            if not parameter['values']:
                optionalParameters = tree.get_children(commandIds+"optional")
                print("Optional:")
                for subIds in optionalParameters:
                    parameter = tree.item(subIds)
                    subprocessPrintOut = subprocessPrintOut + ' ' + str(parameter['text']) + ' ' + str(parameter['values'][0])
                    print(parameter['text'],parameter['values'][0])
            else:
                subprocessPrintOut = subprocessPrintOut + ' ' + str(parameter['text']) + ' ' + str(parameter['values'][0])
                print(parameter['text'],parameter['values'][0])
        commandsInPipeline.append(subprocessPrintOut)
    for printoutstuff in commandsInPipeline:
        print(printoutstuff,end='\n')


childButton = Button(master = root, text = "Run", command = runTree)
childButton.pack()
###
def saveTree():
    #fileName = "test.txt"
    #completeName = path.join(SAVE_PATH,fileName)
    saveFile = filedialog.asksaveasfile(mode = 'w', defaultextension = ".txt")
    if saveFile is None:
        return
    #saveFile = open(completeName, "w")
    mainBranches = tree.get_children()
    ############
    marker = False
    ############
    for commandIds in mainBranches:
        saveFile.write(commandIds.split("$")[0] + "\n")
        command = tree.get_children(commandIds)
        saveFile.write("Required:\n")
        for ids in command:
            parameter = tree.item(ids)
            if not parameter['values']:
                marker = True
                optionalParameters = tree.get_children(commandIds+"optional")
                saveFile.write("\nOptional:\n")
                for subIds in optionalParameters:
                    parameter = tree.item(subIds)
                    saveFile.write('{} {} '.format(parameter['text'],parameter['values'][0]))
            else:
                saveFile.write('{} {} '.format(parameter['text'],parameter['values'][0]))
        # If no optional arguments, write the lines for optional anyway
        if marker == False:
            saveFile.write("\nOptional:\n")
        marker = False
        saveFile.write("\n###\n")
    saveFile.close()

saveButton = Button(master = root, text = "Save", command = saveTree)
saveButton.pack()

###
def openTree():
    completeName = filedialog.askopenfilenames(initialdir = './', title = "Select file", filetypes = (("all files","*.*"),("txt files","*.txt")))
    if completeName == '':
        return
    # try:
    #     fileTree = open(completeName[0], 'r')
    # except FileNotFoundError:
    #     return 
    fileTree = open(completeName[0], 'r')
    tree.delete(*tree.get_children())
    key = ''
    reqWidgets = []
    optWidgets = []
    action = 1
    for line in fileTree:
        if action == 1:
            key = line.strip()
            action = action%6 + 1
        elif action == 2 or action == 4:
            action = action%6 + 1
        elif action == 3:
            arguments = line.split(" ")
            for pair in range(0,len(arguments),2):
                try:
                    reqWidgets.append((str(arguments[pair]),str(arguments[pair+1])))
                except IndexError:
                    action = action%6 + 1
                    pass
        elif action == 5:
            arguments = line.split(" ")
            for pair in range(0,len(arguments),2):
                try:
                    optWidgets.append((str(arguments[pair]),str(arguments[pair+1])))
                except IndexError:
                    action = action%6 + 1
                    pass
        elif action == 6:
            addCommandToTree(key,reqWidgets,optWidgets)
            key = ''
            reqWidgets = []
            optWidgets = []
            action = action%6 + 1
    fileTree.close()


openPipeButton = Button(master = root, text = "Open", command = openTree)
openPipeButton.pack()


###
root.mainloop()