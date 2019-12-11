# -*- coding: utf-8 -*-
import telebot
import os
import json

bot = telebot.TeleBot("850219369:AAEiyhnQ_Yc4iJXm-4z1kmRfeNAqYZrfupQ")

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('/case')
keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard2.row('/read')
keyreg = telebot.types.ReplyKeyboardMarkup(True, True)
keyreg.row('/reg')


def em_all(eml, pers):
    f = open('users/id_list.txt', 'r')
    s = '404 not found'
    if pers.setdefault('Status') == 'офицер':
        s = 'Приказ отдал '
    elif pers.setdefault('Status') == 'создатель':
        s = 'Сообщение отправил '
    for line in f:
        if int(line) != pers.setdefault('id'):
            try:
                bot.send_message(int(line), eml + '\nP.S\n ' + s + str(pers.setdefault('Obr')) + ' ' +
                                 str(pers.setdefault('Sename')) + '!', reply_markup=keyboard2)
            except:
                print(line)


def check_Code(kod):
    f = open('users/status_kod.txt', 'r')
    for line in f:
        print(line[0:8])
        if kod == line[0:8]:
            if line[8] == '0':
                return 'офицер'
            elif line[8] == '1':
                return 'старшина'
            elif line[8] == '2':
                return 'канцеляр'
            elif line[8] == '3':
                return 'замок'
            elif line[8] == '4':
                return 'комод'
            elif line[8] == '5':
                return 'курсант'
    f.close()


def create_pers(message):
    s = message.text[6:].rsplit(sep=',')
    print(s)
    pers = dict(id=message.from_user.id, Name=s[2], Sename=s[1], Status=check_Code(s[4]), point='1', Groups=s[3],
                Kod=0, obr=s[5])
    with open("users/user_" + str(message.from_user.id) + ".json", "w", encoding="utf-8") as fh:
        fh.write(json.dumps(pers))
        fh.close()
    f = open('users/id_list.txt', 'a')
    f.write('\n' + str(message.from_user.id))
    f.close()
# осталось дохуя! надо сделать: отчет о прочитаном, вывод зарегестрированных, защита от спама, подпправить рассылку


def check_Stat(persSt):
    if persSt == 'старшина' or persSt == 'создатель' or persSt == 'офицер' or persSt == 'канцеляр':
        return True
    return False


def check_json(us_id):
    if os.path.exists("users/user_" + str(us_id) + ".json"):
        return True
    return False


def updateJson(lip, us_id):
    with open("users/user_" + str(us_id) + ".json", "w", encoding="utf-8") as fh:
        fh.write(json.dumps(lip))
        fh.close()


def check_id_list(us_id):
    f = open('users/id_list.txt', 'r')
    for line in f:
        print(str(us_id) + ' ' + str(line))
        if int(line) == int(us_id):
            f.close()
            return False

    f.close()
    return True


def get_user(us_id):
    with open("users/user_" + str(us_id) + ".json", "r", encoding="utf-8") as fh:
        data = json.load(fh)
        fh.close()
        return data


def log(message):
    f = open('text.txt', 'a')
    f.write("<!------!>" + '\n')
    print("<!------!>")
    from datetime import datetime
    valma = str(datetime.today())
    f.write(valma + ' ')
    print(datetime.now())
    f.write("Сообщение от {0} {1} (id = {2}) \n {3} \n".format(message.from_user.first_name,
                                                               message.from_user.last_name,
                                                               str(message.from_user.id), message.text))
    print("Сообщение от {0} {1} (id = {2}) \n {3}".format(message.from_user.first_name,
                                                          message.from_user.last_name,
                                                          str(message.from_user.id), message.text))
    f.close()


@bot.message_handler(commands=['start'])
def start(message):
    if check_id_list(message.from_user.id):
        bot.send_message(message.chat.id, 'Вы не зарегестрированны в системе, используйте /reg, чтобы пройти' +
                                          'регестрацию', reply_markup=keyreg)
    else:
        print(message)
        if check_json(message.from_user.id):
            user = get_user(message.from_user.id)
            print(user)
            bot.send_message(message.chat.id, 'Товарищ ' + str(user.setdefault('obr')) + ' Добро пожаловать в ' +
                             'систему оповещения ' +
                             'командного состава.')
            if user.setdefault('Status') == "офицер":
                bot.send_message(message.chat.id, 'Выберете действие', reply_markup=keyboard1)
            other = dict(point=1)
            user.update(other)
            print(user)
            updateJson(user, message.from_user.id)
    log(message)


@bot.message_handler(commands=['case'])
def case(message):
    pers = get_user(message.from_user.id)
    if (pers.setdefault('point') == 1) and check_Stat(pers.setdefault('Status')):
        bot.send_message(message.from_user.id, 'Введите текст приказа')
        other = dict(point=2)
        pers.update(other)
        print(pers)
        updateJson(pers, message.from_user.id)
        print(pers)


@bot.message_handler(commands=['root'])
def root(message):
    if message.text[6:14] == '12344321':
        bot.send_message(message.chat.id, 'Добро пожаловать Создатель')
    elif message.text[6:14] == '11111111':
        bot.send_message(message.chat.id, 'Добро подаловать, ' + message.from_user.first_name + ' уровень прав 1!\n' +
                         'В данный момент функционал сервиса ограничен, приносим свои извинения!')
    else:
        bot.send_message(message.chat.id, 'Код не опознан введенный код: ' + message.text[6:14])
    print(message)
    log(message)


@bot.message_handler(commands=['reg'])
def reg(message):
    if not check_id_list(message.from_user.id):
        bot.send_message(message.chat.id, 'Вы уже зарегестрированны!')
    else:
        bot.send_message(message.chat.id, 'Добро пожаловать в подсистему регистрации!'
                                          ' Пожалуйста введите данные в формате:\n'
                                          '/regd порядковый_номер,фамилия,имя,номер'
                                          '_группы,код (взять у командира группы '
                                          'или канцеляров),звание.'
                                          ' \n Пример:\n/regd 52,Сечко,Александр,3972,00000000,рядовой')
        log(message)


@bot.message_handler(commands=['regd'])
def regd(message):
    if check_id_list(message.from_user.id):
        create_pers(message)
        bot.send_message(message.chat.id, 'Регистрация прошла успешно!')
    else:
        bot.send_message(message.chat.id, 'Вы уже зарегистрированы')
    log(message)


@bot.message_handler(content_types=['text'])
def send_text(message):
    pers = get_user(message.from_user.id)
    if (pers.setdefault('point') == 2) and check_Stat(pers.setdefault('Status')):
        em_all(message.text, pers)
        bot.send_message(message.chat.id, 'Приказ отправлен')
    if message.text == 'Привет Misu':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
    elif message.text == 'Пока Misu':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    log(message)


bot.polling()
