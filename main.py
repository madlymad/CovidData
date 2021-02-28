import os
import re
import locale

from config import initConfig
from config import KEY_VIBER_DB
from db import create_connection, select_covid
from writer import writeData
from data import specialHandler

locale.setlocale(locale.LC_ALL, '')

header = ["ημερομηνία","ημερίσια κρούσματα", "θάνατοι", "κρούσματα συνολικά", "θάνατοι συνολικά", "διασωληνωμένοι", "εξέλθει από ΜΕΘ", "PCR", "Rapid Ag"]
data = []

config = initConfig()
viberDb = config[KEY_VIBER_DB]
print(viberDb)
conn = create_connection(viberDb)
with conn:
    entries = select_covid(conn)
    
    rData = r" (\d+\/\d+\/\d+|\d+(?:\.\d{3})*|κανένα)+"
    for entry in entries:
        #print(entry)
        values = re.findall(rData, entry[0])
        values = values[:9]
        #print(f"{len(values)}:\t{values}")
        values = specialHandler(values)
        data.append(values)

#print(data)
writeData("covid.xlsx", data, header[0], header)