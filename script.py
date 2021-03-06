import sys, os, requests, tkinter, binascii, csv, random, gc, subprocess, time, math
from multiprocessing import Queue
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
from pathlib import Path
GUI = tkinter.Tk()
DiceExchangeWindow = tkinter.Toplevel()
DiceExchangeWindow.withdraw()
DieImages = {
    0:tkinter.PhotoImage(file=(r'Images\dice.png')),
    1:tkinter.PhotoImage(file=(r'Images\dice1.png')),
    2:tkinter.PhotoImage(file=(r'Images\dice2.png')),
    3:tkinter.PhotoImage(file=(r'Images\dice3.png')),
    4:tkinter.PhotoImage(file=(r'Images\dice4.png')),
    5:tkinter.PhotoImage(file=(r'Images\dice5.png')),
    6:tkinter.PhotoImage(file=(r'Images\dice6.png'))
}
Templates = {
1:"Templates/base.pk7",
2:"Templates/Newoutput.pk7",
3:"Templates/outfile.pk7",
4:"Templates/outfile2.pk7",
}
serveLegalityLog = open('serveLegality-CLI/serveLegality/serveLegality/binaries/Debug/log.txt', "w")
serveLegalityLog.write("")
serveLegalityLog.close()

FrameList = []
##DiceFrameList = {}
##FrameList2 = []
currentusernum = 0
DiceEffect = tkinter.StringVar()
DiceEffect.set("as")
Effects = ["N/a",["Evolve","Devolve","Reroll","Curse Reroll","Trade","Nothing","Evolve All","Choose that Pokemon","Sabotage","Choose your Fate"],[13,13,13,13,13,13,9,9,3,1]]
SeekLocations = {
    "EncryptConst":     0,
    "Sanity":           4,
    "PokemonNDexID":    8,
    "HeldItem":         10,
    "TID":              12,
    "SID":              14,
    "XP":               16,
    "Ability":          20,
    "AbilityNum":       21,
    "MarkValue":        22,
    "PID":              24,
    "Nature":           28,
    "FaithGendAlt":     29,
    "HPEV":             30,
    "ATKEV":            31,
    "DEFEV":            32,
    "SPEEV":            33,
    "SPAEV":            34,
    "SPDEV":            35,
    "NickNameL1":       64,
    "NickNameL2":       66,
    "NickNameL3":       68,
    "NickNameL4":       70,
    "NickNameL5":       72,
    "NickNameL6":       74,
    "NickNameL7":       76,
    "NickNameL8":       78,
    "NickNameL9":       80,
    "NickNameL10":      82,
    "NickNameL11":      84,
    "NickNameL12":      86,
    "Move1":            90,
    "Move2":            92,
    "Move3":            94,
    "Move4":            96,
    "Move1PP":          98,
    "Move2PP":          99,
    "Move3PP":          100,
    "Move4PP":          101,
    "NickNameBool":     119,
    "Country":          224,
    "ConsoleRegion":    226,
}

with open(r'pokedex\pokedex\data\csv\pokemon.csv', mode='r') as infile:
    reader = csv.reader(infile)
    mydict = {rows[0]:rows[1] for rows in reader}
with open(r'pokedex\pokedex\data\csv\pokemon.csv', mode='r') as infile:
    reader = csv.reader(infile)
    isdefault = {rows[0]:rows[7] for rows in reader}
with open(r'pokedex\pokedex\data\csv\pokemon.csv', mode='r') as infile:
    reader = csv.reader(infile)
    speicies = {rows[0]:rows[2] for rows in reader}
with open(r'pokedex\pokedex\data\csv\pokemon_forms.csv', mode='r') as infile:
    reader = csv.reader(infile)
    FormPK = {}
    for rows in reader:
        FormPK[rows[3]] = [rows[6],rows[7],rows[8]]
