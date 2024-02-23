from random import randint
from dotenv import load_dotenv
import os
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from alias import Alias

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
    command = Alias(string.split())
    text_box = command.sum()
    return text_box


def create_alias(string):
    list_string = string.split()
    list_string.pop(0)
    name = list_string[0]
    list_string.pop(0)
    command = Alias(list_string)
    command.create_name(name)
    command.write_to_db()
    text_box = command.sum()
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

            elif str(msg).find('al') != -1:
                try:
                    send_some_msg(id, f"{create_alias(msg)}")
                except:
                    send_some_msg(id, f"БД пошло по пизде")
