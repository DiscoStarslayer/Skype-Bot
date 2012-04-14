from Filter import Filter
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

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