with open(r'pokedex\pokedex\data\csv\pokemon_species.csv', mode='r') as infile:
    reader = csv.reader(infile)
    Evolutions = {rows[0]:rows[3] for rows in reader}

class userGUI:
    def __init__(self,UserNum,USERDGUI,isdefault):
        self.NumberUser = UserNum
        self.USERDGUI = USERDGUI
        if UserNum % 2 == 0:
            self.x = 2
            self.y = UserNum / 2
            self.y -= 1
        else:
            self.x = 1
            self.y = UserNum - 1
            self.y = self.y / 2
        self.userframe = tkinter.Frame(self.USERDGUI,bd=3,relief="sunken",padx=3,pady=3)
        self.userframe.grid(column = int(self.x), row = int(self.y))
        FrameList.append(self.userframe)
        self.userLable = tkinter.Label(self.userframe, text = "user"+str(UserNum))
        self.userLable.grid()
        self.NewNotebook = Notebook(self.userframe)
        self.NewNotebook.grid()
        self.PokeNumber = tkinter.StringVar()
        self.PokeNumber.set("# to gen")
        self.genpoke = tkinter.Button(self.userframe, text = 'Generate pokemon', width = 16,command = lambda pickpokemon = self.pickpokemon, PokeNumber = self.PokeNumber: pickpokemon(int(PokeNumber.get())))
        self.genpoke.grid(column = 0, row=98)
        self.PokeNum = tkinter.Entry(self.userframe, textvariable=self.PokeNumber)
        self.PokeNum.grid(column = 0, row=99)
        self.truepokenum = 0
        self.genfilesandsendto3ds = tkinter.Button(self.userframe, text="Sendto3ds",width = 16, command = lambda:self.compileto3ds(self.truepokenum))
        self.genfilesandsendto3ds.grid(row=100)
        self.dsipadd = tkinter.StringVar()
        self.dsipadd.set("IP ADDRESS")
        self.dsipaddent = tkinter.Entry(self.userframe, textvariable=self.dsipadd)
        self.dsipaddent.grid(column = 0, row=101)
        self.pokenum = []
        self.pokepids = []
        self.poketids = []
        self.pokesids = []
        self.tabnum = []
        self.pokemomids = {}
        self.pokemomPIDs = {}
        self.pokemomTIDs = {}
        self.pokemomSIDs = {}
        self.GenderFormFath = 0
        self.PokeImage1 = {}
        self.genderbools = []
        self.gendercheck=[]
        self.PokeImage = {}
        self.IPFAIL = 0


    def compileto3ds(self, number):
        self.IPFAIL = 0
        self.number = number
        for count in range(self.number):
            if str(isdefault.get(str(self.pokemomids.get(count)))) == '1':
                self.replacehex('PokemonNDexID',self.flipthehexorder(self.turninttohex(self.pokemomids.get(count),4)))
            else:
                self.replacehex('PokemonNDexID',self.flipthehexorder(self.turninttohex(int(speicies.get(str(self.pokemomids.get(count)))),4)))
                if str(FormPK.get(str(self.pokemomids.get(count)))[0]) == "0":
                    self.GenderFormFath += 8*int(FormPK.get(str(self.pokemomids.get(count)))[2])
            self.replacehex('PID',self.flipthehexorder(self.turninttohex(self.pokemomPIDs.get(count),8)))
            self.replacehex('TID',self.flipthehexorder(self.turninttohex(self.pokemomTIDs.get(count),4)))
            self.replacehex('SID',self.flipthehexorder(self.turninttohex(self.pokemomSIDs.get(count),4)))
            self.GenderFormFath += (self.genderbools[count].get()*2)
            self.replacehex('FaithGendAlt',self.flipthehexorder(self.turninttohex(self.GenderFormFath,2)))
            self.sendfilesto3ds(self.pokenum[count])
            self.GenderFormFath = 0

    def turninttohex(self,numbers,width):
        self.numbers = numbers
        self.curent = str(hex(self.numbers)[2:])
        if len(self.curent) == width:
            return self.curent
        else:
            self.curent = self.curent.zfill(width)
            return self.curent

