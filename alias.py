from casts import Cast
import sqlite3


class Alias:

    def __init__(self):
        self.id = None
        self.name = None
        self.list_cast = []

    def create_from_string(self, list_string):
        for string in list_string:
            command = Cast(string)
            command.create_from_string()
            self.list_cast.append(command)

    def create_from_db(self, name):
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM Alias WHERE name = ?", [name])
        alias_id = cursor.fetchone()
        cursor.execute("SELECT * FROM Casts WHERE Alias_id = ?", [alias_id[0]])
        list_string = cursor.fetchall()
        connection.close()
        for string in list_string:
            command = Cast("")
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
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS Alias (id INTEGER PRIMARY KEY,name TEXT NOT NULL)")

        cursor.execute("CREATE TABLE IF NOT EXISTS Casts ("
                       "id INTEGER PRIMARY KEY,"
                       "count INTEGER NOT NULL,"
                       "facets INTEGER NOT NULL,"
                       "bomb INTEGER NOT NULL,"
                       "mod INTEGER NOT NULL,"
                       "multi INTEGER NOT NULL,"
                       "resist INTEGER NOT NULL,"
                       "percent INTEGER NOT NULL,"
                       "Alias_id INTEGER NOT NULL,"
                       "FOREIGN KEY (Alias_id) REFERENCES Alias (id))")

        cursor.execute("INSERT INTO Alias (name) VALUES (?)", [self.name])
        cursor.execute("SELECT LAST_INSERT_ROWID()")
        id = cursor.fetchone()
        print(id[0])
        for cast in self.list_cast:
            cursor.execute("INSERT INTO Casts (count, facets, bomb, mod, multi, resist, percent, Alias_id)"
                           " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (cast.dict_values['count'], cast.dict_values['facets'], cast.dict_values['bomb'],
                            cast.dict_values['mod'], cast.dict_values['multi'], cast.dict_values['resist'],
                            cast.dict_values['percent'], id[0]))

        connection.commit()
        connection.close()
