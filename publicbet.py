#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import time
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Filters
import diamond_db
from tenacity import retry, wait_fixed, stop_after_attempt
import threading

lock = threading.Lock()

TOKEN = ''

bot = telebot.TeleBot(token=TOKEN, num_threads=15)

creators = []
betting = {}
partners = {}
grouplist = {}
teams = ['roosta', 'ferghe', 'ghatel', 'atash', 'gorg', 'monafegh']
helpme = '''᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥
به بخش راهنمای ورولف بت خوش آمدید🐾
❗️توضیحات :

❕این ربات به این گونه است که شرط بندی برای چند بازی در روز باز میشود و شما میتوانید روی آن بازی ها شرط بسته و الماس بدست آورید💎

❕این ربات دارای ضریب می باشد و به شما ضریبی ارائه میدهد که در صورت برد شما در شرط بندی ، ضریب در مقدار الماس شرط بندی شده ضرب خواهد شد و به تعداد الماس های شما اضافه میشود💎

❕شما میتوانید با ثبت نام در ربات (/registerme) و عضو شدن در کانال میتوانید الماس بدست آورید💎

❗️دستورات بات :

/getstate :
شما با استفاده از این دستور میتوانید آمار کامل بت های خود را مشاهده کنید🐾

/wallet :
شما با استفاده از این دستور میتوانید تعداد الماس های خود را مشاهده کنید🐾

/bestbet :
شما با استفاده از این دستور میتوانید لیست بهترین بت باز های گروه را مشاهده کنید🐾

/betting :
شما با استفاده از این دستور در زمان باز شدن شرط بندی میتوانید شرط خود را ببندید🐾

/registerme :
شما با استفاده از این دستور میتوانید در ربات ثبت نام کنید و الماس رایگان بدست آورید🐾

❗️دستورات مدیریتی ربات :

plus number 💎 , sub number 💎 :
شما یا استفاده از این دستور به صورت ریپلای روی شخص مورد نظر میتوانید الماس به او افزوده یا کم کنید🐾
مثال :
plus 10 💎 | sub 10 💎

addadmin , remadmin :
کریتور با استفاده از این دستور میتواند ادمین اضافه یا کم کند🐾

/beton , /betoff :
شما با استفاده از این دستور میتوانید بت را روشن یا خاموش کنید🐾

/result team :
شما پس از پایان بازی اییکه شرط بندی روی آن بوده با استفاده از این دستور میتوانید تیم برنده را مشخص کنید تا ربات الماس هارا به شرکت کنندگان بدهد🐾
مثال:
📍درصورت برد فرقه
/result ferghe
📍درصورت برد روستا
/result roosta
📍درصورت برد گرگ
/result gorg
📍درصورت برد قاتل
/result ghatel
📍درصورت برد منافق
/result monafegh
📍درصورت برد آتش زن
/result atash

channel : @WereWolf_Bet 💎

༆𝒎𝒐𝒔𝒕 𝒃𝒆 𝒂 𝒍𝒖𝒑𝒊𝒏𝒆 𝒈𝒖𝒚 𝒕𝒐 𝒃𝒆 𝒂𝒍𝒊𝒗𝒆 💎
᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥'''


def check_admin(chat_id, user_id):
    admins = diamond_db.load_admin(chat_id)
    if user_id in admins:
        return True
    else:
        return False


def check_cr(chat_id, user_id):
    cr = diamond_db.load_creator(chat_id)
    if user_id in cr or user_id in creators:
        return True
    else:
        return False


def add_betting(chat_id):
    global betting
    if chat_id not in betting:
        betting.update({chat_id: False})


def add_partners(chat_id):
    global partners
    if chat_id not in partners:
        partners.update({chat_id: []})


def add_grouplist(chat_id):
    global grouplist
    if chat_id not in grouplist:
        try:
            lock.acquire(True)
            if diamond_db.isactive(chat_id):
                grouplist.update({chat_id: []})
            else:
                try:
                    bot.send_message(chat_id, '''🔹برای فعال سازی  ربات برای گروه خود با ایدی زیر در تماس باشید🔹
ID : @GreatAg 🔅''', reply_markup=build_markup3())
                    bot.leave_chat(chat_id)
                except:
                    pass
                return False
        finally:
            lock.release()
    return 1


