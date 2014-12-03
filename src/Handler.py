from Response import ResponseGenerator


class NotifyHandler:
    """Handle SkypeAPI messages from dbus"""

    def __init__(self, reply_bus):
        self.reply_bus = reply_bus
        self.chat_id = ""
        self.response_generator = ResponseGenerator(reply_bus)

    def input(self, string):
        tokens = string.split(" ")
        self.read(tokens)

    def read(self, tokens):
        message = self.parse_message(tokens)
        if (
            message["type"] == "CHATMESSAGE" and
            message["status"] == "RECEIVED"
        ):
            body = self.get_chat_message(message["chat_message_id"])
            chat_name = self.get_chat_message_chat_name(message["chat_message_id"])
            self.set_chat_message_read(message["chat_message_id"])
            self.parse_response(body, chat_name)

    def set_chat_message_read(self, msg_id):
        return self.send_message(
            "SET CHATMESSAGE {msg_id} SEEN".format(msg_id=msg_id)
        )

    def get_chat_message(self, msg_id):
        return self.send_message(
            "GET CHATMESSAGE {msg_id} BODY".format(msg_id=msg_id)
        )

    def get_chat_message_chat_name(self, msg_id):
        return self.send_message(
            "GET CHATMESSAGE {msg_id} CHATNAME".format(msg_id=msg_id)
        )

    def parse_response(self, body_response, chat_name_response):
        chat_name = self.parse_chat_name_response(chat_name_response)
        body = self.parse_body_response(body_response)

        self.response_generator.generate_response(chat_name, body)

    def parse_body_response(self, body_response):
        # BODY is 4 characters with a trailing space
        body_index = body_response.find("BODY") + 5
        return body_response[body_index:]

    def parse_chat_name_response(self, chat_name_response):
        tokens = chat_name_response.split(" ")
        return(tokens[3])

    def send_message(self, message_string):
        return self.reply_bus.Invoke(message_string)

    def parse_message(self, tokens):
        parsed_dict = dict()
        parsed_dict["type"] = tokens[0]

        if parsed_dict["type"] == "CHAT":
            parsed_dict["chat_id"] = tokens[1]
            parsed_dict["timestamp"] = tokens[3]
        elif parsed_dict["type"] == "CHATMESSAGE":
            parsed_dict["chat_message_id"] = tokens[1]
            parsed_dict["status"] = tokens[3]
        else:
            print("Unknown Message: {}".format(str(tokens)))

        return parsed_dict
