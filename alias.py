from casts import Cast
import sqlite3
import uuid


class Alias:

    def __init__(self, list_string):
        self.id = None
        self.name = None
        self.list_cast = []
        for string in list_string:
            self.list_cast.append(Cast(string))

    def create_name(self, name):
        self.name = name
        self.id = uuid.uuid4()

    def sum(self):
        result = 0
        some_text = ""
        for cast in self.list_cast:
            res, text_box = cast.calculation()
            result += res
            some_text += text_box + f"\n"

        text = f"Суммарный результат: {result} \n" + some_text

        return text

    # def write_to_db(self):
    #     connection = sqlite3.connect('my_database.db')
    #     cursor = connection.cursor()
    #
    #     cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS Alias (
    #     id INTEGER PRIMARY KEY,
    #     name TEXT NOT NULL,
    #     )
    #     ''')
    #
    #     cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS Casts (
    #     id INTEGER PRIMARY KEY,
    #     count INTEGER NOT NULL,
    #     facets INTEGER NOT NULL,
    #     bomb INTEGER NOT NULL,
    #     mod INTEGER NOT NULL,
    #     multi INTEGER NOT NULL,
    #     resist INTEGER NOT NULL,
    #     percent INTEGER NOT NULL
    #     FOREIGN KEY(Alias_id) REFERENCES Alias (id)
    #     )
    #     ''')
    #
    #     cursor.execute('INSERT INTO Alias (id ,name) VALUES (?, ?)',
    #                    (self.id, self.name))
    #
    #     for cast in self.list_cast:
    #         cursor.execute('INSERT INTO Casts (count, facets, bomb, mod, multi, resist, percent, Alias_id)'
    #                        ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
    #                        (cast.dict_values['count'], cast.dict_values['facets'], cast.dict_values['bomb'],
    #                         cast.dict_values['mod'], cast.dict_values['multi'], cast.dict_values['resist'],
    #                         cast.dict_values['percent'], self.id))
    #
    #     connection.commit()
    #     connection.close()
