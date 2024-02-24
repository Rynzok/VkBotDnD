import sqlite3


def write_to_db(name, command, list_cast):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS Alias "
                   "(id INTEGER PRIMARY KEY,name TEXT NOT NULL UNIQUE, command TEXT NOT NULL)")

    cursor.execute("CREATE TABLE IF NOT EXISTS Casts ("
                   "id INTEGER PRIMARY KEY,"
                   "string TEXT NOT NULL,"
                   "count INTEGER NOT NULL,"
                   "facets INTEGER NOT NULL,"
                   "bomb INTEGER NOT NULL,"
                   "mod INTEGER NOT NULL,"
                   "multi INTEGER NOT NULL,"
                   "resist INTEGER NOT NULL,"
                   "percent INTEGER NOT NULL,"
                   "Alias_id INTEGER NOT NULL,"
                   "FOREIGN KEY (Alias_id) REFERENCES Alias (id))")

    cursor.execute("INSERT INTO Alias (name, command) VALUES (?, ?)", (name, command))
    cursor.execute("SELECT LAST_INSERT_ROWID()")
    alias_id = cursor.fetchone()
    for cast in list_cast:
        cursor.execute("INSERT INTO Casts (string, count, facets, bomb, mod, multi, resist, percent, Alias_id)"
                       " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (cast.command, cast.dict_values['count'], cast.dict_values['facets'], cast.dict_values['bomb'],
                        cast.dict_values['mod'], cast.dict_values['multi'], cast.dict_values['resist'],
                        cast.dict_values['percent'], alias_id[0]))

    connection.commit()
    connection.close()


def casts_read_from_db(name):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT id, command FROM Alias WHERE name = ?", [name])
    alias_id = cursor.fetchone()
    command = alias_id[1]
    cursor.execute("SELECT * FROM Casts WHERE Alias_id = ?", [alias_id[0]])
    list_string = cursor.fetchall()
    connection.close()
    return list_string, command


def alias_all_read_db():
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT name, command FROM Alias")
    list_alias = cursor.fetchall()
    connection.close()
    return list_alias


def alis_del_db(string):
    list_string = string.split()
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM Alias WHERE name = ?", [list_string[1]])
    alias_id = cursor.fetchone()
    cursor.execute("DELETE FROM Alias WHERE name = ?", [list_string[1]])
    cursor.execute("DELETE FROM Casts WHERE Alias_id = ?", [alias_id[0]])
    connection.commit()
    connection.close()
    return "Удаление совершено"