#https://stackoverflow.com/questions/45415347/generate-random-integer-between-two-ranges
    def random_of_ranges(self,*ranges):
        self.all_ranges = sum(ranges, [])
        return random.choice(self.all_ranges)


    def flipthehexorder(self,hexes):
        self.hexes = hexes
        self.hexlist = []
        self.runnum = 0
        self.runnum2 = 0
        for nibbles in range(1+int(len(self.hexes)/2)):
            if nibbles == 0:
                pass
            else:
                self.runnum += 1
                if (self.runnum2*2) == 0:
                    self.hexlist.append(self.hexes[len(self.hexes)-(self.runnum*2):])
                else:
                    self.hexlist.append(self.hexes[len(self.hexes)-(self.runnum*2):-(self.runnum2*2)])
                self.runnum2 += 1
        return ''.join(map(str, self.hexlist))

    def replacehex(self,whattochange,hexvalues):
        with open(Templates.get(2), 'rb') as f:
            content = f.read()
            f.close()
        g = open(Templates.get(2),'wb')
        g.write(content)
        g.seek(SeekLocations.get(whattochange))
        hex_data=bytearray.fromhex(hexvalues)
        g.write(hex_data)
        g.close()

    def resetdicts(self):
        self.pokemomids = {}
        for tabsdel in self.tabnum:
            tabsdel.destroy()
        self.tabnum = []
        self.truepokenum = 0
        self.pokemomPIDs = {}
        self.pokemomTIDs = {}
        self.pokemomSIDs = {}
        self.PIDFRAME = []
        self.TIDFRAME = []
        self.SIDFRAME = []
        self.PokeIDFrame = []
        self.PokeImage1 = {}
        self.PokeImage = {}
        self.genderbools = []
        self.gendercheck=[]


    def ReRollIDs(self,counts,varr,types):
        if types == "PID":
            self.pokemomPIDs[counts] = random.randrange(0,4294967295)
            varr.set("PID: "+str(self.pokemomPIDs[counts]))
        elif types == "TID":
            self.pokemomTIDs[counts] = random.randrange(0,65535)
            varr.set("TID: "+str(self.pokemomTIDs[counts]))
        elif types == "SID":
            self.pokemomSIDs[counts] = random.randrange(0,65535)
            varr.set("SID: "+str(self.pokemomSIDs[counts]))

    def CheckPicGender(self,counts):
        if self.genderbools[counts].get() == 0:
            filedirpng = Path(r"sprites\\sprites\\pokemon\\"+str(speicies.get(str(self.pokemomids.get(counts))))+".png")
            self.PokeImage1[counts]=tkinter.PhotoImage(file=filedirpng)

        else:
            filedirpng = Path(r"sprites\\sprites\\pokemon\\female\\"+str(speicies.get(str(self.pokemomids.get(counts))))+".png")
            if filedirpng.is_file():
                self.PokeImage1[counts]=tkinter.PhotoImage(file=filedirpng)
        self.PokeImage[counts].configure(image=self.PokeImage1[counts])



    def pickpokemon(self,number):
        self.resetdicts()
        self.number = number
        for counts in range(self.number):
            self.genderbools.append(tkinter.IntVar(value=0))
            self.pokenum.append(tkinter.StringVar())
            self.pokepids.append(tkinter.StringVar())
            self.poketids.append(tkinter.StringVar())
            self.pokesids.append(tkinter.StringVar())
            self.tabnum.append(tkinter.Frame(self.NewNotebook))
            self.PokeIDFrame.append(tkinter.Frame(self.tabnum[counts]))
            self.PokeIDFrame[counts].grid()
            self.PIDFRAME.append(tkinter.Frame(self.tabnum[counts]))
            self.PIDFRAME[counts].grid()
            self.TIDFRAME.append(tkinter.Frame(self.tabnum[counts]))
            self.TIDFRAME[counts].grid()
            self.SIDFRAME.append(tkinter.Frame(self.tabnum[counts]))
            self.SIDFRAME[counts].grid()
            self.NewNotebook.add(self.tabnum[counts],text="Pokemon"+str(counts+1))
            self.pokemonlable = tkinter.Label(self.PokeIDFrame[counts],textvariable=self.pokenum[counts])
            self.pokemonlable.grid(row=0,column=0)
            self.pokemonnum = 0+self.random_of_ranges(list(range(1, 803)), list(range(10001, 10147)))
            self.pokemomids[counts] = self.pokemonnum
            self.pokemomPIDs[counts] = random.randrange(0,4294967295)
            self.pokemomTIDs[counts] = random.randrange(0,65535)
            self.pokemomSIDs[counts] = random.randrange(0,65535)
            self.pokemonpid = tkinter.Label(self.PIDFRAME[counts],textvariable=self.pokepids[counts])
            self.pokemonpid.grid(row=0,column=1)
            self.pokemontid = tkinter.Entry(self.TIDFRAME[counts],textvariable=self.poketids[counts])
            self.pokemontid.grid(row=0,column=1)
            self.pokemonsid = tkinter.Entry(self.SIDFRAME[counts],textvariable=self.pokesids[counts])
            self.pokemonsid.grid(row=0,column=1)
            if str(FormPK.get(str(self.pokemonnum))[0]) == "0":
                self.pokenum[counts].set(mydict.get(str(self.pokemonnum)).title())
            else:
                self.pokenum[counts].set(mydict.get(str(speicies.get(str(self.pokemonnum)))).title())
            self.pokepids[counts].set("PID: "+str(self.pokemomPIDs[counts]))
            self.poketids[counts].set("TID: "+str(self.pokemomTIDs[counts]))
            self.pokesids[counts].set("SID: "+str(self.pokemomSIDs[counts]))
            self.pokemonpidRoll = tkinter.Button(self.PIDFRAME[counts],text="ReRoll", command = lambda counts=counts, pokepids=self.pokepids[counts]:self.ReRollIDs(counts,pokepids,"PID"))
            self.pokemonpidRoll.grid(row=0,column=2)
            self.pokemontidRoll = tkinter.Button(self.TIDFRAME[counts],text="ReRoll", command = lambda counts=counts, poketids=self.poketids[counts]:self.ReRollIDs(counts,poketids,"TID"))
            self.pokemontidRoll.grid(row=0,column=2)
            self.pokemonsidRoll = tkinter.Button(self.SIDFRAME[counts],text="ReRoll", command = lambda counts=counts, pokesids=self.pokesids[counts]:self.ReRollIDs(counts,pokesids,"SID"))
            self.pokemonsidRoll.grid(row=0,column=2)
            self.gendercheck.append(tkinter.Checkbutton(self.PIDFRAME[counts],text="Feamle?",variable=self.genderbools[counts],command=lambda counts=counts:self.CheckPicGender(counts)))
            self.gendercheck[counts].grid(row=0,column=3)
            if str(isdefault.get(str(self.pokemonnum))) == '1':
                self.PokeImage1[counts] = tkinter.PhotoImage(file=(r"sprites\\sprites\\pokemon\\"+str(self.pokemonnum)+".png"))
                self.PokeImage[counts] = Label(self.PIDFRAME[counts],image=self.PokeImage1[counts])
            else:
                self.PokeImage1[counts] = tkinter.PhotoImage(file=(r"sprites\\sprites\\pokemon\\"+str(speicies.get(str(self.pokemonnum)))+".png"))
                self.PokeImage[counts] = Label(self.PIDFRAME[counts],image=self.PokeImage1[counts])
            self.PokeImage[counts].grid(row=0,column=4)
        self.truepokenum = number



    def sendfilesto3ds(self,pokemonname):
