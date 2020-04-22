from tkinter import  *
import re
import string
#import the whole tkinter

root = Tk()
#makes instance to be used later
root.title("Gimatria")
#names tiltle 
root.geometry("400x600")

#how big window to open
root.iconbitmap("icon.ico")
#set icon for file quit
root.resizable(True, True)

hsn = {'numerals': {1:"א", 2:"ב", 3:"ג", 4:"ד", 5:"ה", 6:"ו", 7:"ז", 8:"ח", 9:"ט", 10:"י", 20:"כ", 30:"ל", 40:"מ", 50:"נ", 60:"ס", 70:"ע", 80:"פ", 90:"צ", 100:"ק"}, 'specials': {0:"0", 15:"טו", 16:"טז", 115:"קטו", 116:"קטז"}, 'separators':{'geresh':"\'", 'gershayim':"\""}}
numValue = {"א":1, "ב":2, "ג":3, "ד":4, "ה":5, "ו":6, "ז":7, "ח":8, "ט":9, "י":10, "כ":20, "ל":30, "מ":40, "נ":50, "ס":60, "ע":70, "פ":80, "צ":90, "ק":100, "ר":200, "ש":300, "ת":400, "ם":40, "ן":50, "ף":80, "ץ":90, "ך":20}

hebrewLetters = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ו', 'ז', 'ח', 'ט', 'י', 'כ', 'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'פ', 'צ', 'ק', 'ר', 'ש', 'ת', 'ם', 'ן', 'ץ', 'ף', 'ך', ' ', '־']
bookDictionary = {1:("br_edit.txt","בראשית"), 2:("sh_edit.txt", "שמות"), 3:("vy_edit.txt",  "ויקרא"),
 4:("bm_edit.txt",  "במדבר"), 5:("dv_edit.txt", "דברים"), 6:("neviim/yehoshua_edit.txt", "יהושע"),
  7:("neviim/shoftim_edit.txt", "שופטים"), 8:("neviim/shmuel1_edit.txt", "שמואל א"),
   9:("neviim/shmuel2_edit.txt", "שמואל ב"), 10:("neviim/melachim1_edit.txt", "מלכים א"),
    11:("neviim/melachim2_edit.txt", "מלכים ב"), 12:("neviim/yeshaya_edit.txt", "ישעיה"),
     13:("neviim/yirmiya_edit.txt", "ירמיה"), 14:("neviim/yechezkel_edit.txt", "יחזקאל"),
      15:("neviim/hoshea_edit.txt", "הושע"), 16:("neviim/yoel_edit.txt","יואל"), 
      17:("neviim/amos_edit.txt", "עמוס"), 18:("neviim/ovadya_edit.txt", "עובדיה"), 
      19:("neviim/yonah_edit.txt", "יונה"), 20:("neviim/micha_edit.txt", "מיכה"), 
      21:("neviim/nachum_edit.txt", "נחום"), 22:("neviim/chavakuk_edit.txt", "חבקוק"),
       23:("neviim/tzefania_edit.txt", "צפניה"), 24:("neviim/chagai_edit.txt", "חגי"), 
       25:("neviim/zecharia_edit.txt", "זכריה"), 26:("neviim/malachi_edit.txt", "מלאכי"), 
       27:("kesuvim/tehilim_edit.txt", "תהלים"), 28:("kesuvim/mishlei_edit.txt", "משלי"),
        29:("kesuvim/iyov_edit.txt", "איוב"), 30:("kesuvim/shirHashirim_edit.txt", "שיר השירים"),
         31:("kesuvim/rus_edit.txt", "רות"), 32:("kesuvim/eicha_edit.txt", "איכה"), 
         33:("kesuvim/koheles_edit.txt","קהלת"), 34:("kesuvim/esther_edit.txt", "אסתר"),
          35:("kesuvim/daniel_edit.txt", "דניאל"), 36:("kesuvim/ezra_edit.txt", "עזרא"),
           37:("kesuvim/nechemia_edit.txt", "נחמיה"), 38:("kesuvim/divreiHayamim1_edit.txt", "דברי הימים א"),
            39:("kesuvim/divreiHayamim2_edit.txt", "דברי הימים ב")}
listOfAnswers = []

