import dbus


class SkypeInterface:
	"""The basic interface between this program and Skype"""

	def __init__(self):
		self.bus = dbus.SessionBus()
		self.service = "com.Skype.API"
		self.cts = "/com/Skype"
		self.stc = "/com/Skype/Client"
		
	def Connect(self, name):
		self.skype = self.bus.get_object(self.service, self.cts)
		print self.Send("NAME " + name)
		print self.Send("PROTOCOL 8")
	
	def Send(self, text):
		print self.skype.Invoke(text)
		
	def Get(self):
		print self.skype.Notify()
	