##        messagebox.showerror("Error", "Repet message")
        if self.IPFAIL == 0:
            with open(Templates.get(2), "rb") as old, open(Templates.get(3), "wb") as new:
                new.write(str.encode(r'PKSMOTA'))
                new.write(binascii.unhexlify('07'))
                new.write(old.read())
                new.close()
            #https://stackoverflow.com/a/7006424
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            serveLegalityLog = open('serveLegality-CLI/serveLegality/serveLegality/binaries/Debug/log.txt', "a")
            try:
                serveLegality = subprocess.check_output(['serveLegality-CLI/serveLegality/serveLegality/binaries/Debug/serveLegality.exe',Templates.get(3),Templates.get(4)],startupinfo=si)
                serveLegalityLog.write(serveLegality.decode(errors="ignore"))
            except UnicodeDecodeError as lmao:
                print('fugn')
            serveLegalityLog.close()
            while True:
                try:
                    with open(Templates.get(4), 'rb') as f: r = requests.post('http://'+self.dsipadd.get()+':9000', files={Templates.get(4): f}, timeout=5)
                except requests.exceptions.ConnectionError as errs:
                    if "Max retries exceeded with url" in str(errs):
                        messagebox.showerror('ERROR','Unable to connect to 3DS\nRestart PKSM?\nWrong IP?')
                        self.IPFAIL = 1
                        break
                    elif "Remote end closed connection without response" in str(errs):
                        break
                    elif "An existing connection was forcibly closed by the remote host" in str(errs):
