import RPi.GPIO as GPIO
import time

class Motor:
	def __init__(self,dirPin,stepPin, stepsPerRevolution):
		self.dirPin = dirPin
		self.stepPin = stepPin
		self.stepsPerRevolution = stepsPerRevolution

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(dirPin, GPIO.OUT)
		GPIO.setup(stepPin, GPIO.OUT)
	
	def forward(self,steps):
		GPIO.output(self.dirPin, GPIO.HIGH)
		for _ in range(steps):
			# + int(6400*10/360)
			# Estas quatro linhas resultam em 1 passo:
			GPIO.output(self.stepPin, GPIO.HIGH)
			time.sleep(0.005)  # Atraso em segundos (2000 microssegundos)
			GPIO.output(self.stepPin, GPIO.LOW)
			time.sleep(0.005)  # Atraso em segundos (2000 microssegundos)
			
	def backward(self,steps):
		GPIO.output(self.dirPin, GPIO.LOW)
		for _ in range(steps):
			# Estas quatro linhas resultam em 1 passo:
			GPIO.output(self.stepPin, GPIO.HIGH)
			time.sleep(0.005)  # Atraso em segundos (1000 microssegundos)
			GPIO.output(self.stepPin, GPIO.LOW)
			time.sleep(0.005)  # Atraso em segundos (1000 microssegundos)


#motor = Motor(21,20,6400)
#motor.forward(int(6400*90/360))
#motor.backward(int(6400*360/360))

GPIO.cleanup()

