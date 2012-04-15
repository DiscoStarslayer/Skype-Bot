import Filter
import random
import Database
from subprocess import check_output

class Parse:
	
	def __init__(self, bus, chatNumber):
		self.bus = bus
		self.chatNumber = chatNumber
		self.db = Database.Data()
		self.commands = self.db.ToDict('commands')
		self.excuses = self.db.ToList('excuses')
		
	def Start(self, body):
		if body[0].lower() == '!create':
			string = ""
			length = len(body) - 2
			for i in range(length):
				string = string + body[i+2] + " "
			string.strip()
			self.commands["!"+body[1].lower()] = string
			self.Reply("Created !" + body[1])
			self.db.SaveDict(self.commands, 'commands')
			self.Reply("Saved commands to file")
		elif body[0].lower() == "!list":
			string = ""
			for i in self.commands:
				string = string + i + " "
			self.Reply(string.lower())
		elif body[0].lower() == "!fortune":
			string = check_output('fortune')
			self.Reply(string)
		elif body[0].lower() == "!excuse":
			self.Reply(self.excuses[random.randint(0, len(self.excuses))])
		elif body[0].lower() == "!save":
			self.db.SaveDict(self.commands, 'commands')
			self.Reply("Saved commands to file")
		elif body[0].lower() == "!reload":
			self.commands = self.db.ToDict('commands')
			self.Reply("Reloaded command file")
		elif body[0].lower() == "!delete":
			del self.commands['!' + body[1].lower()]
		else:
			for i in body:
				if i.lower() in self.commands:
					self.Reply(self.commands[i.lower()])

	def Reply(self, message):
		string = "CHATMESSAGE " + self.chatNumber + " " + message
		self.bus.Invoke(string)
		
	def SetChatNumber(self, chatNumber):
		self.chatNumber = chatNumber