##                        self.Retry = messagebox.askyesno("Question", "Did "+pokemonname.get()+" Send?")
##                        if self.Retry == True:
##                            messagebox.showerror("Error", "Yes message")
##                            break
##                        else:
##                            messagebox.showerror("Error", "No message")
                        Errorisgus = "TRU"
        else:
            pass

##def RollDiceFunc(DiceWink,ChanceFrame):
##    Rand = random.randint(1,6)
##    DiceWink.configure(image=DieImages[Rand])
##    if DiceEffect.get() == "as":
##        YourEffect = tkinter.Button(ChanceFrame, textvariable=DiceEffect, command=lambda:RandomEvent())
##        YourEffect.grid(row=2)
##    DiceEffect.set(Effects[Rand])
RollDiceFuncItems = {"MainFrames":[],"HowManyEventsEntry":[],"HowManyEventsIntVar":[],"ComBoBoxes":[],"EventComboAndentryFrame":[],"OptionMenuVar":[],"PercentLable":[],"PercentENTRY":[],"PercentVAR":[]}
DiceExchangeWindow.protocol("WM_DELETE_WINDOW", lambda:ResetDicewindow())
def ResetDicewindow():
    DiceExchangeWindow.withdraw()
    DeleteDiceItems()

def SetDefaultPercent(Outpt, Inpt, Default="No"):
    if Default == "No":
        Outpt.set(Effects[2][int(str([str([i for i,x in enumerate(Effects[1]) if x == Inpt])[1:-1]])[2:-2])])


def DeleteDiceItems():
    global RollDiceFuncItems
    for items in RollDiceFuncItems["EventComboAndentryFrame"]:
        items.destroy()
    for items in RollDiceFuncItems["MainFrames"]:
        items.destroy()
    RollDiceFuncItems = {"MainFrames":[],"HowManyEventsEntry":[],"HowManyEventsIntVar":[],"ComBoBoxes":[],"EventComboAndentryFrame":[],"OptionMenuVar":[],"PercentLable":[],"PercentENTRY":[],"PercentVAR":[],"NoteTab":[],"NoteTabItems":[]}

