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


class Cast:

    def __init__(self, string):
        self.dict_values = {'count': 1, 'facets': 20, 'bomb': 0, 'mod': 0, 'multi': 1, 'resist': 0, 'percent': 0}
        self.command = string
        list_symbols = ['d', '%', '!', '+', 'x', 'r']
        list_characters = []
        list_key = ['count', 'facets']

        # Получаем список ключевых символов котороые есть в строке
        for i in list_symbols:
            if string.find(i) != -1:
                list_characters.append(i)

        for i in list_characters:
            if i == '!':
                list_key.append('bomb')
            elif i == '+':
                list_key.append('mod')
            elif i == 'x':
                list_key.append('multi')
            elif i == 'r':
                list_key.append('resist')
            elif i == '%':
                list_key.append('percent')

        list_characters.append('z')
        string = string + 'z'

        buff = ""
        j = 0
        for i in range(len(string)):
            buff += string[i]
            if buff[-1] == list_characters[j]:
                self.set_values(list_key[j], buff[:-1])
                j += 1
                buff = ""

    def set_values(self, key, value):
        if value != '':
            self.dict_values[key] = int(value)
        else:
            if key == 'count':
                self.dict_values[key] = 1
            elif key == 'facets':
                self.dict_values[key] = 20
            elif key == 'bomb':
                self.dict_values[key] = 1
            elif key == 'resist':
                self.dict_values[key] = 1
            elif key == 'multi':
                self.dict_values[key] = 1
            elif key == 'percent':
                self.dict_values[key] = 1
            else:
                self.dict_values[key] = 0

    def calculation(self):
        cubes = [0 for _ in range(self.dict_values['count'])]

        if self.dict_values['percent'] == 1:
            self.set_values('facets', 100)

        for i in range(self.dict_values['count']):
            cubes[i] = randint(0, self.dict_values['facets'])
            if i < self.dict_values['bomb'] and cubes[i] == self.dict_values['facets']:
                cubes.append(randint(0, self.dict_values['facets']))

        result = (sum(cubes) + self.dict_values['mod']) * self.dict_values['multi']
        if self.dict_values['resist'] == 1:
            result = result / 2

        text_box = f"Бросок {self.command}: {result} ("
        if self.dict_values['resist'] == 1:
            text_box += "половина от "
        for i in cubes:
            text_box += str(i) + " + "
        if self.dict_values['mod'] != 0:
            text_box += str(self.dict_values['mod'])
        else:
            text_box = text_box[:-2]
        if self.dict_values['multi'] != 1:
            text_box += f" помноженное на {self.dict_values['multi']})"
        else:
            text_box += ")"

        return result, text_box


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
    command = Cast(string)
    result, text_box = command.calculation()
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
            # Оброботка вех бросков кубика
            elif str(msg).find('d') != -1:
                try:
                    send_some_msg(id, f"{calculation_dice(msg)}")
                except:
                    send_some_msg(id, f"Что-то введено не верно...Но как?")
