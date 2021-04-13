from winBuilder import *
from os import path, makedirs

TREE_COMMAND_INDEX = 0 #Index for pipeline-tree widget, used to mark each command's key so multiple same commands can be in the tree
SAVE_PATH = "pipelines"

# Create "pipelines" directory
try:
    makedirs(SAVE_PATH)
except FileExistsError:
    pass

# Empty class for the container with last command
class emptyClass():
    def __init__(self):
        self.key = ''
        self.optValues = ''
        self.reqValues = ''

pipelineTreeContent = emptyClass()

# Create/empty-out log.file
logfile = open("log.file","w")
logfile.close()

# Create popup window with command
def popupWig(master,widget,key):
    """Uses winBuild to create a pop-up window with instructions from widget and key.

    :param widget: a nested list of widgets used in the pop-up window for that command
    :type widget: tuple

    :param key: name of the command 
    :type key: str 
    """
    newWindow = Toplevel(master)
    newWindow.title("{}".format(key))
    global pipelineTreeContent
    pipelineTreeContent = winBuild(newWindow,widget,key)

# Main Menu set-up
root = Tk()
root.title("Main Menu")
root.geometry("700x500")
menuBar = Menu(root)

# Menu Bar 
commands = Menu(menuBar,tearoff=0)
for package in commandWig.keys():
    subMenu = Menu(commands,tearoff=0)
    for key in commandWig[package]:
        subMenu.add_command(label="{}".format(key),command=lambda packKey=(package,key): popupWig(subMenu,commandWig[packKey[0]][packKey[1]],packKey[1]))
    commands.add_cascade(label="{}".format(package),menu=subMenu,underline=0)
menuBar.add_cascade(label = "Commands",menu = commands)

root.config(menu=menuBar)

# Frame for mainMenu elements
mmFrame = Frame(root)
mmFrame.config(background = "green")
mmFrame.pack()

### Pipeline section ###

# TreeView set-up
tree = ttk.Treeview(mmFrame, columns = ("Stuff"))
tree.heading("#0", text = "Command")
tree.heading("#1", text = "Content")
tree.grid(row = 0, column = 0)

# Add last command to tree
def addCommandToTree(key,reqWidgets,optWidgets):
    if reqWidgets == []:
        return
    global TREE_COMMAND_INDEX
    TREE_COMMAND_INDEX+=1
    parentID = tree.insert(parent = "", index = "end", text = key, values = "")
    for parameter,value in reqWidgets:
        tree.insert(parent = parentID, index = "end", text = parameter, values = value)
    if optWidgets:
        subParentID = tree.insert(parent = parentID, index = "end", text = "Optional")
        for parameter,value in optWidgets:
            tree.insert(parent = subParentID, index = "end", text = parameter, values = value)

def handleCommand():
    """Function for the button; uses addCommandToTree to add command to tree, then resets pipelineTreeContent to empty state 
    """
    global pipelineTreeContent
    if pipelineTreeContent.key:
        addCommandToTree(pipelineTreeContent.key,pipelineTreeContent.reqValues,pipelineTreeContent.optValues)
        pipelineTreeContent = emptyClass()

# Edit selected content in pipeline
def selectbranch(event):
    """Double-click event; when you doubleclick after selecting a cell with content, 
    it creates an Edit Window, where you can change the selected value.
    """
    # Create editWindow only for columns with content
    clmn = tree.identify_column(event.x)
    if clmn != "#1":
        return 
    content = tree.selection()
    try:
        treeItem = tree.item(content)
        treeItemValue = treeItem["values"][0]
    except IndexError:
        return 
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

# Manage communication between bash and program
def communicate(processChild):
    """
    Handle return codes form processes, produce appropriate messages and write error messages to log.file
    """
    rc = processChild.returncode
    if rc != 0:
        with open("log.file","w") as logfile:
            logfile.write(processChild.stderr.decode("utf-8"))
        messageBox.config(state=NORMAL)
        messageBox.insert(END, " ".join(processChild[0:3]),"ended in an error. For more information check log.file","error")
        messageBox.config(state=NORMAL)
        return
    else:
        messageBox.config(state=NORMAL)
        messageBox.insert(END, "Success!\n","success")
        messageBox.config(state=NORMAL)


