from pathlib import Path
from miio import Vacuum
import shelve
import time

def query(failed) :
    print("Query")

    if failed > 5 :
        return "failed"

    try :
        status = vac.status()
    except Exception as e :
        print(e)
        query(failed+1)
    
    try :
        consumables = vac.consumable_status()
    except Exception as e :
        print(e)
        query(failed+1)
    
    try :
        carpet = vac.carpet_mode()
    except Exception as e :
        print(e)
        query(failed+1)

    print("Saving..")
    s = shelve.open("status")
    s["status"] = status
    s["carpet"] = carpet
    s["consumables"] = consumables

with open("vac.txt", "r") as f :
    data = f.read().split("/")
    token = data[1]
    ip = data[0]

vac = Vacuum(ip, token)

if __name__ == "__main__" :
    while True :
        query(0)
        time.sleep(15)