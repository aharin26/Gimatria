# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 17:39:39 2020

@author: shloimie
"""
from tkinter import  *

#import the whole tkinter

root = Tk()
#makes instance to be used later
root.title("Gimatria")
#names tiltle 
root.geometry("590x650")
#how big window to open
root.iconbitmap("icon.ico")
#set icon for file quit
root.resizable(False, False)
import re
import string
numValue = {"א":1, "ב":2, "ג":3, "ד":4, "ה":5, "ו":6, "ז":7, "ח":8, "ט":9, "י":10, "כ":20, "ל":30, "מ":40, "נ":50, "ס":60, "ע":70, "פ":80, "צ":90, "ק":100, "ר":200, "ש":300, "ת":400, "ם":40, "ן":50, "ף":80, "ץ":90, "ך":20}

hebrewLetters = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ו', 'ז', 'ח', 'ט', 'י', 'כ', 'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'פ', 'צ', 'ק', 'ר', 'ש', 'ת', 'ם', 'ן', 'ץ', 'ף', 'ך', ' ', '־']

def valueOf(text):

	try: int(text)
	except:
		textList = list(text)
		value = 0
		for letter in textList:
			if letter ==  " " or letter == "\n" or letter == "־": continue
			value = value + numValue[letter]
		return value
	return int(text)

def checkIfContains(word, contain):
	for char in word:
		if char == contain:
			return True
	return False
def numberOfInstancesIn(word, contains):
	number = 0
	for char in word:
		if char == contains:
			number += 1
	return number

bookDictionary = {1:("br_edit.txt", "Bereishis"), 2:("sh_edit.txt", "Shemos"), 3:("vy_edit.txt", "Vayikra"), 4:("bm_edit.txt", "Bamidbar"), 5:("dv_edit.txt", "Devarim"), 6:("neviim/yehoshua_edit.txt", "Yehoshua"), 7:("neviim/shoftim_edit.txt", "Shoftim"), 8:("neviim/shmuel1_edit.txt", "Shmuel 1"), 9:("neviim/shmuel2_edit.txt", "Shmuel 2"), 10:("neviim/melachim1_edit.txt", "Melachim 1"), 11:("neviim/melachim2_edit.txt", "Melachim 2"), 12:("neviim/yeshaya_edit.txt", "Yeshaya"), 13:("neviim/yirmiya_edit.txt", "Yirmiya"), 14:("neviim/yechezkel_edit.txt", "Yechezkel"), 15:("neviim/hoshea_edit.txt", "Hoshea"), 16:("neviim/yoel_edit.txt", "Yoel"), 17:("neviim/amos_edit.txt", "Amos"), 18:("neviim/ovadya_edit.txt", "Ovadya"), 19:("neviim/yonah_edit.txt", "Yonah"), 20:("neviim/micha_edit.txt", "Micha"), 21:("neviim/nachum_edit.txt", "Nachum"), 22:("neviim/chavakuk_edit.txt", "Chavakuk"), 23:("neviim/tzefania_edit.txt", "Tzefania"), 24:("neviim/chagai_edit.txt", "Chagai"), 25:("neviim/zecharia_edit.txt", "Zecharia"), 26:("neviim/malachi_edit.txt", "Malachi"), 27:("kesuvim/tehilim_edit.txt", "Tehillim"), 28:("kesuvim/mishlei_edit.txt", "Mishlei"), 29:("kesuvim/iyov_edit.txt", "Iyov"), 30:("kesuvim/shirHashirim_edit.txt", "Shir Hashirim"), 31:("kesuvim/rus_edit.txt", "Rus"), 32:("kesuvim/eicha_edit.txt", "Eicha"), 33:("kesuvim/koheles_edit.txt", "Koheles"), 34:("kesuvim/esther_edit.txt", "Esther"), 35:("kesuvim/daniel_edit.txt", "Daniel"), 36:("kesuvim/ezra_edit.txt", "Ezra"), 37:("kesuvim/nechemia_edit.txt", "Nechemia"), 38:("kesuvim/divreiHayamim1_edit.txt", "Divrei Hayamim 1"), 39:("kesuvim/divreiHayamim2_edit.txt", "Divrei Hayamim 2")}


listOfAnswers = []
########## Scan Through
def scanThrough(testVal):
	perek = 0
	pasuk = 0
	parsha = ''


	bookAddress ="tanach/"
	fileAddressSeperator = "/"
	# cycle thru bookim
	for book in range(1, 40):
		
		bookName = bookDictionary[book][1]
		book = open("{}{}".format(bookAddress, bookDictionary[book][0]), encoding='utf-8')
			
		perek = 0

		# line number that the loop is up to
		presentLineNum = 0


		for line in book:
			presentLineNum +=1
			# make sure it's not a perek number or parsha name
			if checkIfContains(line, "׳") or checkIfContains(line, "״"):
				perek += 1
				pasuk = 1
				continue
			elif numberOfInstancesIn(line, " ") < 2 and not checkIfContains(line, "־"):
				parsha = line
				continue

			# split up words
			line = re.split(r' |־', line)

			# accumilated value of words
			currentVal = 0
			wordsStr = ""

			# index (in line) of starting word of sequence
			startingWordIndex = 0

			# iterate thru words in line (to be STARTING word)
			for word in line:


				# dont want these words to be starting words
				if checkIfContains(word, "(") or checkIfContains(word, "["):
					continue

				# iterate thru words of line after STARTING word
				for word in line[startingWordIndex:]:

					# dont want this word to be counted
					if checkIfContains(word, "(") or checkIfContains(word, "]") or checkIfContains(word, "["):
						continue

					# dont want the newline to be part of the word
					if checkIfContains(word, "\n"):
						word = word[:-1]

					# add this word to sequence and value to accumilated value
					wordsStr = wordsStr + word + " "

#                                       currentVal += valueOf(word)

					# find where there is corrupted text (must comment out the line before
					try: currentVal += valueOf(word)
					except: print(book, presentLineNum, word)

					if currentVal == testVal:
						T.insert(END, "{}, {}, {}, {}\n".format(wordsStr, bookName, str(perek), str(pasuk)))
						
						listOfAnswers.append((wordsStr, bookName, str(perek), str(pasuk)))
						break
					elif currentVal > testVal:
						break
				currentVal = 0
				wordsStr = ""           
				startingWordIndex += 1
			
			pasuk += 1
		T.update()
#		for answer in listOfAnswers:
#			print(answer)
#			listOfAnswers = []
	

# Handle input
def handleInputAndScan(text):
	if text == "quit" or text == "q":
	    quit()
	letters = 0
	numbers = 0
	for char in str(text):
		if char in hebrewLetters:
			letters += 1
			if letters == len(text):
				print(valueOf(text))
				scanThrough(valueOf(text))
				break
#                       if numbers + letters == len(text):
#                               handleNumbersAndLettersTogether(text)
		elif char in string.digits:
			numbers += 1
			if numbers == len(str(text)):
				scanThrough(int(text))
				break
			if numbers + letters == len(text):
				handleNumbersAndLettersTogether(text)
		else: print("Please enter only numbers or only letters!!")

def handleNumbersAndLettersTogether(text):
	sumOfNumbersAndLetters = 0
	for char in text:
		sumOfNumbersAndLetters += valueOf(char)
	scanThrough(sumOfNumbersAndLetters)
	
value=0
def buttonClicked1():
	
	T.delete( 1.0 ,END)
	
	value = valueOf(user_word.get())
	toplabel.configure(text="Value = " + str(value))
	toplabel.update()

	handleInputAndScan(user_word.get())
	
	



# Run the program!!     
#while True:
#	handleInputAndScan(input("Please enter a number or words:"))

#top right frame 
labelFrame = Frame(root ,width = 40,height =200 ,bd =5,)
labelFrame.grid(row=1,column=1, sticky= W)
#box wth intro text
label1 = Label(labelFrame,text="Please Enter A Number Or Letter" )
label1.pack()
#box with user name
entryFrame = Frame(root ,width = 20,height =200 ,bd =5,)
entryFrame.grid(row=2,column=1)
user_word = Entry(entryFrame, width=60, font=("Helvtica"))
user_word.pack()


#button
but1 = Button(root,text="Search", width =40, command=buttonClicked1)
but1.grid(row =3 , column =1 ,sticky =W)
#random frame
valueFrame = Frame(root ,width = 20,height =200 ,bd =5)
valueFrame.grid(row=3,column=1 ,sticky =W)
toplabel =Label(valueFrame, text = "Value= " + str(value) ,font=("Helvtica"),relief="groove")
toplabel.pack()
#frame with text 
resultsFrame = Frame(root ,height =200 ,bd =5)
resultsFrame.grid(row=4,column=1, sticky = W+E)
root.columnconfigure(1)
root.columnconfigure(2)
scrollBar = Scrollbar(resultsFrame)

T = Text(resultsFrame, height=40)

T.grid(column =1, row = 1)

scrollBar.config(command=T.yview)
scrollBar.grid(column=2, row=1, sticky = N+S)
T.config(yscrollcommand=scrollBar.set)

root.mainloop()
#end loop