# Run pipeline in bash
def runTree():
    """
    Function for "Run pipeline" button in the pipeline widget. Pull all functions and parameters in the tree and passes them to bash.
    Currently only prints commands instead of running in bash. 
    Allows starting pipeline from selected command instead of from the beginning.
    """
    mainBranches = tree.get_children()
    sP = 0 # Starting Point
    if sPC_Value.get() == 1:
        try:
            currentSel = tree.focus()
            # Search for main branch
            while currentSel not in mainBranches:
                currentSel = tree.parent(currentSel)
            sP = mainBranches.index(currentSel)
        except ValueError:
            pass
    commandsInPipeline = []
    #rc = 0
    for branch in mainBranches[sP:]:
        command = 'qiime'
        command = command + ' ' + tree.item(branch)["text"]
        children = tree.get_children(branch)
        for child in children:
            currentChild = tree.item(child)
            if currentChild["text"] == 'Optional':
                optChildren = tree.get_children(child)
                for optChild in optChildren:
                    currOptChild = tree.item(optChild)
                    command = command + ' ' + currOptChild["text"] + ' ' + str(currOptChild["values"][0])
            else:
                command = command + ' ' + currentChild["text"] + ' ' + str(currentChild["values"][0])
        commandsInPipeline.append(command)
    for printoutstuff in commandsInPipeline:
        print(printoutstuff,end='\n')
        lista = printoutstuff.split()
        messageBox.config(state=NORMAL)
        messageBox.insert(END, "Running " + " ".join(lista[:3]) + "...\n")
        messageBox.config(state=NORMAL)
        '''
        child = subprocess.run(lista, stderr = subprocess.PIPE)
        communicate(child)
        ###
        rc = child.returncode
        if rc != 0:
            logfile = open("log.file","w")
            logfile.write(child.stderr.decode("utf-8"))
            logfile.close()
            print(" ".join(lista[0:3]),"ended in an error. For more information check log.file")
            return
        '''
    print("\n\n")


# Move up
def up():
    current = tree.selection()
    if current:
        tree.move(current, tree.parent(current),tree.index(current)-1)
# Move down
def down():
    current = tree.selection()
    if current:
        tree.move(current, tree.parent(current),tree.index(current)+1)

# Delete selected
def delete():
    current = tree.selection()
    if current:
        tree.delete(current)

# Delete all
def deleteAll():
    tree.delete(*tree.get_children())

# Save pipeline to file
def saveTree():
    saveFile = filedialog.asksaveasfile(mode = 'w', defaultextension = ".txt")
    if saveFile is None:
        return
    mainBranches = tree.get_children()
    marker = False
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

# Open pipeline from file
def openTree():
    completeName = filedialog.askopenfilenames(initialdir = './', title = "Select file", filetypes = (("all files","*.*"),("txt files","*.txt")))
    if completeName == '':
        return
    try:
        fileTree = open(completeName[0], 'r')
    except IndexError:
        return
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

## Container for pipeline window control buttons
controlFrame = Frame(master = mmFrame)
controlFrame.config(background = "red")
controlFrame.grid(row = 0, column = 1)

showMeContentForTree = Button(master = controlFrame, text = "Add last command to pipeline", command = handleCommand)
showMeContentForTree.grid(row = 1, column = 1, columnspan = 2, sticky = 'nesw')

sPC_Value = IntVar() # Interger value for startingPointCheck
startingPointCheck = Checkbutton(master = controlFrame, text = "Start from selected", variable = sPC_Value, onvalue=1, offvalue = 0, width = 15)
startingPointCheck.grid(row = 2, column = 2, sticky = 'nesw')

runButton = Button(master = controlFrame, text = "Run", command = runTree, width = 15)
runButton.grid(row = 2, column = 1, sticky = 'nesw')

upButton = Button(master = controlFrame, text = "Move up", command = up, width = 15)
upButton.grid(row = 3, column = 1, sticky = 'nesw')

downButton = Button(master = controlFrame, text = "Move down", command = down, width = 15)
downButton.grid(row = 3, column = 2, sticky = 'nesw')

delButton = Button(master = controlFrame, text = "Delete", command = delete, width = 15)
delButton.grid(row = 4, column = 1, sticky = 'nesw')

delAllButton = Button(master = controlFrame, text = "Delete all", command = deleteAll, width = 15)
delAllButton.grid(row = 4, column = 2, sticky = 'nesw')

saveButton = Button(master = controlFrame, text = "Save", command = saveTree, width = 15)
saveButton.grid(row = 5, column = 1, sticky = 'nesw')

openPipeButton = Button(master = controlFrame, text = "Open", command = openTree, width = 15)
openPipeButton.grid(row = 5, column = 2, sticky = 'nesw')
### End of pipeline section ###

### Message box ###
# Text box for messages
messageBox = Text(master = mmFrame, height = 15)
messageBox.grid(row = 1, column = 0, columnspan = 2)
messageBox.config(state = DISABLED)

# Fonts for messages
messageBox.tag_config("error", foreground = "red")
messageBox.tag_config("success", foreground = "green")

# Scrollbar for messageBox
messageBoxScrollbar = ttk.Scrollbar(master = mmFrame, command = messageBox.yview)
messageBoxScrollbar.grid(row = 1, column = 1, sticky = N + S + E)
messageBox['yscrollcommand'] = messageBoxScrollbar.set

### End of message box section ###

root.mainloop()