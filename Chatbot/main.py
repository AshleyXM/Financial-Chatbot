from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config
from telegram.ext import Updater
import re
import random
import telegram
import yfinance as yf
import pandas as pd
import time
import matplotlib.pyplot as plt
import pylab as pl

trainer = Trainer(config.load("config_spacy.yml"))
training_data = load_data('stock.json')
interpreter = trainer.train(training_data)

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)

bot_name='financebot'
bot = telegram.Bot(token='<your telegram token>')
bot.sendMessage(chat_id=911235370,text="Hello,I'm {}.You can ask me any question about stock!".format(bot_name))

intent_responses = {
         "greet":[ "Hi",
                   "Hello",
                   "Howdy",
                   "Hi there"],
         'affirm': ["It's my pleasure to help you:)",
                    'So smart I am:)',
                    'Any other question then?',
                    ':)',
                    'Happy to have helped you:)'],
         'goodbye': ['Bye',
                     'Bye bye',
                     "Good Bye"],
         'name_query': ['My name is {}'.format(bot_name),
                        'They call me {}'.format(bot_name),
                        'You can call me {}'.format(bot_name)],
        }

pattern_list=["I'd like to know (.*)","Could you tell me (.*)","Could you please tell me (.*)","Do you know (.*)","I wonder (.*)","How about (.*)","What's (.*)","What was (.*)"]

updater = Updater(token='1111588934:AAE1Dq9fnTYi8cVGcJvPlYUZeyhya_zB6Jw')
dispatcher = updater.dispatcher

def get_info(message):
    data = interpreter.parse(message)
    intent = data["intent"]["name"]  # 获取消息意图
    entities = data["entities"]  # 获取消息中的实体
    org_list=[]
    entity_dic={}  #存放消息实体的字典
    for ent in entities:
        if ent["entity"]=='org':
            org_list.append(str(ent["value"]))
        else:
            entity_dic[ent["entity"]]=str(ent["value"])
    return intent,org_list,entity_dic

handlable_intent=['highest_price_query','lowest_price_query','price_query','volume_query']

start_date=None
end_date=None
period=None
intent=None
entities={}
org_list=[]
chat_id=None

paint_color=['r','y','','b','g']
dot_style=['-o','--o','-.o','-d','-.s']

def formattime(t):
    array=time.strptime(t,"%Y-%m-%d %H:%M:%S")
    return time.strftime("%Y-%m-%d",array)

def querydate(org,start_date,end_date,index):
    result = ''
    plt.cla()
    flag=None
    for seq,item in enumerate(org):
        date_list = []
        value_list = []
        item = item.upper()
        result += item + ':\n'
        data = yf.download(item, start=start_date, end=end_date)  #data为DataFrame类型
        flag=data.empty
        if flag:
            result+='Sorry,the stock market is CLOSED during the appointed period!\n\n'
        else:
            data_set = data[index]  # data_set为Series类型
            data_len=len(data_set)
            if index=='Close':
                result += 'Date               ' + 'Price' + '\n'
            else:
                result += 'Date               ' + index + '\n'
            for i in range(data_len):
                date=formattime(str(data_set.index[i]))   #date为str类型
                value='%.6f' % data_set.values[i]         #value为str类型
                result+=date+'   '+value+'\n'
                date_list.append(date)
                value=float(value)         #将value转为float类型，方便绘图
                value_list.append(value)
            plt.plot(date_list, value_list, paint_color[seq]+dot_style[seq],label=item)
        result+="\n"
    if flag==False:
        result+="And I'll draw you a graph to illustrate the trend of change more clearly. "
    reply_markup = telegram.ReplyKeyboardHide()
    bot.sendMessage(chat_id=chat_id, text=result, reply_markup=reply_markup)
    if flag == False:
        plt.xlabel('Date', fontsize=14)
        plt.ylabel('Quantity', fontsize=14)
        plt.legend(loc="best")
        pl.xticks(rotation=75)  # 逆时针旋转
        now_time = str(int(time.time()))  # 获取当前时间的时间戳并转换为字符串形式
        plt.savefig("pictures/" + now_time + '.png', dpi=200, bbox_inches='tight')
        bot.sendPhoto(chat_id=chat_id, photo=open('pictures/' + now_time + '.png', 'rb'))

