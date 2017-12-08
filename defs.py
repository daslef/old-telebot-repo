import datetime
import re
from parsing import parsing

today = datetime.datetime.today()
week = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']

def teacher_scheduler(text):
    
    x = {}
    y = ''
    courses = parsing()
    
    for course in courses:
        if courses[course]['place'] == text and courses[course]['start'] < today < courses[course]['finish']:
            x[course] = courses[course]
    
    for i in week:
        y += (i + ":\n")
        for j in x:
            if x[j]['day'] == i:
                y += "{}\t{} ({}-{} лет) {}-{}\n".format(j, x[j]['name'], x[j]['age'][0], x[j]['age'][1], x[j]['time_start'], x[j]['time_finish'])
    #print(y)
    return(y + '\n\tДля возврата в стартовое меню нажмите /start')
    
def pupil_scheduler(a,b):
    
    x = {}
    y = ''
    
    courses = parsing()
    
    for course in courses:
        if courses[course]['place'] == a and (courses[course]['name'] == b or 'Unity' in b and re.search(r".*Unity", courses[course]['name']) is not None) and courses[course]['start'] < today < courses[course]['finish']:
            x[course] = courses[course]
    
    for i in week:
        y += (i + ":\n")
        for j in x:
            if x[j]['day'] == i:
                y += "{}\t{} ({}-{} лет) {}-{}\n".format(j, x[j]['name'], x[j]['age'][0], x[j]['age'][1], x[j]['time_start'], x[j]['time_finish'])
    #print(y)
    #reg = re.findall(r"[А-Я]+?.*:\s[PS]-.*\d\s", y, re.DOTALL)
    #print(reg)      
    
    if len(y) < 70:
        return("К сожалению на этой площадке выбранный Вами курс не проводится\nНажмите /start и попробуйте другую площадку")
    else:
        return(y + '\n\tДля возврата в стартовое меню нажмите /start' )


def check_places(a):
    
    x = []
    i = ''
    
    courses = parsing()
    
    '''
    for course in courses:
        print(courses[course].values()) '''
    
    for course in courses:
        if (courses[course]['name'] == a or 'Unity' in a and re.search(r".*Unity", courses[course]['name']) is not None or a =='Анимация' and courses[course]['name'] == 'Анимация Stop Motion') and courses[course]['start'] < today < courses[course]['finish'] and courses[course]['place'] not in x:
            x.append(courses[course]['place'])
    
    i = '\n'.join(x)
    #print(i.count('\n'))
    
    return(i)