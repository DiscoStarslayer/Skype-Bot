import Filter
from subprocess import check_output

class Parse:
	
	def __init__(self, bus, chatNumber):
		self.bus = bus
		self.chatNumber = chatNumber
		self.commands = {'!test':"This is a test reply",
				 '!tase':"I'm afraid I can't do that.",
				 '!hello':'Hello Dave',
				 '!create':'',
				 '!list':'',
				 '!fortune':''}
		
	def Start(self, body):
		if body[0].lower() == '!create':
			string = ""
			length = len(body) - 2
			for i in range(length):
				string = string + body[i+2] + " "
			string.strip()
			self.commands["!"+body[1].lower()] = string
			self.Reply("Created !" + body[1])
		elif body[0].lower() == "!list":
			string = ""
			for i in self.commands:
				string = string + i + " "
			self.Reply(string.lower())
		elif body[0].lower() == "!fortune":
			string = check_output('fortune')
			self.Reply(string)
		else:
			for i in body:
				if i.lower() in self.commands:
					self.Reply(self.commands[i.lower()])

	def Reply(self, message):
		string = "CHATMESSAGE " + self.chatNumber + " " + message
		self.bus.Invoke(string)
		
	def SetChatNumber(self, chatNumber):
		self.chatNumber = chatNumber
