import os
import re
import locale

from config import initConfig
from config import KEY_VIBER_DB
from db import create_connection, convid_conversation, select_covid
from writer import writeData
from data import specialHandler
from util import resource_path

locale.setlocale(locale.LC_ALL, '')

header = ["ημερομηνία", "ημερίσια κρούσματα", "θάνατοι", "κρούσματα συνολικά",
          "θάνατοι συνολικά", "διασωληνωμένοι", "εξέλθει από ΜΕΘ", "PCR", "Rapid Ag"]
data = []

config = initConfig()
viberDb = config[KEY_VIBER_DB]
print(f"Reading from {viberDb}.")
conn = create_connection(viberDb)
with conn:

    chatId = convid_conversation(conn)
    entries = select_covid(conn, chatId)

    rData = r" (\d+\/\d+\/\d+|\d+(?:\.\d{3})*|κανένα)+"
    for entry in entries:
        # print(entry)
        values = re.findall(rData, entry[0])
        values = values[:9]
        # print(f"{len(values)}:\t{values}")
        values = specialHandler(values)
        data.append(values)

# print(data)
xlsx = resource_path("covid.xlsx")
writeData(xlsx, data, header[0], header)
print(f"Data saved at {xlsx}")
