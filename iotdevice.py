import websocket
import thread
import time
import sys
import json


info=False
query={}
sensor={}
def writebysign(write,sensor,value):
    global info
    global query
    info=True
    setDeviceStatus(sensor,value)
    tempq={"method":"put","status":{"sensor" :sensor,"value" :value}}
    return json.dumps(tempq)

def setDeviceStatus(sens,value):
    global sensor
    sensor[sens]=value
    print "==========================\n"
    for key in sensor.keys():
        print "sensor=",key," status=",sensor[key]
    print "==========================\n"

def on_message(ws, message):
    global sensor
    print "[info]from message function:",str(message)
    statinfo=json.loads(message)
    setDeviceStatus(statinfo['sensor'],statinfo['value'])

def on_error(ws, error):
    print(error)

def on_close(ws):
    print "[notify] connection closed"

def on_open(ws):
    def run(*args):
        global query
        global info
        while True:
            if info is True:
                print "[info]ready query",query
                ws.send(query)
                info=False
            else:
                value=raw_input('enter value of sensor=>\n')
                sensor=raw_input('enter sensor id=>\n')
                write="device"
                info=True
                query=writebysign(write,sensor,value)



        #ws.close()
        print("[notify] Thread terminating")
    thread.start_new_thread(run, ())
if __name__ == "__main__":
    websocket.enableTrace(False)
    host = "ws://127.0.0.7/ws?device=CJUQITVIVSXXG3FKSMSL&key=7HSZJU1CTYCZ79K&side=device"
    ws = websocket.WebSocketApp(host,on_message = on_message,on_error = on_error,on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