def build_markup3():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton('⚜Bet channel⚜', url='t.me/WereWolf_Bet'))
    return markup


@bot.message_handler(commands=['active'], func=Filters.user([638994540, 835478580]))
def active_group(message):
    gp = message.text.split(" ")
    try:
        gp_id = gp[1]
    except IndexError:
        bot.reply_to(message, "لطفا آیدی عددی گروه را مقابل دستور قرار دهید")
        return
    try:
        if 8 < len(gp_id) < 16:
            gp_id = int(gp_id)
            result = diamond_db.activegap(gp_id)
            bot.reply_to(message, result)
        else:
            bot.reply_to(message, 'this form : 10 < group id < 16')
            return
    except:
        bot.reply_to(message, 'لطفا ایدی عددی را درست وارد کنید❕')
        return


@bot.message_handler(commands=['list'], func=Filters.user([638994540, 835478580]))
def list(message):
    listgp = diamond_db.getactivegaps()
    listgps = 'لیست گروه ها:'
    numgps = 0
    for i in listgp:
        try:
            gp = bot.get_chat(i).title
            numgps += 1
            listgps += f'\n{numgps}- {gp} (`{i[0]}`)'
        except:
            pass
    bot.send_message(message.chat.id, listgps, parse_mode='markdown')


@bot.message_handler(commands=['deactive'], func=Filters.user([638994540, 835478580]))
def diactive(message):
    whichgap = message.text.split(' ')
    try:
        whichgap = int(whichgap[1])
    except:
        bot.reply_to(message, 'آیدی عددی گروه را جلوی دستور قرار دهید❕')
        return
    result = diamond_db.deactivegap(whichgap)
    bot.reply_to(message, result)
    try:
        partners.pop(whichgap)
    except:
        pass
    try:
        betting.pop(whichgap)
    except:
        pass
    try:
        grouplist.pop(whichgap)
    except:
        pass


