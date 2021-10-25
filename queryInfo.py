from pathlib import Path
from miio import Vacuum
import shelve
import time
import sys

def query(failed) :
    print("Query")

    if failed > 0 :
        print(failed)

    if failed > 5 :
        return "failed"

    s = shelve.open("status")

    if failed == 0 :
        try :
            if time.time() - s["lastRequest"] > 200 :
                print("Waiting extra..")
                time.sleep(90)
        except KeyError :
            print("First start?")

    try :
        status = vac.status()
    except Exception as e :
        print(e)
        return query(failed+1)
    
    try :
        consumables = vac.consumable_status()
    except Exception as e :
        print(e)
        return query(failed+1)
    
    try :
        carpet = vac.carpet_mode()
    except Exception as e :
        print(e)
        return query(failed+1)

    print("Saving..")
    s["status"] = status
    s["carpet"] = carpet
    s["consumables"] = consumables
    s["lastCheck"] = int(time.time())

try :
    with open("vac.txt", "r") as f :
        data = f.read().split("/")
        token = data[1]
        ip = data[0]
except FileNotFoundError :
    print("Please complete the setup..")
    input("Press [ENTER] to quit..")
    sys.exit()


vac = Vacuum(ip, token)

if __name__ == "__main__" :
    while True :
        query(0)
        time.sleep(30)