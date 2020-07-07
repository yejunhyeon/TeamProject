# ex -> https://qiita.com/comachi/items/c494e0d6c6d1775a3748
# ex2 -> https://github.com/Adam-Langley/pybleno
# uuid -> https://www.uuidgenerator.net/version4

from pybleno import *
import binascii

bleno = Bleno()

MY_SERVICE_UUID = '13333333-3333-3333-3333-333333333307'
NOTIFY_CHARACTERISTIC_UUID = '13333333-3333-3333-3333-333333333301'
READ_CHARACTERISTIC_UUID = '13333333-3333-3333-3333-333333333302'
WRITE_CHARACTERISTIC_UUID = '13333333-3333-3333-3333-333333333303'
DEVICE_NAME = 'WDJ'

counter = 0

########## ########## ########## ########## ##########

# Characteristic -> bleno inheritance / node ->util.inherits(XX, Characteristic);
class NotifyCharacteristic(Characteristic):
  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': NOTIFY_CHARACTERISTIC_UUID,
      'properties': ['notify'],
      'value': None
    })
    self._value = 0
    self._updateValueCallback = None

  def onSubscribe(self, maxValueSize, updateValueCallback):
    print('Characteristic - onSubscribe')
    self._updateValueCallback = updateValueCallback
  def onUnsubscribe(self):
    print('Characteristic - onUnsubscribe')
    self._updateValueCallback = None

class ReadCharacteristic(Characteristic):
  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': READ_CHARACTERISTIC_UUID,
      'properties': ['read'],
      'value': None
    })
    self._value = 0
    self._updateValueCallback = None

  # def onReadRequest(self, offset, callback):
  #   # B == unsigned char int 1btyes
  #   data = array.array('B', [0] * 2) # [0,]
  #   # writeUInt8(buffer, value, offset)
  #   print(data)
  #   # callback(Characteristic.RESULT_SUCCESS, self._value)
  #   callback(Characteristic.RESULT_SUCCESS, data)

  def onReadRequest(self, offset, callback):
    data = array.array('b', [5]*20)
    writeUInt8(data, 100, 1)
    writeUInt8(data, 200, 2)
    print(data)
    callback(Characteristic.RESULT_SUCCESS, data)

class WriteCharacteristic(Characteristic):
  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': WRITE_CHARACTERISTIC_UUID,
      'properties': ['write'],
      'value': None
    })
    self._value = 0
    self._updateValueCallback = None

  def onWriteRequest(self, data, offset, withoutResponse, callback):
    print('onWriteRequest', end='')
    print(data)
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

def onAdvertisingStart(error):
  print('on -> advertisingStart: ' + ('error ' + error if error else 'success'))
  if not error:
    bleno.setServices([
      BlenoPrimaryService({
        'uuid': MY_SERVICE_UUID,
        'characteristics': [
          notifyCharacteristic,
          readCharacteristic,
          writeCharacteristic
        ]
      })
    ])

bleno.on('advertisingStart', onAdvertisingStart)
bleno.start()

########## ########## ########## ########## ##########

import time
def task():
  global counter
  counter += 1
  notifyCharacteristic._value = counter
  if notifyCharacteristic._updateValueCallback:
    #  value 를 str().encode() 하면 '12' 가 [49, 50] 이 됨
    # 'b' 형태 <class 'bytes'>
    # print('Sending notification with value : ' + str(notifyCharacteristic._value))
    # notificationBytes = str(notifyCharacteristic._value).encode()
    # print(notificationBytes)

    # data = array.array('b', [5]*10)
    # writeUInt8(data, 30, 1)
    # writeUInt8(data, 40, 2)
    # print(data)

    data = array.array('b', [0])
    writeUInt8(data, counter, 0)
    notifyCharacteristic._updateValueCallback(data)

while True:
  task()
  time.sleep(1)