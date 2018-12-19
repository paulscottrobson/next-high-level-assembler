# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		hlasm.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		19th December 2018
#		Purpose :	Code Generator
#
# ***************************************************************************************
# ***************************************************************************************

import re

class DummyStore(object):
	def __init__(self):
		self.addr = 0x1000
	def cByte(self,b):
		self.addr += 1
	def getAddress(self):
		return self.addr

class DummyDictionary(object):
	pass

# ***************************************************************************************
#									Base Class
# ***************************************************************************************

class BaseGenerator(object):
	def __init__(self,storage,dictionary):
		self.storage = storage
		self.dictionary = dictionary
		self.regExCompile = re.compile(self.regexSource())

	def check(self,word):
		print("****",word,"****")
		self.word = word
		if self.quickTest(word):
			self.match = self.regExCompile.match(self.word)
			if self.match is not None:
				print(self.match.groups())
				self.group = self.match.groups()
				self.generateCode()
				return True
		return False

	def generateCode(self):
		return self.dummyCode()
	def quickTest(self,word):
		return word.find(self.quickTestCharacter()) >= 0	
	def quickTestCharacter(self):
		assert False,"Not implemented"

BaseGenerator.IDENT = "([\_a-z][\_a-z0-9]+)"
BaseGenerator.OPTIND = "(\.[0-9a-z\_])?"
	
# ***************************************************************************************
#									String constant
# ***************************************************************************************

class StringConstant(BaseGenerator):
	def regexSource(self):
		return "^\"(.*)\"$"
	def quickTestCharacter(self):
		return '"'
	def dummyCode(self):
		print("{0:04x} : db  '{1}',0".format(self.storage.getAddress(),self.word[1:-1].replace("_"," ")))
		self.storage.cByte(0)

# ***************************************************************************************
#									Integer constant
# ***************************************************************************************

class IntegerConstant(BaseGenerator):
	def regexSource(self):
		return "^[0-9]+$"
	def quickTest(self,word):
		return word[0] >= '0' and word[0] <= '9'
	def dummyCode(self):
		print("{0:04x} : lda #${1:04x}',0".format(self.storage.getAddress(),int(self.word)))
		self.storage.cByte(0)

# ***************************************************************************************
#									  Load Variable
# ***************************************************************************************

class LoadVariable(BaseGenerator):
	def regexSource(self):
		return "^"+BaseGenerator.IDENT+BaseGenerator.OPTIND+"$"		
	def quickTest(self,word):
		return (word[0] >= 'a' and word[0] <= 'z') or word[0] == "_"
	def dummyCode(self):
		if self.groups[1] is None:
			print("{0:04x} : lda ${1:04x}',0".format(self.storage.getAddress(),int(self.word)))
			self.storage.cByte(0)


store = DummyStore()
ddict = DummyDictionary()

StringConstant(store,ddict).check('"hello_world"')
IntegerConstant(store,ddict).check("42")

LoadVariable(store,ddict).check("hello")
LoadVariable(store,ddict).check("hello.a")
LoadVariable(store,ddict).check("hello.12")
