import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop


class ServiceNotify(dbus.service.Object):
    """
    Create a dbus instance at client path and export Notify dbus function
    for sending messages to the bot
    """

    def __init__(self, dbus_session, client_dbus, handler_interface, handler_path, notify_handler):
        dbus.service.Object.__init__(self, dbus_session, handler_path)
        self.client_dbus = client_dbus
        self.notify_handler = notify_handler(client_dbus)

    @dbus.service.method(dbus_interface='com.Skype.API.Client')
    def Notify(self, string):
        self.notify_handler.input(string)


class ServiceInvoke:
    """Initalize the connection, define bot's name and protocol"""

    def __init__(self, interface, dbus_path, notify_handler):
        DBusGMainLoop(set_as_default=True)
        self.dbus_session = dbus.SessionBus()
        self.interface = interface
        self.dbus_path = dbus_path
        self.client_dbus = None
        self.notify_handler = notify_handler

    def connect(self, name):
        self.client_dbus = self.dbus_session.get_object(
            self.interface,
            self.dbus_path
        )

        self.__send("NAME " + name)
        self.__send("PROTOCOL 7")

    def create_notify_service(self, handler_interface, handler_path):
        ServiceNotify(
            self.dbus_session,
            self.client_dbus,
            handler_interface,
            handler_path,
            self.notify_handler
        )

    def __send(self, text):
        self.client_dbus.Invoke(text)
