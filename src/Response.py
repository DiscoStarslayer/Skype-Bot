from PhraseDatabases import EightBall, Excuses, Commands
from collections import defaultdict
from pymarkovchain import MarkovChain


def _db_factory():
    return defaultdict(_one_dict)


def _one():
    return 1.0


def _one_dict():
    return defaultdict(_one)


class ResponseGenerator:

    def __init__(self, bus):
        self.bus = bus
        self.eightball = EightBall()
        self.excuses = Excuses()
        self.commands = Commands()
        self.chain = MarkovChain("./markovdb")
        self.chain.db = _db_factory()
        with open("markovsource", "r") as markov_file:
            self.chain.generateDatabase(markov_file.readline())

    def generate_response(self, chat_name, body):
        # Tokenize body
        body_tokens = body.lower().split(" ")
        # Important commands can only be run if line is started with the word
        command = body_tokens[0]

        if command == '!create':
            new_command = body_tokens[1]
            response_index = body.find(new_command) + len(new_command) + 1
            response = body[response_index:]
            self.commands.set(new_command, response)

            self.reply(chat_name, "Command !{0} created.".format(new_command))

        elif command == "!list":
            string = ""
            for command_ in self.commands.list():
                string += "!{0} ".format(command_)

            self.reply(chat_name, string)

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
            for token in body_tokens:
                if token == "!fortune":
                    # TODO
                    pass
                elif token == "!excuse":
                    self.reply(chat_name, self.excuses.get())

                elif token == "!8ball":
                    self.reply(chat_name, self.eightball.get())

                elif token == "tase":
                    self.reply(chat_name, self.chain.generateString())

                elif token[0] == "!":
                    self.reply(chat_name, self.commands.get(token[1:]))

    def reply(self, chat_name, message):
        string = "CHATMESSAGE " + chat_name + " " + message
        self.bus.Invoke(string)
