import serial

port = '/dev/ttyACM0'
brate = 9600 # boudrate

ard = serial.Serial(port , brate)
print("ard setting end")

while(1):
  c = input()
  print(c)
  if c=='q':
    print('if')
    break
  else:
    print('else')
    c = c.encode('utf-8')
    ard.write(c)
    print('OK')
