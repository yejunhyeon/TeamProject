# ex -> https://qiita.com/comachi/items/c494e0d6c6d1775a3748
# ex2 -> https://github.com/Adam-Langley/pybleno
# uuid -> https://www.uuidgenerator.net/version4

from pybleno import *
import binascii

bleno = Bleno()

MY_SERVICE_UUID = '13333333-3333-3333-3333-333333330000'
NOTIFY_CHARACTERISTIC_UUID = '13333333-3333-3333-3333-333333330001'
READ_CHARACTERISTIC_UUID = '13333333-3333-3333-3333-333333330002'
WRITE_CHARACTERISTIC_UUID = '13333333-3333-3333-3333-333333330003'
MOVE_CHARACTERISTIC_UUID = '13333333-3333-3333-3333-333333330004'
STATE_CHARACTERISTIC_UUID = '13333333-3333-3333-3333-333333330005'
DEVICE_NAME = 'WDJ'

counter = 0

########## DATA ##########
_data = array.array('b', [0]*13)
_moveData = array.array('b', [0]*4)
_stateData = array.array('b', [0,0,0,1]) # onoff / onoff / on / off
########## DATA ##########

########## ########## ########## ########## ##########
class NotifyCharacteristic(Characteristic):
  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': NOTIFY_CHARACTERISTIC_UUID,
      'properties': ['notify'],
      'value': None
    })
    self.isSubscribed = True
    self._value = 0
    self._updateValueCallback = None

  def onSubscribe(self, maxValueSize, updateValueCallback):
    print('Characteristic - onSubscribe > ', end='')
    self.isSubscribed = True
    print(self.isSubscribed)
    self._updateValueCallback = updateValueCallback
  def onUnsubscribe(self):
    print('Characteristic - onUnsubscribe > ', end='')
    self.isSubscribed = False
    print(self.isSubscribed)
    self._updateValueCallback = None

class ReadCharacteristic(Characteristic):
  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': READ_CHARACTERISTIC_UUID,
      'properties': ['read','notify'],
      'value': None
    })
    self._value = 0
    self._updateValueCallback = None

  def onReadRequest(self, offset, callback):
    data = array.array('B', [5]*7) # or data = bueffer
    writeUInt8(data, 100, 1)
    writeUInt8(data, 200, 2)
    writeUInt8(data, 100, 3)
    print("onReadRequest")
    print(data)
    callback(Characteristic.RESULT_SUCCESS, data)

class WriteCharacteristic(Characteristic):
  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': WRITE_CHARACTERISTIC_UUID,
      'properties': ['write','notify'],
      'value': None
    })
    self._value = 0
    self._updateValueCallback = None

  def onWriteRequest(self, data, offset, withoutResponse, callback):
    print('onWriteRequest -> ', end='')
    print(data)
    callback(Characteristic.RESULT_SUCCESS)

class MoveCharacteristic(Characteristic):
  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': MOVE_CHARACTERISTIC_UUID,
      'properties': ['write'],
      'value': None
    })
    self._value = 0
    self._updateValueCallback = None

  def onWriteRequest(self, data, offset, withoutResponse, callback):
    print('Move - > ', end='')
    # 0 -> H
    # 1 -> J
    # 2 -> K
    # 3 -> L
    print(data) # move event add
    # _moveData

    # ex) moveData = _moveData
    #     moveData[data]
    #     writeArduino

    #   next -> 
    #   moveData = _moveData
    #   moveData[data] <- nodata, write ok

    # requset -> set , arduino response -> reset
    callback(Characteristic.RESULT_SUCCESS)

class StateCharacteristic(Characteristic):
  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': STATE_CHARACTERISTIC_UUID,
      'properties': ['write'],
      'value': None
    })
    self._value = 0
    self._updateValueCallback = None

  def onWriteRequest(self, data, offset, withoutResponse, callback):
    print('State - > ', end='')
    # 0 -> arduino on / off
    # 1 -> autoFocus on / off
    # 2 -> report start
    # 3 -> report stop
    print(data) # state event add
    choice = int(data.decode())
    # print(choice)
    # print(type(choice))
    global _stateData
    if (choice >= 2):
      if choice == 2:
        _stateData[2] = 1
        _stateData[3] = 0
      if choice == 3:
        _stateData[2] = 0
        _stateData[3] = 1
    elif choice == 0 or choice == 1:
      if choice == 0 and _stateData[choice] == 1:
        print("off reset ~!")
        _stateData = array.array('b', [0,0,0,1])
      else: 
        _stateData[choice] = 1 if _stateData[choice] == 0 else 0
    else:
      pass
    print(_stateData)
    # requset -> set , arduino response -> reset
    callback(Characteristic.RESULT_SUCCESS)

########## ########## ########## ########## ##########

def onStateChange(state):
  print('on -> stateChange: ' + state)
  if (state == 'poweredOn'):
    bleno.startAdvertising(DEVICE_NAME, [MY_SERVICE_UUID])
  else:
    bleno.stopAdvertising()

bleno.on('stateChange', onStateChange)

notifyCharacteristic = NotifyCharacteristic()
readCharacteristic = ReadCharacteristic()
writeCharacteristic = WriteCharacteristic()
moveCharacteristic = MoveCharacteristic()
stateCharacteristic = StateCharacteristic()

def onAdvertisingStart(error):
  print('on -> advertisingStart: ' + ('error ' + error if error else 'success'))
  if not error:
    bleno.setServices([
      BlenoPrimaryService({
        'uuid': MY_SERVICE_UUID,
        'characteristics': [
          notifyCharacteristic,
          readCharacteristic,
          writeCharacteristic,
          moveCharacteristic,
          stateCharacteristic
        ]
      })
    ])

bleno.on('advertisingStart', onAdvertisingStart)
bleno.start()

########## ########## ########## ########## ##########

import time
def appNotify():
  global counter, _data
  counter += 1
  if counter > 99:
    counter = 1
  data = _data
  writeUInt8(data, counter, 0)
  print(">>>> ", end='')
  print(counter)
  global _stateData
  if _stateData[0] == 1:
    if notifyCharacteristic._updateValueCallback:
      notifyCharacteristic._updateValueCallback(data) 

########## ########## ########## ########## ##########

while True:
  time.sleep(0.5)
  appNotify()