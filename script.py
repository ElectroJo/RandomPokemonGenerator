import sys
import os
import requests
from multiprocessing import Queue
import tkinter
from tkinter import filedialog
from tkinter.ttk import *
import binascii
import csv
import random
GUI = tkinter.Tk()
FrameList = []
SeekLocations = {
    "PokemonNDexID" : 8,
    "PID" : 24
}

with open(r'pokedex\pokedex\data\csv\pokemon.csv', mode='r') as infile:
    reader = csv.reader(infile)
    mydict = {rows[0]:rows[1] for rows in reader}
class userGUI:
    def __init__(self,UserNum):
        if UserNum % 2 == 0:
            self.x = 2
            self.y = UserNum / 2
            self.y -= 1
        else:
            self.x = 1
            self.y = UserNum - 1
            self.y = self.y / 2
        self.userframe = tkinter.Frame(GUI)
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
        self.genfilesandsendto3ds = tkinter.Button(self.userframe, text="Sendto3ds", command = lambda:self.compileto3ds(self.truepokenum))
        self.genfilesandsendto3ds.grid(row=100)
        self.dsipadd = tkinter.StringVar()
        self.dsipadd.set("IP ADDRESS")
        self.dsipaddent = tkinter.Entry(self.userframe, textvariable=self.dsipadd)
        self.dsipaddent.grid(column = 0, row=101)
        self.pokenum = []
        self.tabnum = []
        self.pokemomids = {}


    def compileto3ds(self, number):
        self.number = number
        for count in range(self.number):
            self.replacehex('PokemonNDexID',self.flipthehexorder(self.turninttohex(self.pokemomids.get(count),4)))
            self.replacehex('PID',(self.turninttohex(random.randrange(0,4294967295),8)))
            self.sendfilesto3ds()

    def turninttohex(self,numbers,width):
        self.numbers = numbers
        self.curent = str(hex(self.numbers)[2:])
        if len(self.curent) == width:
            return self.curent
        else:
            self.curent = self.curent.zfill(width)
            return self.curent





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
        with open('Newoutput.pk7', 'rb') as f:
            content = f.read()
            f.close()
        g = open('Newoutput.pk7','wb')
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

    def pickpokemon(self,number):
        self.resetdicts()
        self.number = number
        for counts in range(self.number):
            self.tabnum.append(None)
            self.pokenum.append(tkinter.StringVar())
            self.tabnum[counts] = tkinter.Frame(self.NewNotebook)
            self.NewNotebook.add(self.tabnum[counts],text="Pokemon"+str(counts+1))
            pokemonlable = tkinter.Label(self.tabnum[counts],textvariable=self.pokenum[counts])
            pokemonlable.grid()
            self.pokemonnum = random.randrange(1,802)
            self.pokemomids[counts] = self.pokemonnum
            self.pokenum[counts].set(mydict.get(str(self.pokemonnum)))
        self.truepokenum = number


    def sendfilesto3ds(self):
        with open("Newoutput.pk7", "rb") as old, open("outfile.pk7", "wb") as new:
            new.write(str.encode('PKSMOTA'))
            new.write(old.read())
            new.close()
        try:
            with open('outfile.pk7', 'rb') as f: r = requests.post('http://'+self.dsipadd.get()+':9000', files={'outfile.pk7': f})
        except:
            pass


def AddUsers(Number):
    for Frames in FrameList:
        Frames.destroy()
    for Num in range(Number):
        userGUI(Num+1)

def main():
    UserNumber = tkinter.StringVar()
    UserNum = tkinter.Entry(GUI, width=5, textvariable=UserNumber)
    UserNum.grid(column = 2, row=99)
    TestCommand = tkinter.Button(GUI, text = 'Add Users', width = 16,command = lambda: AddUsers(int(UserNumber.get())))
    TestCommand.grid(column=1, row=99)
    tkinter.mainloop()


main()

