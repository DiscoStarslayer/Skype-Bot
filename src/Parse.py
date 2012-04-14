import Filter

class Parse:
	
	def __init__(self, bus, chatNumber):
		self.bus = bus
		self.chatNumber = chatNumber
		self.commands = {'!test':"This is a test reply",
				 '!colin':'brb in 10 min',
				 '!nigger':"THAT'S RACIST!",
				 '!petras':"Loves Pokemon more than his family",
				 '!willy':"Is FABULOUS!",
				 '!darren':"He is the all mighty creator!",
				 '!dev':"I like trucks too",
				 '!tase':"I'm afraid I can't do that Dave."}
		
	def Start(self, body):
		if body[0].lower() == '!create' and not body[1].lower() == 'list':
			string = ""
			length = len(body) - 2
			for i in range(length):
				string = string + body[i+2] + " "
			string.strip()
			self.commands["!"+body[1].lower()] = string
		elif body[0].lower() == "!list":
			string = ""
			for i in self.commands:
				string = string + i + " "
			self.Reply(string.lower())
		else:
			for i in body:
				if i.lower() in self.commands:
					self.Reply(self.commands[i.lower()])

	def Reply(self, message):
		string = "CHATMESSAGE " + self.chatNumber + " " + message
		self.bus.Invoke(string)
		
	def SetChatNumber(self, chatNumber):
		self.chatNumber = chatNumber
