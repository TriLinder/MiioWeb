from pathlib import Path
from miio import Vacuum
import shelve
import time

with open("vac.txt", "r") as f :
    data = f.read().split("/")
    token = data[1]
    ip = data[0]

vac = Vacuum(ip, token)

while True :
    print("Query")

    try :
        status = vac.status()
    except Exception as e :
        print(e)
        continue

    print("Saving..")
    s = shelve.open("status")
    s["status"] = status
    
    time.sleep(30)