def GenerateRollFunction(Default="No"):
    global RollDiceFuncItems
    if Default == "Yes":
        RollDiceFuncItems["HowManyEventsIntVar"][0].set(10)
    RollDiceFuncItems["ComBoBoxes"] = []
    for items in RollDiceFuncItems["EventComboAndentryFrame"]:
            items.destroy()
    RollDiceFuncItems["EventComboAndentryFrame"] = []
    RollDiceFuncItems["OptionMenuVar"] = []
    RollDiceFuncItems["PercentLable"] = []
    RollDiceFuncItems["PercentENTRY"] = []
    RollDiceFuncItems["PercentVAR"] = []
    for items in range(RollDiceFuncItems["HowManyEventsIntVar"][0].get()):
        RollDiceFuncItems["EventComboAndentryFrame"].append(tkinter.Frame(RollDiceFuncItems["MainFrames"][1],bd=5,relief=tkinter.RAISED))
        if items < 3:
            if items == 0:
                RollDiceFuncItems["EventComboAndentryFrame"][items].grid(row=0,column=items)
            elif items == 1:
                RollDiceFuncItems["EventComboAndentryFrame"][items].grid(row=0,column=items)
            elif items == 2:
                RollDiceFuncItems["EventComboAndentryFrame"][items].grid(row=0,column=items)
        elif 6 > items >= 3:
            RollDiceFuncItems["EventComboAndentryFrame"][items].grid(row=1,column=round(items-3))
        elif 9 > items >= 6:
            RollDiceFuncItems["EventComboAndentryFrame"][items].grid(row=2,column=round(items-6))
        elif 10 > items >= 9:
            RollDiceFuncItems["EventComboAndentryFrame"][items].grid(row=3,column=round(items-9))
        RollDiceFuncItems["OptionMenuVar"].append(tkinter.StringVar())
        if Default=="No":
            RollDiceFuncItems["OptionMenuVar"][items].set("Event")
        elif Default=="Yes":
            RollDiceFuncItems["OptionMenuVar"][items].set(Effects[1][items])
        RollDiceFuncItems["PercentLable"].append(tkinter.Label(RollDiceFuncItems["EventComboAndentryFrame"][items], text="%:"))
        RollDiceFuncItems["PercentLable"][items].grid(row=0,column=1)
        RollDiceFuncItems["PercentVAR"].append(tkinter.StringVar())
        RollDiceFuncItems["PercentENTRY"].append(tkinter.Entry(RollDiceFuncItems["EventComboAndentryFrame"][items], textvariable=RollDiceFuncItems["PercentVAR"][items]))
        RollDiceFuncItems["PercentENTRY"][items].grid(row=0,column=2)
        RollDiceFuncItems["ComBoBoxes"].append(tkinter.OptionMenu(RollDiceFuncItems["EventComboAndentryFrame"][items],RollDiceFuncItems["OptionMenuVar"][items],*Effects[1], command= lambda inpt=RollDiceFuncItems["OptionMenuVar"][items], items=items:SetDefaultPercent(RollDiceFuncItems["PercentVAR"][items],inpt)))
        if Default == "Yes":
            RollDiceFuncItems["PercentVAR"][items].set(Effects[2][items])
        RollDiceFuncItems["ComBoBoxes"][items].grid(row=0,column=0)

def RollStuff():
    global RollDiceFuncItems, currentusernum
    for items in RollDiceFuncItems["NoteTabItems"]:
        items.destroy()
    RollDiceFuncItems["NoteTabItems"] = []
    TotalPercent = []
    ButtonEvent = []
    for itms in RollDiceFuncItems["PercentVAR"]:
        try:
            TotalPercent.append(int(itms.get()))
        except:
            TotalPercent.append(int(0))
    for users in range(currentusernum):
        RollDiceFuncItems["NoteTab"].append(tkinter.Frame(RollDiceFuncItems["HowManyEventsEntry"][4]))
        RollDiceFuncItems["HowManyEventsEntry"][4].add(RollDiceFuncItems["NoteTab"][users],text="User"+str(users+1))
        ButtonEvent.append(ReturnDice())
        RollDiceFuncItems["NoteTabItems"].append(tkinter.Button(RollDiceFuncItems["NoteTab"][users],text=ButtonEvent[users], command=lambda:DoEvent(ButtonEvent[users])))
        RollDiceFuncItems["NoteTabItems"][users].grid()