def hebrew_numeral(val, gershayim=True):
	# 1. Lookup in specials
	if val in hsn['specials']:
		retval = hsn['specials'][val]
		return add_gershayim(retval) if gershayim else retval

	# 2. Generate numeral normally
	parts = []
	rest = str(val)
	while rest:
		digit = int(rest[0])
		rest = rest[1:]
		if digit == 0: continue
		power = 10 ** len(rest)
		parts.append(hsn['numerals'][power * digit])
	retval = ''.join(parts)
	# 3. Add gershayim
	return add_gershayim(retval) if gershayim else retval

def add_gershayim(s):
	if len(s) == 1:
		s += hsn['separators']['geresh']
	else:
		s = ''.join([
			s[:-1],
			hsn['separators']['gershayim'],
			s[-1:]
		])
	return s

class Test(Text):
    def __init__(self, master, **kw):
        Text.__init__(self, master, **kw)
        self.bind('<Control-c>', self.copy)
        self.bind('<Control-x>', self.cut)
        self.bind('<Control-v>', self.paste)

    def copy(self, event=None):
        self.clipboard_clear()
        text = self.get("sel.first", "sel.last")
        self.clipboard_append(text)

    def cut(self, event):
        self.copy()
        self.delete("sel.first", "sel.last")

    def paste(self, event):
        text = self.selection_get(selection='CLIPBOARD')
        self.insert('insert', text)





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



########## Scan Through
def scanThrough(testVal):
	perek = 0
	pasuk = 0
	parsha = ''


	bookAddress ="tanach/"


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
						T.insert(END, "{}, {}, {} \t {}\n".format(bookName, hebrew_numeral(perek), hebrew_numeral(pasuk), wordsStr))
#						T.insert(END, "{}, \t{}, {}, {}\n".format(wordsStr, bookName, hebrew_numeral(perek), hebrew_numeral(pasuk)))
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
		else: 
			T.insert(END, "Please enter only numbers or only letters!!")
			T.configure()
			T.update()

def handleNumbersAndLettersTogether(text):
	sumOfNumbersAndLetters = 0
	for char in text:
		sumOfNumbersAndLetters += valueOf(char)
	scanThrough(sumOfNumbersAndLetters)
	
value=0
def buttonClicked1():
	
	T.delete( 1.0 ,END)
	
	try: 
		value = valueOf(user_word.get())
		toplabel.configure(text="Value = " + str(value))
		toplabel.update()
	except: pass
	

	handleInputAndScan(user_word.get())
	
def reset_tabstop(event):
	event.widget.configure(tabs=(event.width-8, "right"))

def func(event):
	buttonClicked1()
	
root.bind('<Return>', func)

#makes enter key hit search

# Run the program!!     
#while True:
#	handleInputAndScan(input("Please enter a number or words:"))




#box wth intro text
label1 = Label(root,text="Please Enter A Number Or Letter" )
label1.grid(row=1,column=1, sticky= W)
#box with user name
user_word = Entry(root, width=43, font=("Times",16))
user_word.grid(row=2,column=1 ,)
user_word.columnconfigure(1, weight=1)
user_word.focus_set()
#button
but1 = Button(root,text="Search", width =40, command=buttonClicked1)
but1.grid(row =3 , column =1 ,sticky =W)

#value frame
valueFrame = Frame(root ,width = 20 ,bd =5)
valueFrame.grid(row=3,column=1 ,sticky =W)
toplabel =Label(valueFrame, text = "Value= " + str(value) ,font=("Helvtica"),relief="groove")
toplabel.pack()

#frame with text 
resultsFrame = Frame(root,bd =5)
resultsFrame.grid(row=4,column=1, sticky = W+E+N+S)
root.columnconfigure(1, weight=1)
root.rowconfigure(4, weight=1)
resultsFrame.columnconfigure(1, weight=1)
resultsFrame.rowconfigure(1, weight=1)

scrollBar = Scrollbar(resultsFrame)

T = Text(resultsFrame, height=40,font=("Times"))

T.grid(column =1, row = 1, sticky=E+W+N+S)

#T.tag_add("center", 1.0, "end")


scrollBar.config(command=T.yview)
scrollBar.grid(column=2, row=1, sticky = N+S)
T.config(yscrollcommand=scrollBar.set)
T.bind("<Configure>", reset_tabstop)

label2 = Label(root,text="Gimatria" )
label2.grid(row=5,column=1, sticky= E)

root.mainloop()
#end loop