import sqlite3


class EightBall:
    def __init__(self):
        self.connection = sqlite3.connect("8ball.db")
        self.cursor = self.connection.cursor()

    def get(self):
        self.cursor.execute(
            "SELECT content FROM phrases ORDER BY RANDOM() LIMIT 1"
        )
        return self.cursor.fetchone()[0]


class Excuses:
    def __init__(self):
        self.connection = sqlite3.connect("excuses.db")
        self.cursor = self.connection.cursor()

    def get(self):
        self.cursor.execute(
            "SELECT content FROM excuses ORDER BY RANDOM() LIMIT 1"
        )
        return self.cursor.fetchone()[0]


class Commands:
    def __init__(self):
        self.connection = sqlite3.connect("commands.db")
        self.cursor = self.connection.cursor()

    def exists(self, command):
        self.cursor.execute(
            "SELECT EXISTS(SELECT 1 FROM commands WHERE command=? LIMIT 1)",
            (command,)
        )
        return self.cursor.fetchone()[0]

    def get(self, command):
        if self.exists(command):
            self.cursor.execute(
                "SELECT response FROM commands WHERE command=? LIMIT 1",
                (command,)
            )

            return self.cursor.fetchone()[0]

        return "Command not in file!"

    def set(self, command, response):
        if self.exists(command):
            self.cursor.execute(
                "UPDATE commands SET response=? WHERE command=? LIMIT 1",
                (response, command)
            )
        else:
            self.cursor.execute(
                "INSERT INTO commands VALUES (NULL, ?, ?)",
                (command, response)
            )

        self.connection.commit()

    def delete(self, command):
        if self.exists(command):
            self.cursor.execute(
                "DELETE FROM commands WHERE command=? LIMIT 1",
                (command,)
            )

            self.connection.commit()
            return True

        return False

    def list(self):
        self.cursor.execute(
            "SELECT command FROM commands"
        )

        result_list = list()
        for tuple_ in self.cursor.fetchall():
            result_list.append(tuple_[0])

        return result_list