def ButtonEvent(Event):
    pass

def ReturnDice():
    RangeOfNum = []
    for items in range(len(RollDiceFuncItems["OptionMenuVar"])):
        if items > 9:
            pass
        else:
            for count in range(int(RollDiceFuncItems["PercentVAR"][items].get())):
                RangeOfNum.append(RollDiceFuncItems["OptionMenuVar"][items].get())
    return RangeOfNum[random.randrange(len(RangeOfNum))]


def RollDiceFunc():
    global RollDiceFuncItems
    DeleteDiceItems()
    DiceExchangeWindow.deiconify()
    RollDiceFuncItems["MainFrames"].append(tkinter.Frame(DiceExchangeWindow,bd=5,relief=tkinter.RAISED))
    RollDiceFuncItems["MainFrames"][0].grid(row=0,column=0)
    RollDiceFuncItems["MainFrames"].append(tkinter.Frame(DiceExchangeWindow,bd=5,relief=tkinter.SUNKEN))
    RollDiceFuncItems["MainFrames"][1].grid(row=1,column=0)
    RollDiceFuncItems["MainFrames"].append(tkinter.Frame(DiceExchangeWindow,bd=5,relief=tkinter.SUNKEN))
    RollDiceFuncItems["MainFrames"][2].grid(row=2,column=0)
    RollDiceFuncItems["MainFrames"].append(tkinter.Frame(DiceExchangeWindow,bd=5,relief=tkinter.SUNKEN))
    RollDiceFuncItems["MainFrames"][3].grid(row=3,column=0)
    RollDiceFuncItems["HowManyEventsEntry"].append(tkinter.Label(RollDiceFuncItems["MainFrames"][0], text="How Many Options?"))
    RollDiceFuncItems["HowManyEventsEntry"][0].grid(row=0,column=0)
    RollDiceFuncItems["HowManyEventsIntVar"].append(tkinter.IntVar())
    RollDiceFuncItems["HowManyEventsEntry"].append(tkinter.Entry(RollDiceFuncItems["MainFrames"][0], textvariable=RollDiceFuncItems["HowManyEventsIntVar"][0]))
    RollDiceFuncItems["HowManyEventsEntry"][1].grid(row=0,column=1)
    RollDiceFuncItems["HowManyEventsEntry"].append(tkinter.Button(RollDiceFuncItems["MainFrames"][0], text="Set", command=lambda: GenerateRollFunction()))
    RollDiceFuncItems["HowManyEventsEntry"][2].grid(row=0,column=2)
    RollDiceFuncItems["HowManyEventsEntry"].append(tkinter.Button(RollDiceFuncItems["MainFrames"][2], text="Roll", command=lambda: RollStuff()))
    RollDiceFuncItems["HowManyEventsEntry"][3].grid(row=0,column=0)
    RollDiceFuncItems["HowManyEventsEntry"].append(Notebook(RollDiceFuncItems["MainFrames"][3]))
    RollDiceFuncItems["HowManyEventsEntry"][4].grid(row=0,column=0)
    RollDiceFuncItems["HowManyEventsEntry"].append(tkinter.Button(RollDiceFuncItems["MainFrames"][0], text="Default", command=lambda: GenerateRollFunction(Default="Yes")))
    RollDiceFuncItems["HowManyEventsEntry"][5].grid(row=0,column=3)




##def resetdiceexchange(Framee):
##    Framee.destroy()
##    DiceExchangeWindow.withdraw()
##    for item in FrameList2:
##        item.destroy()

