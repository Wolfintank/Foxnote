import tkinter
import tkinter.filedialog as FD
import tkinter.simpledialog as SD
import os

CurrentNoteID = 0
TabButtons = []
Tabs = []
Files = [None]

def SwitchToTab(TabID):
    global CurrentNoteID
    TabButtons[CurrentNoteID]["relief"] = "raised"
    Tabs[CurrentNoteID].pack_forget()
    CurrentNoteID = TabID
    TabButtons[CurrentNoteID]["relief"] = "sunken"
    Tabs[CurrentNoteID].pack()

def CreateEmptyTab():
    NewTabID = len(TabButtons)
    TabButton = tkinter.Button(TabListFRM,text=f"New ({NewTabID})",command=lambda: SwitchToTab(NewTabID))
    TabButton.grid(row=0,column=NewTabID)
    TabButtons.append(TabButton)

    Tab = tkinter.Text(TabContentFRM,width=50)
    Tabs.append(Tab)

    Files.append(None)
    SwitchToTab(NewTabID)

def LoadFile():
    NewTabID = len(TabButtons)
    Loadpath = FD.askopenfilename(initialdir='/',filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')],title="Open")

    TabButton = tkinter.Button(TabListFRM,text=os.path.basename(Loadpath).replace(".txt",""),command=lambda: SwitchToTab(NewTabID))
    TabButton.grid(row=0,column=NewTabID)
    TabButtons.append(TabButton)

    Tab = tkinter.Text(TabContentFRM,width=50)
    Tab.insert("1.0", open(Loadpath).read())
    Tabs.append(Tab)

    Files.append(Loadpath)
    SwitchToTab(NewTabID)


def CloseTab():
    global CurrentNoteID
    if(CurrentNoteID != 0):
        TabToDelete = CurrentNoteID
        SwitchToTab(0)
        Tabs[TabToDelete].destroy()
        TabButtons[TabToDelete].destroy()

def RenameTab():
    global CurrentNoteID
    if(CurrentNoteID != 0):
        TID = CurrentNoteID
        OldName = TabButtons[TID]["text"]
        NewName = SD.askstring(title=f"Rename ${OldName} to:", prompt="File Name")

        if(NewName == "" or NewName == " " or NewName == None or NewName == OldName):
            return
        
        if(Files[TID] != None):
            Files[TID] = Files[TID].replace(OldName,NewName)

        TabButtons[TID]["text"] = NewName

def DuplicateTab():
    global CurrentNoteID
    if(CurrentNoteID != 0):
        TID = CurrentNoteID
        NewTabID = len(TabButtons)
        TabButton = tkinter.Button(TabListFRM,text=TabButtons[TID]["text"] + " Copy",command=lambda: SwitchToTab(NewTabID))
        TabButton.grid(row=0,column=NewTabID)
        TabButtons.append(TabButton)

        Tab = tkinter.Text(TabContentFRM,width=50)
        Tab.insert("1.0",Tabs[TID].get("1.0","end"))
        Tabs.append(Tab)

        Files.append(None)
        SwitchToTab(NewTabID)

def SaveFile():
    global CurrentNoteID
    if(CurrentNoteID != 0):
        TID = CurrentNoteID
        if(Files[TID] != None):
            Savepath = Files[TID]
            File = open(Savepath, "w")
            File.write(Tabs[TID].get("1.0","end"))
            File.close()
        else:
            SaveFileAs()

def SaveFileAs():
    global CurrentNoteID
    if(CurrentNoteID != 0):
        TID = CurrentNoteID
        Savepath = FD.asksaveasfilename(initialdir='/',filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')],defaultextension='.txt',confirmoverwrite=True,title="Save as",initialfile=TabButtons[TID]["text"])
        File = open(Savepath, "w")
        File.write(Tabs[TID].get("1.0","end"))
        File.close()
        FileName = os.path.basename(Savepath)
        FileName = FileName.replace(".txt","")
        TabButtons[TID]["text"] = FileName
        Files[TID] = Savepath
        
    

#Main Window Creation
MainWindow = tkinter.Tk(className="foxnote")
MenuListFRM = tkinter.Frame(MainWindow)
MenuListFRM.pack()
TabListFRM = tkinter.Frame(MainWindow)
TabListFRM.pack()
TabContentFRM = tkinter.Frame(MainWindow)
TabContentFRM.pack()

#OptionsButton
FileOptions = tkinter.Menubutton(MenuListFRM,text="File")
NEWMENU = tkinter.Menu(FileOptions,tearoff=0)
NEWMENU.add_command(label="Create Empty",command=CreateEmptyTab)
NEWMENU.add_command(label="Load File",command=LoadFile)
FileOptions["menu"] = NEWMENU
FileOptions.grid(row=0,column=0)

TabOptions = tkinter.Menubutton(MenuListFRM,text="Tab")
TABMENU = tkinter.Menu(TabOptions,tearoff=0)
TABMENU.add_command(label="Close", command=CloseTab)
TABMENU.add_command(label="Rename", command=RenameTab)
TABMENU.add_command(label="Duplicate", command=DuplicateTab)
TabOptions["menu"] = TABMENU
TabOptions.grid(row=0,column=1)

SaveOptions = tkinter.Menubutton(MenuListFRM,text="Save")
SAVEMENU = tkinter.Menu(SaveOptions,tearoff=0)
SAVEMENU.add_command(label="Save",command=SaveFile)
SAVEMENU.add_command(label="Save as",command=SaveFileAs)
SaveOptions["menu"] = SAVEMENU
SaveOptions.grid(row=0,column=2)

#Home Tab
HomeTabBtn = tkinter.Button(TabListFRM,text="Home",relief="sunken",command=lambda: SwitchToTab(0))
HomeTabBtn.grid(row=0,column=0)
TabButtons.append(HomeTabBtn)
HomeMenu = tkinter.Frame(TabContentFRM, width=50)
Home_Label = tkinter.Label(HomeMenu,text="Create or Load a File to edit")
Home_Label.grid(row=0,column=1)
Home_New_Btn = tkinter.Button(HomeMenu,text="Create New",command=CreateEmptyTab)
Home_New_Btn.grid(row=2,column=1)
Home_Load_Btn = tkinter.Button(HomeMenu,text="Open File",command=LoadFile)
Home_Load_Btn.grid(row=4,column=1)
Tabs.append(HomeMenu)
HomeMenu.pack()

MainWindow.mainloop()


