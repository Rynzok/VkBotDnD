from casts import Cast
from work_with_db import write_to_db, casts_read_from_db


class Alias:

    def __init__(self):
        self.id = None
        self.name = None
        self.string = None
        self.list_cast = []

    def create_from_string(self, list_string):
        self.string = " ".join(list_string)
        for string in list_string:
            command = Cast(string)
            command.create_from_string()
            self.list_cast.append(command)

    def create_from_db(self, name):
        list_string, string = casts_read_from_db(name)
        self.string = string
        for string in list_string:
            command = Cast(string[1])
            command.create_from_db(string)
            self.list_cast.append(command)

    def create_name(self, name):
        self.name = name

    def sum(self):
        result = 0
        some_text = ""
        for cast in self.list_cast:
            res, text_box = cast.calculation()
            result += res
            some_text += text_box + f"\n"

        text = f"Суммарный результат: {result} \n" + some_text

        return text

    def write_to_db(self):
        write_to_db(self.name, self.string, self.list_cast)
