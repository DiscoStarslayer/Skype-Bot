from PhraseDatabases import EightBall, Excuses, Commands


class ResponseGenerator:

    def __init__(self, bus):
        self.bus = bus
        self.eightball = EightBall()
        self.excuses = Excuses()
        self.commands = Commands()

    def generate_response(self, chat_name, body):
        # Tokenize body
        body_tokens = body.split(" ")
        # Important commands can only be run if line is started with the word
        command = body_tokens[0].lower()

        if command == '!create':
            new_command = body_tokens[1].lower()
            response_index = body.find(new_command) + len(new_command) + 1
            response = body[response_index:]
            self.commands.set(new_command, response)

            self.reply(chat_name, "Command !{0} created.".format(new_command))

        elif command == "!list":
            string = ""
            for command_ in self.commands.list():
                string += "!{0} ".format(command_)

            self.reply(chat_name, string.lower())

        elif command == "!delete":
            cleaned_command = body_tokens[1].lower()
            success = self.commands.delete(cleaned_command)

            if success:
                self.reply(
                    chat_name,
                    "Command !{0} deleted.".format(cleaned_command)
                )
            else:
                self.reply(
                    chat_name,
                    "Command !{0} does not exist.".format(cleaned_command)
                )

        # Not a system command, continue attempting to parse
        else:
            for i in body_tokens:
                word = i.lower()
                if word == "!fortune":
                    # TODO
                    pass
                elif word == "!excuse":
                    self.reply(chat_name, self.excuses.get())

                elif word == "!8ball":
                    self.reply(chat_name, self.eightball.get())

                elif word[0] == "!":
                    self.reply(chat_name, self.commands.get(word[1:]))

    def reply(self, chat_name, message):
        string = "CHATMESSAGE " + chat_name + " " + message
        self.bus.Invoke(string)