@bot.message_handler(regexp='plus', func=Filters.group)
def get_diamond(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    tf = add_grouplist(chat_id)
    if not tf:
        return
    if not message.reply_to_message:
        return
    if not check_admin(chat_id, user_id):
        return
    rep_id = message.reply_to_message.from_user.id
    num = message.text.split(" ")
    try:
        numdiamond = int(num[1])
    except:
        return

    try:
        if num[2] != '💎':
            bot.reply_to(message, 'لطفا اموجی را درست وارد کنید')
            return
    except:
        bot.reply_to(message, 'لطفا دستور را درست وارد کنید')
        return
    diamond_db.add_diamond(chat_id, rep_id, numdiamond)
    bot.reply_to(message,
                 f'''✦| [{message.reply_to_message.from_user.first_name}](tg://user?id={rep_id})
{numdiamond} المـ💎ـاس دریافت کرد ✔️''',
                 parse_mode='Markdown')


@bot.message_handler(regexp='sub', func=Filters.group)
def get_diamond(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    tf = add_grouplist(chat_id)
    if not tf:
        return
    if not message.reply_to_message:
        return
    if not check_admin(chat_id, user_id):
        return
    rep_id = message.reply_to_message.from_user.id
    num = message.text.split(" ")
    try:
        numdiamond = int(num[1])
    except:
        return

    try:
        if num[2] != '💎':
            bot.reply_to(message, 'لطفا اموجی را درست وارد کنید')
            return
    except:
        bot.reply_to(message, 'لطفا دستور را درست وارد کنید')
        return
    inventory = diamond_db.load_diamond(chat_id, rep_id)
    try:
        if numdiamond > round(inventory[0]):
            bot.send_message(user_id, '✦| مقدار وارد شده بیشتر از تعداد کل المـ💎ـاس ها است ✖️')
            return
    except:
        return
    diamond_db.add_diamond(chat_id, rep_id, -1 * numdiamond)
    bot.reply_to(message,
                 f'''✦| [{message.reply_to_message.from_user.first_name}](tg://user?id={rep_id})
{numdiamond} المـ💎ـاس از دست داد ✔️''',
                 parse_mode='Markdown')


@bot.message_handler(regexp='setcreator', func=Filters.user(creators))
def set_cr(message):
    if not message.reply_to_message:
        return
    rep_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    diamond_db.set_creator(chat_id, rep_id)
    bot.reply_to(message,
                 f'✦| [{message.reply_to_message.from_user.first_name}](tg://user?id={rep_id}) با موفقیت به لیست كريتور ها اضافه شد✔️',
                 parse_mode='Markdown')


@bot.message_handler(regexp='remcreator', func=Filters.user(creators))
def set_cr(message):
    if not message.reply_to_message:
        return
    rep_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    diamond_db.rem_creator(chat_id, rep_id)
    bot.reply_to(message,
                 f'✦| [{message.reply_to_message.from_user.first_name}](tg://user?id={rep_id}) با موفقیت از لیست كريتور ها حذف شد✔️',
                 parse_mode='Markdown')


@bot.message_handler(regexp='addadmin', func=Filters.group)
def add_admin(message):
    if not message.reply_to_message:
        return
    rep_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    tf = add_grouplist(chat_id)
    if not tf:
        return
    if not check_cr(chat_id, message.from_user.id):
        return
    if not check_admin(chat_id, rep_id):
        diamond_db.add_admin(chat_id, rep_id)
        bot.reply_to(message,
                     f'✦| [{message.reply_to_message.from_user.first_name}](tg://user?id={rep_id}) با موفقیت به لیست ادمین ها اضافه شد✔️',
                     parse_mode='Markdown')


@bot.message_handler(regexp='remadmin', func=Filters.group)
def rem_admin(message):
    if not message.reply_to_message:
        return
    rep_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    tf = add_grouplist(chat_id)
    if not tf:
        return
    if not check_cr(chat_id, message.from_user.id):
        return
    if not check_admin(chat_id, rep_id):
        bot.reply_to(message,
                     f'✦| [{message.reply_to_message.from_user.first_name}](tg://user?id={rep_id}) ادمين نيست✔️',
                     parse_mode='Markdown')
        return
    diamond_db.rem_admin(chat_id, rep_id)
    bot.reply_to(message,
                 f'✦| [{message.reply_to_message.from_user.first_name}](tg://user?id={rep_id}) با موفقیت از لیست ادمین ها حذف شد✔️',
                 parse_mode='Markdown')


@bot.message_handler(commands=['beton'], func=Filters.group)
def beton(message):
    global betting
    user_id = message.from_user.id
    chat_id = message.chat.id
    tf = add_grouplist(chat_id)
    if not tf:
        return
    add_betting(chat_id)
    add_partners(chat_id)
    if not check_admin(chat_id, user_id):
        bot.reply_to(message, '✦| شما ادمین ربات نیستید✖️')
        return
    if betting[chat_id]:
        bot.reply_to(message, '✦| بت فعال است✖️')
    betting[chat_id] = True
    msg = bot.send_message(message.chat.id, '''✦| بت آغاز شد هم اکنون میتوانید با زدن دستور 
/betting
تیم برنده بازی بعد را پیش بینی کنید✔️''')


@bot.message_handler(commands=['betoff'], func=Filters.group)
def bettoff(message):
    global betting
    user_id = message.from_user.id
    chat_id = message.chat.id
    tf = add_grouplist(chat_id)
    if not tf:
        return
    add_betting(chat_id)
    add_partners(chat_id)
    if not check_admin(chat_id, user_id):
        bot.reply_to(message, '✦| شما ادمین ربات نیستید✖️')
        return
    if not betting[chat_id]:
        bot.reply_to(message, '✦| بت غیرفعال است✖️')
    betting[chat_id] = False
    bot.send_message(message.chat.id, '✦| بت با موفقیت غیرفعال شد✔️')


def build_markup(chat_id):
    z1 = round(random.uniform(1.5, 2.5), 1)
    z2 = round(random.uniform(2, 3), 1)
    z3 = round(random.uniform(2.5, 3.5), 1)
    z4 = round(random.uniform(6, 7.5), 1)
    z5 = round(random.uniform(6, 7.5), 1)
    z6 = round(random.uniform(4, 5.5), 1)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('برد روستا👨', callback_data=f'roosta {z1} {z2} {z3} {z4} {z5} {z6} {chat_id}'),
               InlineKeyboardButton('برد فرقه👤', callback_data=f'ferghe {z1} {z2} {z3} {z4} {z5} {z6} {chat_id}'))
    markup.add(InlineKeyboardButton('برد گرگ ها🐺', callback_data=f'gorg {z1} {z2} {z3} {z4} {z5} {z6} {chat_id}'),
               InlineKeyboardButton('برد قاتل🔪', callback_data=f'ghatel {z1} {z2} {z3} {z4} {z5} {z6} {chat_id}'))
    markup.add(InlineKeyboardButton('برد آتش زن🔥', callback_data=f'atash {z1} {z2} {z3} {z4} {z5} {z6} {chat_id}'),
               InlineKeyboardButton('برد منافق👺', callback_data=f'monafegh {z1} {z2} {z3} {z4} {z5} {z6} {chat_id}'))
    markup.add(
        InlineKeyboardButton('✖️مشاهده ضرایب✖️', callback_data=f'zarayeb {z1} {z2} {z3} {z4} {z5} {z6} {chat_id}'))
    return markup


def build_markup1(chat_id):
    markup = InlineKeyboardMarkup()
    url = f'https://t.me/WereWolf_Bet_bot?start={chat_id}'
    markup.add(InlineKeyboardButton('ثبت نام📑', url=url))
    return markup


@bot.message_handler(commands=['betting'], func=Filters.group)
def bet(message):
    global betting
    global partners
    chat_id = message.chat.id
    tf = add_grouplist(chat_id)
    if not tf:
        return
    add_partners(chat_id)
    add_betting(chat_id)
    if not betting[chat_id]:
        bot.reply_to(message, '✦| بت غیرفعال است✖️')
        return
    user_id = message.from_user.id
    if not diamond_db.check_register(chat_id, user_id):
        bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                         text='''✦|برای شروع بت اول باید در ربات ثبت نام کنید✖️''', reply_markup=build_markup1(chat_id))
        return
    if user_id in partners[chat_id]:
        msg = bot.reply_to(message, '✦|امكان مجدد شری بندي براي شما وجود ندارد')
        time.sleep(3)
        try:
            bot.delete_message(chat_id, msg.message_id)
        except:
            pass
        return
    try:
        bot.send_message(user_id, '''بـت آغاز شـــد💥

↲ پیش‌بینـے شما روی برد کدام تیـــم است؟ ↳''', reply_markup=build_markup(chat_id))
    except:
        bot.send_message(chat_id, '✦| ابتدا ربات را استارت کنید و مجدد این دستور را بزنید ✖️')
        return
    if user_id not in partners[chat_id]:
        partners[chat_id].append(user_id)
    msg = bot.reply_to(message, '✦|پیام بت در pv  برای شما ارسال شد ✔️')
    time.sleep(2)
    try:
        bot.delete_message(chat_id, msg.message_id)
    except:
        pass


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global betting
    data = call.data
    user_id = call.from_user.id
    try:
        cht = data.split(' ')
        chat_id = int(cht[7])
        add_betting(chat_id)
        add_partners(chat_id)
    except:
        pass
    if 'check_channel' in data:
        sp = data.split(' ')
        chat = int(sp[1])
        add_betting(chat)
        add_partners(chat)
        if diamond_db.check_channel(chat, user_id):
            bot.answer_callback_query(call.id, '✦| شما از قبل ثبت نام کرده اید✔️')
        else:
            status = bot.get_chat_member(user_id=user_id, chat_id='@WereWolf_Bet').status
            if status == 'member' or status == 'creator' or status == 'administrator':
                diamond_db.save_channels(chat, user_id)
                bot.send_message(user_id, '''✦| تایید عضویت
20 المـ💎ـاس دیگر بعنوان هدیه از من به شما ارسال شد✔️''')
                diamond_db.add_diamond(chat, user_id, 20)
            else:
                bot.answer_callback_query(call.id, '''✦| ابتدا در کانال عضو شوید و سپس دکمه عضو شدم را انتخاب کنید✖️''',
                                          show_alert=True)

    elif not betting[chat_id]:
        bot.answer_callback_query(call.id, '✦| بت غیرفعال است✖️')
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        return
    elif 'zarayeb' in data:
        dataa = data.split(' ')
        msg = f'''ضرایب بت برای شما:
برد روستا👨 : {dataa[1]}
برد فرقه👤 : {dataa[2]}
برد گرگ🐺 : {dataa[3]}
برد آتش زن🔥 : {dataa[4]}
برد قاتل🔪 : {dataa[5]}
برد منافق👺 : {dataa[6]}'''
        bot.answer_callback_query(call.id, msg, show_alert=True)
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
        markup.add('cancel✖️')
        msg = bot.send_message(user_id, '''✦| با موفقیت ثبت شد✔️
از چند المـ💎ـاس برای این بت استفاده میکنید؟''',
                               reply_markup=markup)
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        zaribs = data.split(' ')
        if 'roosta' in data:
            zarib = zaribs[1]
        elif 'ferghe' in data:
            zarib = zaribs[2]
        elif 'gorg' in data:
            zarib = zaribs[3]
        elif 'atash' in data:
            zarib = zaribs[4]
        elif 'ghatel' in data:
            zarib = zaribs[5]
        elif 'monafegh' in data:
            zarib = zaribs[6]

        chat_id = int(zaribs[7])
        try:
            bot.register_next_step_handler(msg, savediamonds, zaribs[0], zarib, chat_id)
        except:
            bot.send_message(call.message.chat.id, 'لطفا مجددا تلاش كنيد')


