from random import randint
from dotenv import load_dotenv
import os
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

from alias import Alias
from work_with_db import alias_all_read_db, alis_del_db
import help

load_dotenv()
vk_session = vk_api.VkApi(token=os.getenv('TOKEN'))
vk = vk_session.get_api()
longpool = VkBotLongPoll(vk_session, group_id=224651304, wait=25)
getting_api = vk_session.get_api()


def send_some_msg(chat_id, some_text):
    vk.messages.send(random_id=get_random_id(), peer_id=chat_id, message=some_text)


def get_name(from_id):
    info = getting_api.users.get(user_id=from_id)[0]
    full_name = f"[id{from_id}|{info.get('first_name')}]"
    return full_name


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
    title = list_string[0]
    list_string.pop(0)
    command = Alias()
    command.create_name(title)
    command.create_from_string(list_string)
    command.write_to_db()
    text_box = command.sum()
    return text_box


def alias_read_db():
    list_alias = alias_all_read_db()
    text_box = []
    for i in list_alias:
        text_box.append(f"{i[0]}: {i[1]}")
    some_text = " Список Алиасов: \n"
    for i in text_box:
        some_text += str(i) + "\n"
    return some_text


def alias_release(string):
    list_string = string.split()
    command = Alias()
    command.create_from_db(list_string[1])
    text_box = f"Алиас: {list_string[1]} ({command.string}) \n" + command.sum()
    return text_box


for event in longpool.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_user or event.from_chat and event.message.get('text').lower()[0] == '/':

            msg = event.message.get('text').lower()[1::]
            message = event.obj['message']
            id = message['peer_id']
            name = get_name(event.message.get('from_id'))

            # Вывод информации
            if msg == 'help' or msg == 'h':
                send_some_msg(id, f"{name}, {help.manual}")

            # Создание 6 характеристик персонажа методом броска 4 кубиков
            elif msg == 's' or msg == 'scores':
                send_some_msg(id, f"{name}, {create_characteristic()}")

            # Оброботка вех бросков кубика
            elif (str(msg).find('d') != -1 or str(msg).find('к') != -1)\
                    and str(msg).find('al') == -1 and str(msg).find('ал') == -1:
                try:
                    send_some_msg(id, f"{name}, {calculation_dice(msg)}")
                except:
                    send_some_msg(id, f"{name}, Что-то введено не верно...Но как?")

            # Получение списка всез Алиасов
            elif msg == 'alias' or msg == 'алиасы' or msg == 'al' or msg == 'ал':
                send_some_msg(id, f"{name}, {alias_read_db()}")

            # Удаление Алиаса
            elif str(msg).find('del') != -1:
                send_some_msg(id, f"{name}, {alis_del_db(msg)}")

            # Работа с Алиасами
            elif str(msg).find('al') != -1 or str(msg).find('ал') != -1 and str(msg).find('del') == -1:
                try:
                    # Создание Алиаса
                    if len(str(msg).split()) > 2:
                        send_some_msg(id, f"{name}, {create_alias(msg)}")
                    # Активация Алиаса
                    else:
                        send_some_msg(id, f"{name}, {alias_release(msg)}")
                except:
                    send_some_msg(id, f"{name}, Где-то есть ошибка")

            else:
                send_some_msg(id, f"{name}, Не попало в ifы")

