
from datetime import datetime

NOTHING = 'κανένα'

def specialHandler(data):
    if NOTHING in data:
        data[data.index(NOTHING)] = 0

    for i in range(len(data)):
        data[i] = numbers(data[i])

    if data[0] == '21/9/2020':
        data.pop(2) # delete 184
    if data[0] == '8/6/2020':
        data.pop(3) # delete 4
    
    data[0] = dateFormat(data[0])

    if len(data) == 7 and int(data[-1]) > 50000:
        data.insert(-1, None)
    
    #print(f"\t\t{data}")
    return data + [None]*(9-len(data))
    
def numbers(s):
    return str(s).replace('.', '')

def dateFormat(d):
    if len(str(d[d.rfind('/')+1:])) == 4:
        return datetime.strptime(d, '%d/%m/%Y').date()
    else:
        return datetime.strptime(d, '%d/%m/%y').date()