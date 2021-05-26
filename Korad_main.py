from myTUI import Form, Edit, Text, cls
import sys
from time import sleep, time,strftime,gmtime
import serial
from serial.tools.list_ports import comports


cls()
#HELP KEYS FORM##############################################
  #KEYS
def HelpForm():
  HotKeys = [  '1..9 - select port',
        's - rescan ports',
        '------------------',
        'v - set voltage',
        'i - set current',
        'o - set I cut off',
        '------------------',
        'r - Run KORAD',
        't - Stop KORAD',
        '------------------',
        'q - exit',
        ]
  h = Form('Hot Keys',80,2,28,len(HotKeys)+4)
  t_Keys = []
  for n in range(0, len(HotKeys)):
    t_Keys.append(Text(HotKeys[n],h.x+3,h.y+n+2))

#PORT GENERATOR FORM ##############################################
  #check for different ports and fill up
def ScanPorts():
  ports = []
  for n, (port, desc, hwid) in enumerate(sorted(comports()), 1):
      ports.append(port)
  #From za izpis availabele ports
  Form_ports = Form('Serial Ports',3,2 ,28,len(ports)+9)
  global e
  e = []
  for n in range(0, len(ports)):
    e.append(Edit('(' + str(n+1) + ')', Form_ports.x+3 ,Form_ports.y + n + 5))
    e[n].new_value(ports[n])

  global Set_port
  Set_port = Edit('Port', Form_ports.x+3 ,Form_ports.y + 2)
  Set_port.new_value(e[0].value)

def KoradOutpuForm():
#KORAD OUTPUT FORM ##############################################
  f_k = Form('Korad OUTPUT', 35, 2, 40, 9)
  global Vout
  global Iout
  global Charge
  global Time_r
  global Power
  global eEng
  Vout = Edit('Vout [V]', f_k.x + 3, f_k.y +2)
  Vout.enabled  = False
  #Vout.new_value('00.00')

  Iout = Edit('Iout [A]', f_k.x + 3, f_k.y +3)
  Iout.enabled  = False
  #Iout.new_value('0.000')

  #On time_r [h:m:s] =
  Time_r = Edit('Time', Vout.x+20, Vout.y) 
  Time_r.enabled = False

  Power =  Edit('Power [W]', f_k.x+3, f_k.y+4) 
  Power.enabled = False
  Power.value = '0.0'
  eEng =   Edit('Energy [Wh]', f_k.x+3, f_k.y+5)
  eEng.enabled = False
  eEng.value = '0.0'
  Charge = Edit('Charge [mAh]', f_k.x+3, f_k.y+6)
  Charge.enabled = False
  Charge.value = '0.0'

def KoradSettingsForm():
#KORAD settings FORM ##############################################
  f_s = Form('Korad SETUP', 35, 11, 40, 6)
  global Vset
  global Iset
  global Ioff
  Vset = Edit('Vset [V]', f_s.x + 3, f_s.y +2)
  Vset.new_value('04.30')

  Iset = Edit('Iset [A]', f_s.x + 3, f_s.y +3)
  Iset.new_value('0.900')

  Ioff = Edit('Ioff [A]', f_s.x + 3, f_s.y +4)
  Ioff.new_value('0.010')

def Run():
  #--- clear file data ---
  dataFile = open("./data.csv", "w")
  dataFile.write("Time [h:m:sr], Voltage [V], Current [A]\n")
  ser = serial.Serial(Set_port.value)
  ser.write(('VSET1:'+Vset.value).encode('utf-8'))
  sleep(0.1)
  ser.write(('ISET1:'+Iset.value).encode('utf-8'))
  sleep(0.1)
  ser.write(('OUT1').encode('utf-8'))
  sleep(0.1)
  Charge_out = 0.0
  eEng_out = 0.0
  Start_time = time()
  while True:
    Time_r.new_value(strftime('%H:%M:%S',gmtime(time()-Start_time)))
    ser.write(('VOUT1?').encode('utf-8'))
    text = ser.read(5)
    Vout.new_value(text.decode('utf-8'))
    ser.write(('IOUT1?').encode('utf-8'))
    text = ser.read(5)
    Iout.new_value(text.decode('utf-8'))
    #------- DATA ----------------------------
    Power.new_value('{:.2f}'.format(float(Vout.value)*float(Iout.value)))
    eEng_out += float(Power.value) /3600
    eEng.new_value('{:.2f}'.format(eEng_out))
    Charge_out += float(Iout.value)*1000/60/60
    Charge.new_value('{:.2f}'.format(Charge_out,))
    #------- FILE ----------------------------
    dataFile = open("./data.csv", "a")
    dataFile.write(Time_r.value + ", " + Vout.value + ", " + Iout.value + "\n")
    dataFile.close()
    #------- STOP ----------------------------
    if float(Iout.value)< float(Ioff.value):
      ser.write(('OUT0').encode('utf-8'))
      break  

    sleep(1)

def SetVoltage():
  Vset.new_value('')
  key = input('')
  Vset.new_value(key)
  if float(key) > 30:
    Vset.new_value('00.00')

def SetCurrent():
  Iset.new_value('')
  key = input('')
  Iset.new_value(key)
  if float(key) > 5.0:
    Iset.new_value('5.000')
  elif float(key) < 0.001:
    Ioff.new_value('0.001')

def SetCutOff():
  Ioff.new_value('')
  key = input('')
  Ioff.new_value(key)
  if float(key) > 5.0:
    Ioff.new_value('5.000')
  elif float(key) < 0.001:
    Ioff.new_value('0.001')    


# MAIN PROGRAM ##############################################
HelpForm()
ScanPorts()
KoradSettingsForm()
KoradOutpuForm()

cmd = Edit('Cmd',2,20)
cmd.value = ''
while (cmd.value != 'q'):
  cmd.new_value('')
  key = input('')
  cmd.new_value(key)
  #preveri tipko in naredikar je treba.
  if key == 'r':
    Run()
  elif key == '1':
    Set_port.new_value(e[0].value)
  elif key == '2':
    Set_port.new_value(e[1].value)
  elif key == '3':
    Set_port.new_value(e[2].value)
  elif key == '4':
    Set_port.new_value(e[3].value)
  elif key == '5':
    Set_port.new_value(e[4].value)
  elif key == 'v':
    SetVoltage()
  elif key == 'i':
    SetCurrent()
  elif key == 'o':
    SetCutOff()
  elif key == 's':
    ScanPorts()


cls()
#g = Form('Test-2', f.x+f.dx , f.y , 28, 6)

#e = Edit('Vout', f.x+2, f.y+3)
#e.new_value('Hoj!')

#t = Text('V', e.x + len(e.value) + len(e.text)+2, e.y)

