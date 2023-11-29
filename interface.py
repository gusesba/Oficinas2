from tkinter import *
import math
import time

class Interface:
	
	def atualizarTemperaturaHumidade(self,janela,tempView,humView,read):
		data = read()
		print(data)
		temperature = data[0]
		humidity = data[1]
		if temperature is not None:
			tempView.config(text="{0:0.1f}F".format(temperature))
		#else:
		#	tempView.config(text="failed to read")
		if humidity is not None:
			humView.config(text="{0:0.1f}%".format(humidity))
		#else:
		#	humView.config(text="failed to read")
		janela.after(1000,self.atualizarTemperaturaHumidade,janela,tempView,humView,read)
		
	def searchObjects(self):
		self.options = self.findObj(self.search_view.get())
		self.drop['menu'].delete('0',END)
		for i in self.options:
			self.drop['menu'].add_command(label=i,command=lambda i=i:self.clicked.set(i))
			
	def updateView(self):
		obj = self.clicked.get()
		info = self.getInfo(obj)
		az = info['azimuth']
		alt = info['altitude']
		self.setView(alt,az)
		
	def rastrearObj(self):
		i = 0
		while i<int(self.rastrearInp_view.get()):
			dados = self.trackObj(self.AtualAz,self.AtualAlt)
			self.AtualAz = dados[0]
			self.AtualAlt = dados[1]
			time.sleep(int(self.rastrearInp2_view.get()))
			i += int(self.rastrearInp2_view.get())
			
	def moverMotor2(self):
		dados = self.moverMotor(self.AtualAz,self.AtualAlt)
		self.AtualAz = dados[0]
		self.AtualAlt = dados[1]
	
	def __init__(self,setTime,moverMotor,getView, readSensorTemp,findObj, getInfo, setView,trackObj):
		self.AtualAz = 0
		self.AtualAlt = 0
		self.moverMotor = moverMotor
		self.findObj = findObj
		self.getInfo = getInfo
		self.setView = setView
		self.trackObj = trackObj
		janela = Tk()
		janela.title("STAR4U")
		texto_time = Label(janela, text="Escolha o horário do dia")
		texto_time.grid(column=0,row=0, padx=10, pady=10)
		botaoDia = Button(janela, text="Dia",command=lambda: setTime(0))
		botaoDia.grid(column=0,row=1, padx=10)
		botaoNoite = Button(janela, text="Noite", command=lambda: setTime(200022222))
		botaoNoite.grid(column=0,row=2, padx=10)
		
		texto_motor = Label(janela, text="Movimentar telescópio para a visualização atual")
		texto_motor.grid(column=1,row=0, padx=10, pady=10)
		botaoMotor = Button(janela, text="Movimentar",command=self.moverMotor2)
		botaoMotor.grid(column=1,row=1, padx=10, pady=10)

		texto_view = Label(janela, text="Visualizar coordenadas atuais")
		texto_view.grid(column=3,row=0, padx=10, pady=10)
		texto_view2 = Label(janela, text="")
		texto_view2.grid(column=3,row=2, padx=10, pady=10)
		botaoView = Button(janela, text="Visualizar", command=lambda: texto_view2.config(text='alt: ' + str(getView()[0]) + ", az: " + str(getView()[1])))
		botaoView.grid(column=3,row=1, padx=10, pady=10)
		
		temperatura_text = Label(janela,text="Temperatura")
		temperatura_text.grid(column=4,row=0, padx=10, pady=10)
		temperatura_view = Label(janela, text="")
		temperatura_view.grid(column=4,row=1, padx=10, pady=10)
		
		humidade_text = Label(janela,text="Humidade")
		humidade_text.grid(column=4,row=2, padx=10, pady=10)
		humidade_view = Label(janela, text="")
		humidade_view.grid(column=4,row=3, padx=10, pady=10)
		
		procurar_view = Label(janela,text="Pesquisar Objeto")
		procurar_view.grid(column=5,row=0,padx=10,pady=10)
		drop_view = Label(janela, text= " ")
		drop_view.grid(column=5,row=3,padx=10,pady=10)
		self.search_view = Entry(janela,width=30)
		self.search_view.grid(column=5,row=1,padx=10,pady=10)
		
		
		self.options = ["Moon","Jupiter","Marte"]
		
		self.clicked = StringVar()
		self.drop = OptionMenu(janela,self.clicked,*self.options)
		self.drop.grid(column=5,row=3,padx=10,pady=10)
		
		searchBtn_view = Button(janela,text="Buscar",command=self.searchObjects)
		searchBtn_view.grid(column=5,row=2,padx=10,pady=10)
		
		updateViewBtn_view = Button(janela, text="Atualizar View", command=self.updateView)
		updateViewBtn_view.grid(column=5,row=4,padx=10,pady=10)
	
	
		rastrear_view = Label(janela, text="Rastrear objeto selecionado")
		rastrear_view.grid(column=6,row=0,padx=10,pady=10)
		rastrear2_view = Label(janela, text="Tempo Total (s)")
		rastrear2_view.grid(column=6,row=1,padx=10,pady=10)
		self.rastrearInp_view = Entry(janela,width=20)
		self.rastrearInp_view.grid(column=6,row=2,padx=10,pady=10)
		rastrear3_view = Label(janela, text="Intervalo (s)")
		rastrear3_view.grid(column=6,row=3,padx=10,pady=10)
		self.rastrearInp2_view = Entry(janela,width=20)
		self.rastrearInp2_view.grid(column=6,row=4,padx=10,pady=10)
		rastrearBtn_view = Button(janela,text="Rastrear",command=self.rastrearObj)
		rastrearBtn_view.grid(column=6,row=5,padx=10,pady=10)
		
		
		self.atualizarTemperaturaHumidade(janela,temperatura_view,humidade_view,readSensorTemp)

		janela.mainloop()
	pass
