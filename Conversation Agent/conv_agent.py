# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 23:51:48 2021

@author: ACAN
"""
"""
ASSIGNMENT 1: GIVEN THE SIMPLE REFLEX AGENT BELOW, 
1. IMPROVE IT BY CHOSING WHOS STARTS THE DIALOG 
RANDOMLY AND IN CASE THAT THE COMPUTER STARTS
SELECT THE DIALOG FROM THE RULE BASE DISPLAY IT
TO USER.

2. IMPROVE LEARNING CAPABILITY BY DEFINING 
ALTERNATIVE ANSWERS FOR THE EXISTING DIALOG
RULES

DUE DATE: 29 MARCH 2021 MONDAY
"""
import os
import random
#Simple reflex conversation 
Rule_File="SRA_RuleFile.txt"

if not(os.path.isfile(Rule_File)):
    Rule_Base={}
    Rule_Base={'How are you?':"Thanks, what about you?"}
    Rule_Base['What is your name?']="SRCAgent"
    Rule_Base['']="You are silent!"
else:
    # READ THE RULE FILE
    Rule_Base={}
    InFile=open(Rule_File,"r")
    for Line in InFile:
        Line=Line.rstrip('\n')
        Line=Line.split(':')
        Rule_Base[Line[0]]=Line[1]
    InFile.close()
    
YourName=input("May I get your name please. ")
print("Hi", YourName," let's have a dialog")

# Dialog=''
# Latest_Dialog=''

entry = ""
latest_entry = ""

# I have made 2 changes
# 1st I made it so sometimes the SRCAgent asks the question first and whatever we answer may be added to the rule_base replies
# 2nd I added the option to give more than one possible answer to a question by keeping the Rule base dictionary key as the question
# and the Rule base dictionary value as a list of strings containing possible replies each seperated by '|' character

while entry != ".":
	# a random to choose whether the bot initiates dialogue or us
	r = random.randint(0,1)
	# I use | as a seperator for possible answers to a question
	if r == 0:
		print("-Chat Bot is asking a question-")
		key = random.choice(list(Rule_Base.keys()))
		dialogue_list = Rule_Base[key].split("|")
		entry = input(key)
		if entry == ".":
			break
		elif entry not in dialogue_list:
			# If we enter a dialogue that is not in the list of replies
			# We append that reply on to the list
			Rule_Base[key] += "|" + entry
	else:
		print("-You are asking a question-")
		entry = input()
		if entry == ".":
			break
		elif entry==latest_entry:
			print("Let's not waste time with repetitions")
		elif entry not in Rule_Base:
			print("I am sorry I do not know the reply for this dialog.")
			print("Would you please help me learning? Please type Y (Yes) or N (No)")
			Reply=input()
			if Reply == 'Y':
				Reply = input("Please type your reply: ")
				Rule_Base[entry] = Reply
			latest_entry = Reply
		else:
			# Getting a random reply from list of replies
			Reply = random.choice(Rule_Base[entry].split("|"))
			print(Reply)
			# Request to add another possible reply and append it by using "|"
			Reply = input("Would you like to add another possible reply Y (Yes) / N (No)\n")
			if Reply == "Y":
				Reply = input("Please enter the reply for this dialogue\n")
				if Reply not in Rule_Base[entry].split("|"):
					Rule_Base[entry] += "|"+Reply
				else:
					print("That reply already exists!")
				latest_entry = Reply
			

print("Bye ", YourName, " Thanks for the dialog")

# SAVE THE RULE BASE

OutFile=open(Rule_File,"w")
for x in Rule_Base:
    OutFile.write(x+":"+Rule_Base[x]+'\n')

OutFile.close()

    
