
from datetime import datetime

ZERO_TEXT = 'κανένα'

# Convert data line and handle special cases


def specialHandler(data):
    # Convert none text to number
    if ZERO_TEXT in data:
        data[data.index(ZERO_TEXT)] = 0

    # Clear numbers from dots
    for i in range(len(data)):
        data[i] = numbers(data[i])

    # Convert special dates that not fit the rest of data
    if data[0] == '21/9/2020':
        data.pop(2)  # delete 184
    if data[0] == '8/6/2020':
        data.pop(3)  # delete 4

    # Format dates
    data[0] = dateFormat(data[0])

    # Move tests to proper location when ΜΕΘ is missing
    if len(data) == 7 and int(data[-1]) > 50000:
        data.insert(-1, None)

    # print(f"\t\t{data}")
    # Fill all columns with None
    return data + [None]*(9-len(data))


def numbers(s):
    return str(s).replace('.', '')


def dateFormat(d):
    if len(str(d[d.rfind('/')+1:])) == 4:
        return datetime.strptime(d, '%d/%m/%Y').date()
    else:
        return datetime.strptime(d, '%d/%m/%y').date()
