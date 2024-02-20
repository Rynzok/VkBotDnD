from random import randint
from dotenv import load_dotenv
import os
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

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


def sum_dice(msg):
    border = 0
    for i in range(len(msg)):
        if msg[i] == 'd' or msg[i] == 'к':
            border = i
            break
    if border == 0:
        return "Ошибка. Нет ключевой буквы d или k"
    else:
        count = int(msg[:border])
        facets = msg[(border + 1):]
        if facets == "":
            facets = 20
        else:
            facets = int(facets)
        strings = [0 for _ in range(0, count)]
        for i in range(len(strings)):
            strings[i] = randint(0, facets)
        text_box = f"бросок {msg}: {sum(strings)} ("
        for string in strings:
            text_box += str(string) + " + "
        text_box = text_box[:-3]
        text_box += ")"
        return text_box


for event in longpool.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me and event.text.lower()[0] == '/':
            msg = event.text.lower()[1::].replace(" ", "")
            id = event.user_id
            if msg == 'help' or msg == 'h':
                send_some_msg(id, "Помощь")
            # Создание 6 характеристик персонажа методом броска 4 кубиков
            elif msg == 's' or msg == 'scores':
                send_some_msg(id, f"{create_characteristic()}")
            # Бросок кубика 20 граней
            elif msg == 'd' or msg == 'к':
                send_some_msg(id, f"Бросок d: {randint(1, 20)}")
            # Бросок процентного кубика
            elif msg == 'd%' or msg == 'к%':
                send_some_msg(id, f"Бросок d%: {randint(0, 100)}%")
            # Бросок кубика с заданым числом граней
            elif msg[0] == 'd' or msg[0] == 'к' and msg[1] != '%' and msg[1] != "":
                send_some_msg(id, f"Бросок d{msg[1::]}: {randint(0, int(msg[1::]))}")
            # Сумма бросков
            elif msg[0] != 'd' and msg[0] != 'к':
                try:
                    send_some_msg(id, f"{sum_dice(msg)}")
                except:
                    send_some_msg(id, f"Lol")