def queryperiod(org,period,index):
    result = ''
    plt.cla()
    flag=None
    for seq, item in enumerate(org):
        date_list = []
        value_list = []
        item = item.upper()
        result += item + ':\n'
        data = yf.download(item, period=period)  # data为DataFrame类型
        flag=data.empty
        if flag:
            result+='Sorry,the stock market is CLOSED during the appointed period!\n\n'
        else:
            data_set = data[index]  # data_set为Series类型
            data_len = len(data_set)
            if index=='Close':
                result += 'Date               ' + 'Price' + '\n'
            else:
                result += 'Date               ' + index + '\n'
            for i in range(data_len):
                date = formattime(str(data_set.index[i]))  # date为str类型
                value = '%.6f' % data_set.values[i]  # value为str类型
                result += date + '   ' + value + '\n'
                date_list.append(date)
                value = float(value)  # 将value转为float类型，方便绘图
                value_list.append(value)
            plt.plot(date_list, value_list, paint_color[seq] + dot_style[seq], label=item)
        result += "\n"
    if flag == False:
        result += "And I'll draw you a graph to illustrate the trend of change more clearly. "
    reply_markup = telegram.ReplyKeyboardHide()
    bot.sendMessage(chat_id=chat_id, text=result, reply_markup=reply_markup)
    if flag == False:
        plt.xlabel('Date', fontsize=14)
        plt.ylabel('Quantity', fontsize=14)
        plt.legend(loc="best")
        pl.xticks(rotation=75)
        now_time = str(int(time.time()))  # 获取当前时间的时间戳并转换为字符串形式
        plt.savefig("pictures/" + now_time + '.png', dpi=200, bbox_inches='tight')
        bot.sendPhoto(chat_id=chat_id, photo=open('pictures/' + now_time + '.png', 'rb'))

def highest_price_query(org, start_date, end_date, period):
    if start_date!=None:
        querydate(org,start_date,end_date,'High')
    else:
        queryperiod(org,period,'High')

def lowest_price_query(org, start_date, end_date, period):
    if start_date != None:
        querydate(org, start_date, end_date, 'Low')
    else:
        queryperiod(org,period,'Low')

def price_query(org,start_date,end_date, period):
    if start_date != None:
        querydate(org, start_date, end_date, 'Close')
    else:
        queryperiod(org,period,'Close')

def volume_query(org,start_date,end_date, period):
    if start_date != None:
        querydate(org, start_date, end_date, 'Volume')
    else:
        queryperiod(org,period,'Volume')

def formatdate(date):  #将日期加一天，根据yfinance.download()函数的start参数的性质来决定的
    beforeArray = time.strptime(date, "%Y-%m-%d")  # 转为时间数组
    timeStamp = int(time.mktime(beforeArray))  # 转为时间戳
    timeStamp+=24*60*60
    afterArray=time.localtime(timeStamp)
    return time.strftime("%Y-%m-%d", afterArray)

def handle(intent,org_list,entities):
    global start_date
    global end_date
    global period
    for key,value in entities.items():
        if key=='start_date':
            start_date=end_date=value
        elif key=='end_date':
            end_date=value
        elif key=='period':
            period=value
    #处理多轮对话
    if len(org_list)==0 and (start_date!=None or period!=None):  #start_date和period二选一即可
        bot.sendMessage(chat_id=chat_id, text="So which stock do you want to ask about?")
    elif len(org_list)!=0 and (start_date==None and period==None):
        custom_keyboard = [['1 day', '5 days', '1 month', '3 months']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.sendMessage(chat_id=chat_id, text="Then for which period do you want to ask about?", reply_markup=reply_markup)
    else:
        if start_date!=None:
            start_date = start_date.replace(" ", "")  # 去掉日期空白符
            start_date = formatdate(start_date)
            end_date = end_date.replace(" ", "")
            end_date = formatdate(end_date)
        if intent == 'highest_price_query':
            highest_price_query(org_list, start_date, end_date, period)
        elif intent == 'lowest_price_query':
            lowest_price_query(org_list, start_date, end_date, period)
        elif intent == 'price_query':
            price_query(org_list, start_date, end_date, period)
        elif intent == 'volume_query':
            volume_query(org_list, start_date, end_date, period)

def chat(bot,update):
    global intent
    global entities
    global org_list
    global start_date
    global end_date
    global chat_id
    global period
    chatid=update.message.chat_id
    chat_id=chatid
    message = update.message.text
    for item in pattern_list:  #去掉不重要信息
        match=re.search(item,message,re.I)
        if match is not None:
            message=match.group(1)
            break
    cur_intent,cur_org_list,cur_entities=get_info(message)  #获取当前消息的意图和实体字典
    if cur_intent=='greet' or cur_intent=='affirm' or cur_intent=='goodbye' or cur_intent=='name_query':
        bot.sendMessage(chat_id=chat_id, text=random.choice(intent_responses[cur_intent]))
    else:
        if cur_intent in handlable_intent:  # 当前意图在可处理意图中时处理当前意图
            intent = cur_intent
            entities = cur_entities.copy()
            org_list = cur_org_list[:]
            start_date = None
            end_date = None
            period=None
        else:  # 当前意图不在可处理意图中时
            if intent in handlable_intent:
                for item in cur_org_list:
                    org_list.append(item)
                for key, value in cur_entities.items():
                    entities[key] = str(value)
            else:  # 不可识别意图，直接赋值
                intent = cur_intent
        handle(intent, org_list, entities)  # 处理消息意图和实体
dispatcher.addTelegramMessageHandler(chat)
updater.start_polling()


