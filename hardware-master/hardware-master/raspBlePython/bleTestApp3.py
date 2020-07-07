import cv2, dlib
import numpy as np
from imutils import face_utils
from keras.models import load_model
import threading

from IsTraking import IsTraking

##################################################################
#

import time
import serial

from pybleno import *
import binascii

port = '/dev/ttyACM0'
brate = 115200

seri = serial.Serial(port, baudrate = brate, timeout = None)
seri.flushInput()

bleno = Bleno()

MY_SERVICE_UUID = '13333333-3333-3333-3333-000000000000'
NOTIFY_CHARACTERISTIC_UUID = '13333333-3333-3333-3333-000000000001'
READ_CHARACTERISTIC_UUID = '13333333-3333-3333-3333-000000000002'
WRITE_CHARACTERISTIC_UUID = '13333333-3333-3333-3333-000000000003'
DEVICE_NAME = 'WDJ'

########## DATA ##########
_counter = 0
_data = array.array('B', [0]*10)
########## DATA ##########

########## ########## ########## ########## ##########

class NotifyCharacteristic(Characteristic):
  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': NOTIFY_CHARACTERISTIC_UUID,
      'properties': ['notify'],
      'value': None
    })
    self._value = 0
    self._isSubscribed = True
    self._updateValueCallback = None

  def onSubscribe(self, maxValueSize, updateValueCallback):
    print('Characteristic - Notify - onSubscribe > ')
    self.isSubscribed = True
    self._updateValueCallback = updateValueCallback
  def onUnsubscribe(self):
    print('Characteristic - Notify - onUnsubscribe > ')
    self._isSubscribed = False
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

  def onReadRequest(self, offset, callback):
    data = array.array('B', [5]*5) # or data = buffer
    writeUInt8(data, 100, 1)
    writeUInt8(data, 200, 2)
    writeUInt8(data, 150, 3)
    print('onReadRequest -> ', end='')
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
    print('onWriteRequest -> ', end='')
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
          writeCharacteristic,
        ]
      })
    ])

bleno.on('advertisingStart', onAdvertisingStart)
bleno.start()

########## ########## ########## ########## ##########

import time
def appNotify():
  global _counter, _data
  _counter += 1
  if _counter > 99:
    _counter = 1

  counter = _counter
  data = _data

  writeUInt8(data, counter, 0) # ino read , write
  # print("> ", end='')
  # print(counter, end='')
  # print(" ~ ", end='')
  print(data)

  if notifyCharacteristic._updateValueCallback:
    notifyCharacteristic._updateValueCallback(data)

#
##################################################################
IS = IsTraking()

screen_x= 600
screen_y= 400


state_l = 0
state_r = 0

IMG_SIZE = (34, 26) 

detector = dlib.get_frontal_face_detector()
predictor = IS._predictor

model = load_model('models/2018_12_17_22_58_35.h5')
model.summary()

def crop_eye(img, eye_points):
  x1, y1 = np.amin(eye_points, axis=0)
  x2, y2 = np.amax(eye_points, axis=0)
  cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

  w = (x2 - x1) * 1.2
  h = w * IMG_SIZE[1] / IMG_SIZE[0]

  margin_x, margin_y = w / 2, h / 2

  min_x, min_y = int(cx - margin_x), int(cy - margin_y)
  max_x, max_y = int(cx + margin_x), int(cy + margin_y)

  eye_rect = np.rint([min_x, min_y, max_x, max_y]).astype(np.int)

  eye_img = gray[eye_rect[1]:eye_rect[3], eye_rect[0]:eye_rect[2]]

  return eye_img, eye_rect
  
def printLog():

  print("--------------------------------------")
  print("left eye: ", state_r, "right eye: ", state_l)
  print("--------------------------------------")
  print("screen size x:", screen_x,"y:", screen_y)
  print("left point:",IS.pupil_left_coords())
  print("right point:",IS.pupil_right_coords())

  seeee = 0

  if IS.is_right():
    print("--------------------------------------")
    print("see: right")
    seeee = 10
  elif IS.is_left():
    print("--------------------------------------")
    print("see: left")
    seeee = 20
  elif IS.is_center():
    print("--------------------------------------")
    print("see: middle")
    seeee = 30
##################################################################
#
  global _counter, _data
  data = _data
  writeUInt8(data, 60, 1) # ino read , write
  writeUInt8(data, 40, 2) # ino read , write
  writeUInt8(data, state_l, 3) # ino read , write
  writeUInt8(data, state_r, 4) # ino read , write
  writeUInt8(data, seeee, 5) # ino read , write

  seri.flushInput()
  readData = seri.readline()
  print(readData)
  readData = seri.readline()
  print(readData)
  readData = seri.readline()
  print(readData)
  readData = seri.readline()
  print(readData)
  readData = seri.readline()
  print(readData)
  print("--------------------------------------")
  threading.Timer(1,printLog).start()
  ##### ##### 
  appNotify()
  ##### #####
# time.sleep(1)
#
##################################################################
printLog()

# cap = cv2.VideoCapture("test.mp4")
cap = cv2.VideoCapture(-1)

while cap.isOpened():
  _, frame = cap.read()

  IS.refresh(frame)

  # frame = IS.annotated_frame()


  if cv2.waitKey(1) == 27:
      break


  frame = cv2.resize(frame, dsize=(screen_x, screen_y))

  img = frame.copy()

  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  faces = detector(gray)

  if(faces):
    for face in faces:
      shapes = predictor(gray, face)
      shapes = face_utils.shape_to_np(shapes)

      eye_img_l, eye_rect_l = crop_eye(gray, eye_points=shapes[36:42])
      eye_img_r, eye_rect_r = crop_eye(gray, eye_points=shapes[42:48])

      eye_img_l = cv2.resize(eye_img_l, dsize=IMG_SIZE)
      eye_img_r = cv2.resize(eye_img_r, dsize=IMG_SIZE)
      eye_img_r = cv2.flip(eye_img_r, flipCode=1)

      eye_input_l = eye_img_l.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.
      eye_input_r = eye_img_r.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.

      pred_l = model.predict(eye_input_l)
      pred_r = model.predict(eye_input_r)

      state_l = 1 if pred_l > 0.2 else 2
      state_r = 1 if pred_r > 0.2 else 2

  else:
    state_r = 0
    state_l = 0

