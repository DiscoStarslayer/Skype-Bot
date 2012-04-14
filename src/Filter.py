import Parse


class Filter:
	"""Filter the Skype API down to useable data"""
	
	def __init__(self, replyBus):
		self.bus = replyBus
		self.chatNumber = ""
		self.Parser = Parse.Parse(replyBus, self.chatNumber)
		
	def Input(self, string):
		tokens = string.split(" ")
		self.Read(tokens)
		
	def Read(self, tokens):
		msgType = tokens[0]
		if msgType == "CHAT":
			self.chatNumber = tokens[1]
			self.Parser.SetChatNumber(self.chatNumber)
		elif msgType == "CHATMESSAGE" and (tokens[3] == "RECEIVED" or tokens[3] == "READ"):
			messageNumber = tokens[1]
			body = self.GetMessage(messageNumber)
			self.Parse(self.Clean(body))
	
	def GetMessage(self, msgNum):
		return self.bus.Invoke("GET CHATMESSAGE " + msgNum + " BODY")
		
	def Clean(self, body):
		split = body.split("BODY")
		return split[1][1:].strip()
	
	def Parse(self, body):
		splitBody = body.split(" ")
		
		for i in splitBody:
			self.Parser.Start(i)
		

