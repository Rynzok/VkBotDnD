from random import randint
from dotenv import load_dotenv
import os
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from alias import Alias
import sqlite3

load_dotenv()
vk_session = vk_api.VkApi(token=os.getenv('TOKEN'))
vk = vk_session.get_api()
longpool = VkLongPoll(vk_session)


def send_some_msg(id, some_text):
    vk_session.method("messages.send", {"user_id": id, "message": some_text, "random_id": 0})


class Characteristics:
    def __init__(self):
        self.parameters = [[0 for _ in range(0, 5)] for _ in range(0, 6)]
        self.sym_string = [0 for _ in range(0, 6)]
        for i in range(6):
            for j in range(5):
                if j == 4:
                    self.parameters[i][j] = randint(1, 4)
                else:
                    self.parameters[i][j] = randint(1, 6)
                if j == 4:
                    self.sym_string[i] -= self.parameters[i][j]
                else:
                    self.sym_string[i] += self.parameters[i][j]


def create_characteristic():
    new_characteristic = Characteristics()
    strings = ["" for _ in range(0, 6)]
    for j in range(6):
        strings[j] = f"{new_characteristic.sym_string[j]} ("
        for i in range(5):
            if i != 4 and i != 3:
                strings[j] = strings[j] + str(new_characteristic.parameters[j][i]) + " + "
            else:
                if i == 3:
                    strings[j] = strings[j] + str(new_characteristic.parameters[j][i]) + " - "
                else:
                    strings[j] = strings[j] + str(new_characteristic.parameters[j][i]) + ")"

    text_box = ""
    for string in strings:
        text_box += string + "\n"

    some_text = f"Сгенерированные характиристики:\n {text_box}"
    return some_text


def calculation_dice(string):
    command = Alias()
    command.create_from_string(string.split())
    text_box = command.sum()
    return text_box


def create_alias(string):
    list_string = string.split()
    list_string.pop(0)
    name = list_string[0]
    list_string.pop(0)
    command = Alias()
    command.create_name(name)
    command.create_from_string(list_string)
    command.write_to_db()
    text_box = command.sum()
    return text_box


def alias_read_db():
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM Alias")
    # text_box = "".join(cursor.fetchall())
    text_box = []
    for i in cursor.fetchall():
        text_box.append(i[0])
    some_text = " Список Алиасов: \n"
    for i in text_box:
        some_text += str(i) + "\n"

    connection.close()
    return some_text


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


def alias_release(string):
    list_string = string.split()
    command = Alias()
    command.create_from_db(list_string[1])
    text_box = f"Алиас: {list_string[1]} \n" + command.sum()
    return text_box


for event in longpool.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me and event.text.lower()[0] == '/':
            msg = event.text.lower()[1::]
            id = event.user_id

            if msg == 'help' or msg == 'h':
                send_some_msg(id, "Помощь")

            # Создание 6 характеристик персонажа методом броска 4 кубиков
            elif msg == 's' or msg == 'scores':
                send_some_msg(id, f"{create_characteristic()}")

            # Оброботка вех бросков кубика
            elif str(msg).find('d') != -1 and str(msg).find('al') == -1:
                try:
                    send_some_msg(id, f"{calculation_dice(msg)}")
                except:
                    send_some_msg(id, f"Что-то введено не верно...Но как?")

            elif msg == 'alias':
                send_some_msg(id, f"{alias_read_db()}")

            elif msg != 'alias' and str(msg).find('alias') != -1 and str(msg).find('del') == -1:
                send_some_msg(id, f"{alias_release(msg)}")

            elif str(msg).find('del') != -1:
                send_some_msg(id, f"{alis_del_db(msg)}")

            elif str(msg).find('al') != -1:
                # try:
                send_some_msg(id, f"{create_alias(msg)}")
                # except:
                #     send_some_msg(id, f"БД пошло по пизде")


