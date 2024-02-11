from random import randint

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


vk_session = vk_api.VkApi(token="vk1.a.CWtL1EKHPofoTiVrmYKZuSz9x3mvXJp2f7RgRU5HiOZVVwfA7PWPhIt8N4c6TUHt9TwOqkYS4ud40"
                                "-Cv0FyvyZ2F6KlnyVgdhwbLBbxpaBnGuuhj1JT0Tx1WTwxGg2_3YkDsskeCZ_UjU03QluG8g8qjMR-wv"
                                "-Bp6PfUT9-85s8IlOymVF4AU_2lM9HkNJvG6cNz33_tMf9gUQZm8sHx0Q")
vk = vk_session.get_api()
longpool = VkLongPoll(vk_session)


def send_some_msg(id, some_text):
    vk_session.method("messages.send", {"user_id": id, "message": some_text, "random_id": 0})


class Characteristics:
    def __init__(self):
        self.parameters = [[0 for i in range(0, 5)] for j in range(0, 6)]
        self.sym_string = [0 for i in range(0, 6)]
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


def create_characteristic(id):
    new_characteristic = Characteristics()
    strings = ["" for i in range(0, 6)]
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
    vk_session.method("messages.send", {"user_id": id, "message": some_text, "random_id": 0})


for event in longpool.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            id = event.user_id
            if msg == '/help' or msg == '/h':
                send_some_msg(id, "Помощь")
            elif msg == '/s' or msg == '/scores':
                create_characteristic(id)