def savediamonds(message, data, zarib, chat_id):
    global partners
    user_id = message.from_user.id
    add_partners(chat_id)
    add_betting(chat_id)
    if message.text == 'cancel✖️':
        bot.reply_to(message, '''✦| این بت لغو شد
برای شروع بت جدید در گروه دستور
/betting@LupinBet_bot
را بزنید✔️''')
        if user_id in partners[chat_id]:
            partners[chat_id].remove(user_id)
        return
    if not betting[chat_id]:
        bot.send_message(user_id, '✦| بت غیرفعال است✖️')
        return
    try:
        diamond = int(message.text)
        if chat_id == -1001414592689:
            if diamond > 5000:
                msg1 = bot.send_message(user_id, '''سقف شرط بندي 5000 الماس ميباشد
            لطفا عدد زير 5000 وارد كنيد''')
                bot.register_next_step_handler(msg1, savediamonds, data, zarib, chat_id)
                return
        elif diamond > 1000000:
            msg1 = bot.send_message(user_id, '''سقف شرط بندي 1000000 الماس ميباشد
لطفا عدد زير 1000000 وارد كنيد''')
            bot.register_next_step_handler(msg1, savediamonds, data, zarib, chat_id)
            return
        inventory = diamond_db.load_diamond(chat_id, user_id)
        if diamond > round(inventory[0]) or diamond <= 0:
            msg = '✦| تعداد  المـ💎ـاس های شما کافی نیست ✖️'
            dia = diamond_db.load_diamond(chat_id, user_id)
            try:
                msg += f'''\nموجودي شما در حال حاضر : {dia[0]} 💎'''
            except:
                msg += f'''\nموجودي شما در حال حاضر : {0} 💎'''
            bot.send_message(user_id, msg)
            msg1 = bot.send_message(user_id, '✦|یک عدد وارد کنید✔️')
            bot.register_next_step_handler(msg1, savediamonds, data, zarib, chat_id)
        else:
            diamond_db.save_bet(chat_id, user_id, diamond, data, zarib)
            diamond_db.add_diamond(chat_id, user_id, -1 * diamond)
            bot.send_message(user_id, f'''✦| شما با پیش بینی
برد {translatee(data)} و تعداد {diamond} المـ💎ـاس
با ضریب {zarib}
 وارد بت شدید ✔️''')
    #             bot.send_message(chat_id, f'''✦| [{message.from_user.first_name}](tg://user?id={user_id})
    # با پیش بینی برد {translatee(data)} و تعداد {diamond} المـ💎ـاس با
    #  ضریب {zarib}
    #  وارد بت شد✔️''',
    #                              parse_mode='Markdown')
    except:
        msg2 = bot.send_message(user_id, '✦|یک عدد وارد کنید✔️')
        bot.register_next_step_handler(msg2, savediamonds, data, zarib, chat_id)


