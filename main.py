import requests
import math
import json

import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time
from interface import Interface
from motor import Motor
from motor2 import MotorAlt
from sensorUmidade import SensorUmidade
from sensorGiroscopioAcel import SensorGiroscopioAcel
import re

#Pinos GPIO motor 1 
#direction1 = 18 # Direção
#step1 = 23 # Passo
#EN_pin1 = 7 # Enable

# Declare a instance of class pass GPIO pins numbers and the motor type
#mymotortest = RpiMotorLib.A4988Nema(direction1, step1, (21,21,21), "DRV8825")
#GPIO.setup(EN_pin1,GPIO.OUT) # set enable pin as output

#GPIO.output(EN_pin1,GPIO.LOW) # pull enable to low to enable motor
# def moverMotor():
	# mymotortest.motor_go(False, # True=Clockwise, False=Counter-Clockwise
                     # "Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                     # int(getView()[1]/1.8)
                     # , # number of steps
                     # .005, # step delay [sec]
                     # False, # True = print verbose output 
                     # .05) # initial delay [sec]
steps = 6400
motorAz = Motor(21,20,steps)

motorAlt = MotorAlt(23,24)
                                
sensorHumidade = SensorUmidade(16)


#sensorGiroscopioAcel = SensorGiroscopioAcel()
	

def moverMotor(AtualAz,AtualAlt):
	print(AtualAz,AtualAlt)
	stepAz = int(getView()[1]*steps/360) - AtualAz
	AtualAz += stepAz
	if stepAz > 0:
		motorAz.forward(stepAz)
	else:
		motorAz.backward(-stepAz)
	
	stepAlt = int(getView()[0]*200/360) - AtualAlt
	AtualAlt += stepAlt
	if stepAlt > 0:
		motorAlt.forward(stepAlt)
	else:
		motorAlt.backward(-stepAlt)
	return AtualAz,AtualAlt

def azAngle(seno, cosseno):
    # Usando math.acos para obter o ângulo em radianos no intervalo de 0 a pi (0 a 180 graus)
    angulo_radianos = math.acos(cosseno)
    
    # Converter de radianos para graus
    angulo_graus = math.degrees(angulo_radianos)

    # Verificar se o seno é negativo para determinar o quadrante
    if seno < 0:
        angulo_graus = 360 - angulo_graus

    return angulo_graus


def getView():
	view = requests.get('http://localhost:8090/api/main/view').text
	data = json.loads(view)
	altAz = json.loads(data['altAz'])
	return converterCoordenadas(altAz)

def printView():
	view = getView()
	print('alt: ', view[0], ' az: ', view[1], '\n')

def converterCoordenadas(coordenadas):
	altRad = math.asin(coordenadas[2])
	altDeg = math.degrees(altRad)
	
	cosAz = coordenadas[0]/math.cos(altRad)
	sinAz = coordenadas[1]/math.cos(altRad)
	azDeg = 180 - azAngle(sinAz,cosAz)
	return altDeg, azDeg
	
def setTime(time):
	requests.post('http://localhost:8090/api/main/time?time='+str(time))
	
def findObj(name):
	search = requests.get("http://localhost:8090/api/objects/find?str="+name)
	return json.loads(search.text)

def getInfo(name):
	search = requests.get("http://localhost:8090/api/objects/info?format=json&name="+name)
	return json.loads(search.text)
	
def setView(Alt,Az):
	Alt = math.radians(Alt)
	Az = math.pi - math.radians(Az)
	requests.post("http://localhost:8090/api/main/view?alt="+str(Alt)+"&az="+str(Az))
		
def initialize():
	requests.post('http://localhost:8090/api/main/view?altAz=[0.999722,0.06,0.201384]')
	
def gms_g(texto):
    # Use expressões regulares para extrair graus, minutos e segundos
    padrao = re.compile(r"([-+]?\d+)°(\d+)\'([\d.]+)\"")
    correspondencia = padrao.match(texto)

    graus, minutos, segundos = map(float, correspondencia.groups())
        
        # Converta para radianos
    radianos = (graus + minutos / 60 + segundos / 3600)
        
    return radianos

	
def getSelectedPos(AtualAz,AtualAlt):
	status = requests.get('http://localhost:8090/api/main/status').text
	status = json.loads(status)
	selectedInfo = status['selectioninfo']
	valores = selectedInfo.split('AZ/ALT: ')[1].split('  <br>')[0].split('/')
	setView(gms_g(valores[1]),gms_g(valores[0]))
	return moverMotor(AtualAz,AtualAlt)
	

	
#initialize()
interface = Interface(setTime,moverMotor,getView,sensorHumidade.readSensor,findObj,getInfo,setView,getSelectedPos)

GPIO.cleanup() # clear GPIO allocations after run
