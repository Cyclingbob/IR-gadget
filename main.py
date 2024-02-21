from machine import Pin
import time

irled = Pin(15, Pin.OUT)
irinpt = Pin(1, Pin.IN)

rbtn = Pin(16, Pin.IN, Pin.PULL_UP)
gbtn = Pin(17, Pin.IN, Pin.PULL_UP)

gcode = []
rcode = []
startTimeStamp = -1

class Event:
  def __init__(self, time, state):
    self.time = time
    self.state = state

lastEvent = None
recording = False
running = False
recordingType = -1

while True:
  if rbtn.value() == 0:
    if len(rcode) == 0:
      recording = True
      running = False
      lastEvent = None
      recordingType = 1
      rcode = []
      print("Recording Red...")
    else:
      print("Playing...")
      lastTime = 0

      for event in rcode:
        time.sleep_us((event.time - lastTime))
        lastTime = event.time

        if event.state == 0:
          irled.value(1)
        else:
          irled.value(0)

      print("Finished Playing.")
      time.sleep(0.5)

  if gbtn.value() == 0:
    if len(gcode) == 0:
      recording = True
      running = False
      lastEvent = None
      recordingType = 0
      gcode = []
      print("Recording Green...")
    else:
      print("Playing...")
      lastTime = 0

      for event in gcode:
        time.sleep_us((event.time - lastTime))
        lastTime = event.time

        if event.state == 0:
          irled.value(1)
        else:
          irled.value(0)

      print("Finished Playing.")
      time.sleep(0.5)

  while recording:
    val = irinpt.value()
    currentTime = time.ticks_us()

    if lastEvent == None:
      if val == 0:
        startTimeStamp = currentTime
        e = Event(0, 0)
        running = True

        if recordingType == 0:
          gcode.append(e)
        elif recordingType == 1:
          rcode.append(e)

        lastEvent = e
    else:
      if val != lastEvent.state:
        e = Event(currentTime - startTimeStamp, val)
        lastEvent = e

        if recordingType == 0:
          gcode.append(e)
        elif recordingType == 1:
          rcode.append(e)

    if currentTime - startTimeStamp > 1_000_000 and running == True:
      recording = False
      print("Finished Recording.")