@bot.message_handler(commands=['resetdata'], func=Filters.group)
def reset(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if not check_cr(chat_id, user_id):
        return
    diamond_db.resetdata(chat_id)
    bot.send_message(chat_id, 'data reseted seccesfully !')


@bot.message_handler(commands=['result'], func=Filters.group)
def check(message):
    global betting
    global partners
    chat_id = message.chat.id
    tf = add_grouplist(chat_id)
    if not tf:
        return
    add_betting(chat_id)
    add_partners(chat_id)
    if betting[chat_id]:
        bot.reply_to(message, '✦|لطفا ابتدا شرط بندي را ببنديد')
        return
    user_id = message.from_user.id
    if not check_admin(chat_id, user_id):
        bot.reply_to(message, '✦| شما ادمین ربات نیستید✖️')
        return
    try:
        messag = message.text.split(" ")
        winner = messag[1]
    except:
        bot.reply_to(message, '''✦| دستور را همراه با اسم تیم وارد کنید ✖️

به شکل زیر👇🏼
/result gorg''')
        return
    if winner not in teams:
        bot.reply_to(message, '''✦| دستور را همراه با اسم تیم درست وارد کنید ✖️

به شکل زیر👇🏼
/result gorg''')
        return
    msgg = bot.send_message(message.chat.id, '✦| درحال بررسي...')
    msg = '•| لــیــســـت نــهـایـی شـرط بـنـدی |•'
    load = diamond_db.winners(chat_id, winner)
    users = load[0]
    diamond = load[1]
    zarib = load[2]
    msg += '\nᴡɪɴ🐾'
    for i, user in enumerate(users, start=0):
        try:
            bot.send_message(user,
                             f'''✦|تبریک 👍🏻
شما بت را بردید و {round(zarib[i] * diamond[i])} المـ💎ـاس بدست آوردید✔️''')
        except:
            pass
        diamond_db.save_record(chat_id, user, winner, zarib[i] * diamond[i], True)
        try:
            x = bot.get_chat_member(chat_id=message.chat.id, user_id=user)
            msg += f'\n[[🎉]]✔️[{x.user.first_name}](tg://user?id={x.user.id}) | +{round(zarib[i] * diamond[i])} 💎 |'
        except:
            pass

    load = diamond_db.losers(chat_id, winner)
    users = load[0]
    diamond = load[1]
    team = load[2]
    j = 0
    msg += '\n'
    msg += '\nʟᴏsᴇ🕸'
    for i, user in enumerate(users, start=0):
        try:
            bot.send_message(user, f'''✦|متاسفم 👎🏾
شما بت را باختید و {diamond[i]} المـ💎ـاس را از دست دادید✖️''')
        except:
            pass
        try:
            diamond_db.save_record(chat_id, user, team[j], diamond[i], False)
        except:
            pass
        try:
            x = bot.get_chat_member(chat_id=message.chat.id, user_id=user)
            msg += f'\n[[🎈]]✖️[{x.user.first_name}](tg://user?id={x.user.id})  | -{round(diamond[i])} 💎 |'
            j += 1
        except:
            j += 1
            pass
    msg += '\n\n/registerme 💎'
    msg += '\n༆𝒎𝒐𝒔𝒕 𝒃𝒆 𝒂 𝒍𝒖𝒑𝒊𝒏𝒆 𝒈𝒖𝒚 𝒕𝒐 𝒃𝒆 𝒂𝒍𝒊𝒗𝒆 💎'
    diamond_db.delete_data(chat_id)
    partners[chat_id].clear()
    try:
        bot.edit_message_text(message_id=msgg.message_id, chat_id=msgg.chat.id, text='✦| كامل شد✔️')
    except:
        pass
    bot.send_message(chat_id, msg, parse_mode='markdown')


@bot.message_handler(commands=['wallet'], func=Filters.group)
def info(message):
    msg = ''
    user_id = message.from_user.id
    chat_id = message.chat.id
    tf = add_grouplist(chat_id)
    if not tf:
        return
    add_betting(chat_id)
    diamond = diamond_db.load_diamond(chat_id, user_id)
    if len(diamond) == 0:
        diamond.append(0)
    msg += f'مقدار الــــمــ💎ــاس شما {diamond[0]}'
    bot.reply_to(message, msg)


@bot.message_handler(commands=['registerme'], func=Filters.group)
def reg(message):
    chat_id = message.chat.id
    tf = add_grouplist(chat_id)
    if not tf:
        return
    add_betting(chat_id)
    bot.send_message(chat_id, '❖برای ثبـت نـام در ربات دکمـه زیر رو بزنیــد❖', reply_markup=build_markup1(chat_id))


def translatee(teamss):
    if teamss == 'ghatel':
        return 'قاتل'
    elif teamss == 'roosta':
        return 'روستا'
    elif teamss == 'gorg':
        return 'گرگ'
    elif teamss == 'atash':
        return 'آتش زن'
    elif teamss == 'ferghe':
        return 'فرقه'
    elif teamss == 'monafegh':
        return 'منافق'


@bot.message_handler(commands=['getstate'], func=Filters.group)
def state(message):
    chat_id = message.chat.id
    tf = add_grouplist(chat_id)
    if not tf:
        return
    add_betting(chat_id)
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        firstname = message.reply_to_message.from_user.first_name
    else:
        user_id = message.from_user.id
        firstname = message.from_user.first_name
    state = diamond_db.load_state(chat_id, user_id)
    bw = diamond_db.stats(chat_id, user_id)
    dia = diamond_db.load_diamond(chat_id, user_id)
    if len(dia) == 0:
        dia.append(0)
    msg = f'sᴛᴀᴛᴇ ғᴏʀ [{firstname}](tg://user?id={user_id})'
    msg += f'''\n`{state[0]}` تـعـداد بت🎰'''
    msg += f'''\n`{state[1]}` تــــعــــداد بــꜛــرد🏆'''
    msg += f'''\n`{state[2]}` تــــعــــداد بـاخـــꜜـت 🕳'''
    if bw[0] is None:
        msg += f'''\n`{0}` بـهـتـریـن بـت ✨'''
    else:
        msg += f'''\n`{bw[0]}` بـهـتـریـن بـت ✨'''
    if bw[1] is None:
        msg += f'''\n`{0}` بـدتـریـن بـت 💥'''
    else:
        msg += f'''\n`{bw[1]}` بـدتـریـن بـت 💥'''
    if state[3] is None:
        msg += f'''\n`{0}` الــــمـــ💎ـاس دریافــت کردی...'''
    else:
        msg += f'''\n`{state[3]}` الــــمـــ💎ـاس دریافــت کردی...'''
    if state[4] is None:
        msg += f'''\n`{0}` الــــمــ💎ــاس از دســت دادی...'''
    else:
        msg += f'''\n`{state[4]}` الــــمــ💎ــاس از دســت دادی...'''
    try:
        msg += f'''\n`{dia[0]}` ✜ موجودی ✜'''
    except:
        msg += f'''\n`{0}` ✜ موجودی ✜'''
    msg += '\n༆𝒎𝒐𝒔𝒕 𝒃𝒆 𝒂 𝒍𝒖𝒑𝒊𝒏𝒆 𝒈𝒖𝒚 𝒕𝒐 𝒃𝒆 𝒂𝒍𝒊𝒗𝒆 💎'
    bot.send_message(chat_id, msg, parse_mode='markdown')


@bot.message_handler(commands=['bestbet'], func=Filters.group)
def best(message):
    chat_id = message.chat.id
    tf = add_grouplist(chat_id)
    if not tf:
        return
    add_betting(chat_id)
    best = diamond_db.get_best(chat_id)
    rank = ['🥇', '🥈', '🥉', '', '', '', '', '', '', '']
    user = best[0]
    diamond = best[1]
    msg = 'ده بــــت باز بــــرتــــر گروه🐾\n'
    j = 1
    for i in user:
        try:
            x = bot.get_chat_member(chat_id=message.chat.id, user_id=i)
            msg += f'\n{rank[j - 1]}[[⭐️]] [{x.user.first_name}](tg://user?id={x.user.id}) | `{diamond[j - 1]}` 💎 |'
            j += 1
        except:
            pass
    msg += '\n\n༆𝒎𝒐𝒔𝒕 𝒃𝒆 𝒂 𝒍𝒖𝒑𝒊𝒏𝒆 𝒈𝒖𝒚 𝒕𝒐 𝒃𝒆 𝒂𝒍𝒊𝒗𝒆 💎'
    bot.send_message(chat_id, msg, parse_mode='Markdown')


def build_markup2(chat_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Bet channel', url='t.me/WereWolf_Bet'))
    markup.add(InlineKeyboardButton('عضو شدم✅', callback_data=f'check_channel {chat_id}'))
    return markup


@bot.message_handler(commands=['start'], func=Filters.private)
def start(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    try:
        text = message.text
        text = text.split(' ')
        chat = text[1]
        if diamond_db.check_register(chat, user_id):
            bot.send_message(user_id, 'شما ثبت نام کرده ایید📑')
        else:
            diamond_db.register(chat, user_id)
            diamond_db.add_diamond(chat, user_id, 20)
            bot.send_message(user_id, '''✦| شما با موفقیت در ربات بت ثبت نام شدید و 20 المـ💎ـاس دریافت کرديد✔️

✦| پلیر عزیز 
با عضو شدن در کانال زیر میتوانید 20 المـ💎ـاس دیگر دریافت کنید✔️'''
                             , reply_markup=build_markup2(chat))

    except IndexError:
        bot.send_message(chat_id, '''᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥
به ربات ورولف بِت خوش آمدید 🐾

تجربه ایی متفاوت برای اولین بار در ورولف💎

شما با استفاده از این ربات قادر خواهید بود روی برد تیم مورد نظر خود شرط بسته و الماس کسب کنید💎

راهنمای ربات : /help 💎

channel : @WereWolf_Bet 💎

 ༆𝒎𝒐𝒔𝒕 𝒃𝒆 𝒂 𝒍𝒖𝒑𝒊𝒏𝒆 𝒈𝒖𝒚 𝒕𝒐 𝒃𝒆 𝒂𝒍𝒊𝒗𝒆 💎
        ᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥''')


@bot.message_handler(commands=['start'], func=Filters.group)
def send_st(message):
    chat_id = message.chat.id
    tf = add_grouplist(chat_id)
    if not tf:
        return
    add_betting(chat_id)
    bot.send_message(chat_id, 'im online!')


@bot.message_handler(func=Filters.private, commands=['help'])
def send_help(message):
    chat_id = message.from_user.id
    try:
        bot.send_message(chat_id, helpme)
    except:
        pass


@bot.message_handler(func=Filters.group, commands=['help'])
def gp_help(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    tf = add_grouplist(chat_id)
    if not tf:
        return
    add_betting(chat_id)
    try:
        bot.send_message(user_id, helpme)
        bot.reply_to(message, '✦|یک پیام در pv  برای شما ارسال شد ✔️')
    except:
        try:
            bot.reply_to(message, '✦| ابتدا ربات را استارت کنید و مجدد این دستور را بزنید ✖️')
        except:
            pass


# @retry(wait=wait_fixed(2), stop=stop_after_attempt(10))
def poll():
    if __name__ == "__main__":
        try:
            # bot.enable_save_next_step_handlers(delay=2)
            # bot.load_next_step_handlers()
            bot.polling(none_stop=True, timeout=234)
        except Exception as e:
            bot.send_message(chat_id=, text=e)
            raise e


poll()

while True:
    pass
