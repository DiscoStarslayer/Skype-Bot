import dbus
import dbus.service
import gobject
from dbus.mainloop.glib import DBusGMainLoop


class Filter:
	"""Filter the Skype API down to useable data"""
	
	def __init__(self, replyBus):
		self.bus = replyBus
		self.chatNumber = ""
		
	def Input(self, string):
		tokens = string.split(" ")
		self.Read(tokens)
		
	def Read(self, tokens):
		msgType = tokens[0]
		
		if msgType == "CHAT":
			self.chatNumber = tokens[1]
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
			if i == "test":
				self.Reply("you are a cunt")
			elif i == "Colin":
				self.Reply("Did you know, Colin is actualy a gnome in disguise?")
		
	def Reply(self, message):
		string = "CHATMESSAGE " + self.chatNumber + " " + message
		self.bus.Invoke(string)

class SNotify(dbus.service.Object):
	"""Create a dbus instance at /com/Skype/Client so skype can communicate
		with the bot. Notify() is called when skype talks to the bot."""
		
	def __init__(self, bus, skype):
		dbus.service.Object.__init__(self, bus, '/com/Skype/Client')
		self.skype = skype #allow bus to be reused
		self.filt = Filter(skype)
		
	def Send(self, text):
		self.skype.Invoke(text)
		
	@dbus.service.method(dbus_interface = 'com.Skype.API.Client')
	def Notify(self, string):
		self.filt.Input(string)


class SInvoke:
	"""Initalize the connection, define bot's name and protocol"""

	def __init__(self):
		DBusGMainLoop(set_as_default = True)
		self.bus = dbus.SessionBus()
		self.interface = "com.Skype.API"
		self.path = "/com/Skype"
		
	def Connect(self, name):
		self.skype = self.bus.get_object(self.interface, self.path)
		self.Send("NAME " + name)
		self.Send("PROTOCOL 7")
		self.notify = SNotify(self.bus, self.skype)
	
	def Send(self, text):
		self.skype.Invoke(text)	


"""Start the main notify loop"""
loop = gobject.MainLoop()
SInvoke().Connect("testing")
loop.run()
