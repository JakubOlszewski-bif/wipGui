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

# Create popup window with command
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

# Main Menu 
root = Tk()
root.title("Main Menu")
root.geometry("500x400")
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

### Pipeline section ###

# TreeView set-up
tree = ttk.Treeview(root, columns = ("Stuff"))
tree.heading("#0", text = "Command")
tree.heading("#1", text = "Content")
tree.pack() 

# Add last command to tree
def addCommandToTree(key,reqWidgets,optWidgets):
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

showMeContentForTree = Button(master = root, text = "Add last command to pipeline", command = handleCommand)
showMeContentForTree.pack()

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

# Run pipeline in bash
def runTree():
    """Function for "Run pipeline" button in the pipeline widget. Pull all functions and parameters in the tree and passes them to bash.
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
        '''
        if rc != 0:
            return
        lista = printoutstuff.split()
        child = subprocess.run(lista, stderr = subprocess.Pipe)
        rc = child.returncode
        
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


## Container for pipeline window control buttons
controlFrame = Frame(master = root)
controlFrame.pack()

sPC_Value = IntVar() # Interger value for startingPointCheck
startingPointCheck = Checkbutton(master = controlFrame, text = "Start from selected", variable = sPC_Value, onvalue=1, offvalue = 0)
startingPointCheck.grid(row = 1, column = 2)
runButton = Button(master = controlFrame, text = "Run", command = runTree)
runButton.grid(row = 1, column = 1)

upButton = Button(master = controlFrame, text = "Move up", command = up)
upButton.grid(row = 2, column = 1,sticky = E)

downButton = Button(master = controlFrame, text = "Move down", command = down)
downButton.grid(row = 2, column = 2, sticky = W)


# Save pipeline to file
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

openPipeButton = Button(master = root, text = "Open", command = openTree)
openPipeButton.pack()
### End of pipeline section ###

root.mainloop()