##def RandomEvent():
##    global whateverthisis
##    try:
##        whateverthisis.destroy()
##    except:
##        sdfdsf=3
##    DiceFrameList = {}
##    DiceExchangeWindow.deiconify()
##    DiceExchangeFrame = tkinter.Frame(DiceExchangeWindow)
##    whateverthisis = DiceExchangeFrame
##    DiceExchangeFrame.grid()
##    Canclebutton = tkinter.Button(DiceExchangeFrame,text="Cancel",command=lambda Framee=DiceExchangeFrame:resetdiceexchange(Framee))
##    Canclebutton.grid(row=99)
##    for obj in gc.get_objects():
##        if isinstance(obj, userGUI):
##            DiceFrameList[obj] = tkinter.Frame(DiceExchangeFrame, bd=1, relief=tkinter.RAISED,width=500,height=50)
##            UserLable = tkinter.Label(DiceFrameList[obj],text="User "+str(obj.NumberUser))
##            if obj.NumberUser % 2 == 0:
##                DiceFrameList[obj].grid(row=int((obj.NumberUser/2)-1),column=1)
##            else:
##                DiceFrameList[obj].grid(row=int((obj.NumberUser-1)/2),column=0)
##            UserLable.grid()
##            for items in obj.pokenum:
##                Pokebutton = tkinter.Button(DiceFrameList[obj],textvariable=items,width=15)
##                Pokebutton.grid()
##                FrameList2.append(Pokebutton)
##
##    DiceExchangeWindow.protocol("WM_DELETE_WINDOW", lambda Framee=DiceExchangeFrame:resetdiceexchange(Framee))



def AddUsers(Number,frame):
    if Number <= 10:
        try:
            USERFRAME.destroy()
        except:
            ChanceFrame = tkinter.Frame(frame)
            ChanceFrame.grid(row=99,column=1)
            WordFrame = Frame(ChanceFrame)
            WordFrame.grid(row=0)
##            RollDiceLable = Label(WordFrame, text="Roll Chance?")
##            RollDiceLable.grid(row=0)
##            DiceFrame = Frame(ChanceFrame)
##            DiceFrame.grid(row=1)
##            YouRolledL = Label(DiceFrame,text="You Rolled A:")
##            YouRolledL.grid(row=0, sticky=tkinter.N+tkinter.S)
##            LookLikeADice = tkinter.Frame(DiceFrame,bd=1, relief=tkinter.RAISED,width=500,height=50)
##            LookLikeADice.grid(row=0,column=1)
##            DiceWink = Label(LookLikeADice,image=DieImages[0])
##            DiceWink.grid()
##            RollDiceButton = Button(WordFrame, text="Roll", command = lambda DiceWink=DiceWink, ChanceFrame=ChanceFrame: RollDiceFunc(DiceWink,ChanceFrame))
##            RollDiceButton.grid(row=1)
            RollDiceButton = Button(WordFrame, text="Play Chance", command = lambda: RollDiceFunc())
            RollDiceButton.grid(row=1)
        for frame in FrameList:
                frame.destroy()
        USERFRAME = tkinter.Frame(GUI)
        USERFRAME.grid(row=97, padx=5)
        for Num in range(Number):
            userGUI(Num+1,USERFRAME,isdefault)
    global currentusernum
    currentusernum += Number


def main():
    UserNumber = tkinter.StringVar()
    BottomStuffFrame = Frame(GUI)
    BottomStuffFrame.grid(row=99)
    UsercommandFrame = tkinter.Frame(BottomStuffFrame,bd=5,bg="lemon chiffon",relief=tkinter.RAISED)
    UsercommandFrame.grid(row=99)
    UserNum = tkinter.Entry(UsercommandFrame, width=5, textvariable=UserNumber)
    UserNum.grid(column = 2, row=1,padx=5,pady=5)
    UserCommand = tkinter.Button(UsercommandFrame, text = 'Add Users', width = 10,command = lambda BottomStuffFrame = BottomStuffFrame: AddUsers(int(UserNumber.get()),BottomStuffFrame))
    UserCommand.grid(column=1,row=1,padx=5,pady=5)
    tkinter.mainloop()


main()

