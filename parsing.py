from bs4 import BeautifulSoup
import requests
import datetime

courses = {'P-LEGO091733':{'name':'0', 'age':[0,0], 'start':'0','finish':'0','place':'0', \
                            'day':'0','time_start':'0','time_finish':'0','info':'0'}}


dictionary = {'Янв':'01','Фев':'02','Март':'03','Апр':'04','Май':'05','Июн':'06','Июл':'07','Авг':'08','Сент':'09','Окт':'10','Нояб':'11','Дек':'12'}
dictionary2 = {'Сб':'Суббота','Вс':'Воскресенье','Пт':'Пятница','Чт':'Четверг','Ср':'Среда','Вт':'Вторник','Пн':'Понедельник'}

def parsing():
    
    html = requests.get("https://crushpro.ru/schedule/")
    soup = BeautifulSoup(html.text, 'lxml')
    
    div = soup.find_all('div', {'class': 'c-infoblock__collapse-wrapper panel panel-default'})
    
    for j in div:

        args_dirty = []

        for i in j.find_all('span'):
            if i.string is not None:
                #print(i.string)
                args_dirty.append(str(i.string))

        if len(args_dirty) > 13:
            del(args_dirty[12::])
        
        if len(args_dirty) == 12:
            args_dirty.insert(1, '')
        
        if len(args_dirty) < 8:
            continue
        
        d_id = args_dirty[10]
        d_st = args_dirty[5] + ' ' + args_dirty[6] + ' 2017'
        d_fin = args_dirty[7] + ' ' + args_dirty[8] + ' 2018'
        d_inf = args_dirty[3] + ' ' + args_dirty[4]
        d_age = args_dirty[0].split()[0].split('-') #пока так
        d_day = args_dirty[12].split()[0]
        d_time_st = args_dirty[12].split()[2] # ? было 2
        d_time_fin = args_dirty[12].split()[4] # было 4
        d_place = args_dirty[11]
        d_name = args_dirty[2]
        
        
        courses[d_id] = {}
        courses[d_id]['start'] = d_st
        courses[d_id]['finish'] = d_fin
        courses[d_id]['info'] = d_inf
        courses[d_id]['name'] = d_name
        courses[d_id]['age'] = d_age
        courses[d_id]['place'] = d_place
        courses[d_id]['day'] = d_day
        courses[d_id]['time_start'] = d_time_st
        courses[d_id]['time_finish'] = d_time_fin
    
        for key, value in dictionary.items():
            courses[d_id]['start'] = courses[d_id]['start'].replace(key, value)
            courses[d_id]['finish'] = courses[d_id]['finish'].replace(key, value)
            
        for key, value in dictionary2.items():
            courses[d_id]['day'] = courses[d_id]['day'].replace(key, value)
            
        courses[d_id]['finish'] = datetime.datetime.strptime(courses[d_id]['finish'], "%d %m %Y")
        courses[d_id]['start'] = datetime.datetime.strptime(courses[d_id]['start'], "%d %m %Y")
        
        courses[d_id]['place'] = courses[d_id]['place'].replace('гиназия','гимназия')
        courses[d_id]['place'] = courses[d_id]['place'].replace('Москва','Офис QIWI') #вроде бы

        '''
        print(d_id)
        for i in courses[d_id].items():
            print(i)
        print('-'*70)
        '''
    return courses

parsing()