import Filter

class Parse:
	
	def __init__(self, bus, chatNumber):
		self.bus = bus
		self.chatNumber = chatNumber
		
	def Start(self, body):
		if body == "test":
			self.Reply("This is a test reply")
		elif body == "Colin":
			self.Reply("brb in 10 min")

	def Reply(self, message):
		string = "CHATMESSAGE " + self.chatNumber + " " + message
		self.bus.Invoke(string)
		
	def SetChatNumber(self, chatNumber):
		self.chatNumber = chatNumber
