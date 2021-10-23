from flask import Flask, render_template, request, redirect
from miio import Vacuum
import queryInfo
import shelve
import time

with open("vac.txt", "r") as f :
    data = f.read().split("/")
    token = data[1]
    ip = data[0]

vac = Vacuum(ip, token)
app = Flask(__name__)

def getStatus() :
    s = shelve.open("status")
    return s["status"]

def getConsumables() :
    s = shelve.open("status")
    return s["consumables"]

def getButtons(state) :
    state = state.lower()

    if state == "charging" :
        return ["start"]
    elif state == "idle" :
        return ["start", "dock"]
    elif state == "charger disconnected" :
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

def queryStatus() :
    print("Query")
    try :
        status = vac.status()
    except Exception as e :
        print(e)
        return "failed"
    
    s = shelve.open("status")
    s["status"] = status
    print(status.state)

#------------------------------------#

@app.get("/")
def main() :
    status = getStatus()
    buttons = getButtons(status.state)

    startVisible = ["hidden","visible"][int("start" in buttons)]
    stopVisible = ["hidden","visible"][int("stop" in buttons)]
    pauseVisible = ["hidden","visible"][int("pause" in buttons)]
    dockVisible = ["hidden","visible"][int("dock" in buttons)]

    error = status.error
    if error == "No error" :
        error = ""

    return render_template("main.html", battery=status.battery, state=status.state, error=error, startVisible=startVisible, stopVisible=stopVisible, pauseVisible=pauseVisible, dockVisible=dockVisible)

@app.get("/extra")
def extra() :
    c = getConsumables()
    s = getStatus()

    return render_template("extra.html", filter_used=c.filter, filter_left=c.filter_left, mainb_used=c.main_brush, mainb_left=c.main_brush_left, sideb_used=c.side_brush, sideb_left=c.side_brush_left, fanspeed=s.fanspeed)

#------------------------------------#

@app.post("/start-clean")
def startClean() :
    print("Starting....")
    #vac.start()

    time.sleep(1)
    queryStatus()

    return "ok"

@app.post("/stop-clean")
def stopClean() :
    print("Stopping....")
    vac.stop()
    
    time.sleep(1)
    queryStatus()

    return "ok"

@app.post("/pause-clean")
def pauseClean() :
    print("Pausing....")
    vac.pause()
    
    time.sleep(1)
    queryStatus()

    return "ok"

@app.post("/return-dock")
def returnToDock() :
    print("Returing to dock....")
    vac.home()
    
    time.sleep(1)
    queryStatus()

    return "ok"

@app.post("/set-fanspeed")
def setFanspeed() :
    fanspeed = str(request.form["fanspeed"])
    try :
        vac.set_fan_speed(fanspeed)
    except :
        pass
    
    time.sleep(1)
    queryStatus()

    return redirect("/extra")

app.run(host="0.0.0.0",port=5000,threaded=True)