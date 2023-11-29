import RPi.GPIO as GPIO
import time

class MotorAlt:
	def __init__(self,dirPin,stepPin):
		self.dirPin = dirPin
		self.stepPin = stepPin
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(dirPin, GPIO.OUT)
		GPIO.setup(stepPin, GPIO.OUT)

	def forward(self,step):
		GPIO.output(self.dirPin, GPIO.HIGH)
		for _ in range(step):
			# Estas quatro linhas resultam em 1 passo:
			GPIO.output(self.stepPin, GPIO.HIGH)
			time.sleep(0.02)
			time.sleep(0.005)  # Atraso em segundos (2000 microssegundos)
			GPIO.output(self.stepPin, GPIO.LOW)
			time.sleep(0.02)
			time.sleep(0.005)  # Atraso em segundos (2000 microssegundos)
		
	def backward(self,step):
		GPIO.output(self.dirPin, GPIO.LOW)
		for _ in range(step):
			# Estas quatro linhas resultam em 1 passo:
			GPIO.output(self.stepPin, GPIO.HIGH)
			time.sleep(0.005)  # Atraso em segundos (2000 microssegundos)
			GPIO.output(self.stepPin, GPIO.LOW)
			time.sleep(0.005)  # Atraso em segundos (2000 microssegundos)



#motor = MotorAlt(23,24)
#motor.forward(360)
#GPIO.cleanup()
