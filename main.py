from flask import Flask, render_template
from miio import Vacuum
import shelve

with open("vac.txt", "r") as f :
    data = f.read().split("/")
    token = data[1]
    ip = data[0]

vac = Vacuum(ip, token)
app = Flask(__name__)

def getStatus() :
    s = shelve.open("status")
    return s["status"]

def getButtons(state) :
    state = state.lower()

    if state == "charging" :
        return ["start"]
    elif state == "idle" :
        return ["start", "dock"]
    elif state == "cleaning" :
        return ["stop", "pause", "dock"]
    elif state == "spot cleaning" :
        return ["stop", "pause", "dock"]
    elif state == "returning home" :
        return ["stop", "pause"]
    elif state == "paused" :
        return ["start", "dock"]
    elif state == "error" :
        return []
    else :
        return []

#------------------------------------#

@app.get("/")
def main() :
    status = getStatus()
    buttons = getButtons(status.state)

    startVisible = ["hidden","visible"][int("start" in buttons)]
    stopVisible = ["hidden","visible"][int("stop" in buttons)]
    pauseVisible = ["hidden","visible"][int("pause" in buttons)]
    dockVisible = ["hidden","visible"][int("dock" in buttons)]

    return render_template("main.html", battery=status.battery, state=status.state, startVisible=startVisible, stopVisible=stopVisible, pauseVisible=pauseVisible, dockVisible=dockVisible)

@app.post("/start-clean")
def startClean() :
    print("Starting....")
    #vac.start()

    return "ok"

@app.post("/stop-clean")
def stopClean() :
    print("Stopping......")
    #vac.stop()
    
    return "ok"

@app.post("/pause-clean")
def pauseClean() :
    print("Pausing....")
    #vac.pause()
    
    return "ok"

@app.post("/return-dock")
def returnToDock() :
    print("Returing to dock....")
    #vac.home()
    
    return "ok"

app.run(host="0.0.0.0",port=5000)