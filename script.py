import sys
import os
import tkinter
from tkinter import filedialog
from tkinter.ttk import *
import binascii
import csv
import random
GUI = tkinter.Tk()
FrameList = []
SeekLocations = {
    "PokemonNDexID" : 8
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
        self.genpoke = tkinter.Button(self.userframe, text = 'Test', width = 16,command = lambda pickpokemon = self.pickpokemon, PokeNumber = self.PokeNumber: pickpokemon(int(PokeNumber.get())))
        self.genpoke.grid(column = 0, row=99)
        self.PokeNum = tkinter.Entry(self.userframe, width=5, textvariable=self.PokeNumber)
        self.PokeNum.grid(column = 1, row=99)

    def turninttohex(self,numbers):
        if len(hex(numbers)[2:]) % 2 == 0:
            return str(hex(numbers)[2:])
        else:
            return str(hex(numbers)[2:].zfill(len(hex(numbers)) - 1))

    def flipthehexorder(self,hexes):
        hexlist = []
        runnum = 0
        runnum2 = 0
        for nibbles in range(1+int(len(hexes)/2)):
            if nibbles == 0:
                pass
            else:
                runnum += 1
                if (runnum2*2) == 0:
                    hexlist.append(hexes[len(hexes)-(runnum*2):])
                else:
                    hexlist.append(hexes[len(hexes)-(runnum*2):-(runnum2*2)])
                runnum2 += 1
        return ''.join(map(str, hexlist))

    def replacehex(self,whattochange,hexvalues):
        with open(filedialog.askopenfilename(), 'rb') as f:
            content = f.read()
            f.close()
        g = open('Newoutput.pk7','wb')
        g.write(content)
        g.seek(SeekLocations.get(whattochange))
        hex_data=bytearray.fromhex(hexvalues)
        g.write(hex_data)
        g.close()

    def pickpokemon(self,number):
        pokenum = []
        tabnum = []
        for counts in range(number):
            tabnum.append(None)
            pokenum.append(tkinter.StringVar())
            tabnum[counts] = tkinter.Frame(self.NewNotebook)
            self.NewNotebook.add(tabnum[counts],text="Pokemon"+str(counts+1))
            pokemonlable = tkinter.Label(tabnum[counts],textvariable=pokenum[counts])
            pokemonlable.grid()

            pokenum[counts].set(mydict.get(str(random.randrange(1,802))))




def AddUsers(Number):
    for Frames in FrameList:
        Frames.destroy()
    for Num in range(Number):
        userGUI(Num+1)

def main():
    UserNumber = tkinter.StringVar()
    UserNum = tkinter.Entry(GUI, width=5, textvariable=UserNumber)
    UserNum.grid(column = 2, row=99)
    TestCommand = tkinter.Button(GUI, text = 'Test', width = 16,command = lambda: AddUsers(int(UserNumber.get())))
    TestCommand.grid(column=1, row=99)
    tkinter.mainloop()


main()
import requests
with open(r'C:\Users\Joey\Downloads\_sunmoon_v6.1\PKHeX Gen 7\003 - Venusaur - E472AD2F84C5.pk7', 'rb') as f: r = requests.post('http://192.168.0.109:9000', files={r'003 - Venusaur - E472AD2F84C5.pk7': f})
"""
import binascii
import requests

example code to be later used for requests to 3ds
with open("base.pk7", "rb") as old, open("penix.pk7", "wb") as new:
    new.write(str.encode('PKSMOTA'))
    new.write(old.read())
with open('penix.pk7', 'rb') as f: r = requests.post('http://192.168.0.109:9000', files={'outfile.pk7': f})
"""