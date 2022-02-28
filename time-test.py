#!/usr/bin/env python
import time
from datetime import datetime
import calendar
import matplotlib.pyplot as plt
import numpy as np
import re
import csv
import pandas as pd
import sys
from os import remove


#Variable para definir los segundos en los que se van a agrupar los ficheros
if len(sys.argv) > 1:
	step = int(sys.argv[1])
else:
	step=3600

access=[]
mail=[]
error=[]

accessT=[]
mailT=[]
errorT=[]

accessIP=[]
mailIP=[]
errorIP=[]


### Salida CSV ###
# open the file in the write mode
f = open('ficheroALlLogs.csv', 'w')
# create the csv writer
writer = csv.writer(f)
##################



def dateorder(file):
	recordlist=[]
	timelist=[]
	first = True

	iplist=[]
	listlist=[]
	first1 = True

	### First log
	if file == 1:
		f = open('./logFiles/access_log')
		for linea in f:
			date_string = linea[linea.find('[')+1:linea.find('-0500')-1]

			fmt = ("%d/%b/%Y:%H:%M:%S")
			epochDate = int(calendar.timegm(time.strptime(str(date_string), fmt)))

			global access
			access.append(int(epochDate))
			access.sort()

			#First record
			if first:
				recordlist.append(epochDate)
				lista=[epochDate, 1]
				timelist.append(lista)
				first=False
				#Calculate the frequecy of the hours for each record
			else:
				if epochDate in recordlist:
					ind = recordlist.index(epochDate)
					timelist[ind][1]=timelist[ind][1]+1
				else:
					lista=[epochDate, 1]
					timelist.append(lista)
					recordlist.append(epochDate)
			
			# Get ip (if contains) from each log 
			ip_list = re.findall( r'[0-9]+(?:\.[0-9]+){3}', linea )
			if len(ip_list) > 0:
				ip = ip_list[0]
				#Para realizar las gráficas de IP
				val=[epochDate, ip]
				if first1:
					lista=[epochDate, ip, 1]
					iplist.append(lista)
					listlist.append(val)
					first1=False
				else:
					if val in listlist:
						ind = listlist.index(val)
						iplist[ind][2]=iplist[ind][2]+1
					else:
						lista=[epochDate, ip, 1]
						iplist.append(lista)
						listlist.append(val)
			else:
				ip = '-'

			#########Logs para el fichero comun
			lista2=[epochDate, "access_log", ip, linea[linea.find(']')+1:-1]]
			# write a row to the csv file
			writer.writerow(lista2)


		timeSort = sorted(timelist, key= lambda time : time[0])
		timeSort2 = sorted(iplist, key= lambda time : time[0])
		global accessT
		global accessIP
		accessT = timeSort
		accessIP = timeSort2


	### Second log
	if file == 2:
		f = open('./logFiles/maillog')
		for linea in f:
			date_string = '2005 ' + linea[:linea.find('combo')-1]
			date_object = datetime.strptime(date_string, "%Y %b %d %X")

			fmt = ("%Y-%m-%d %H:%M:%S")
			epochDate = int(calendar.timegm(time.strptime(str(date_object), fmt)))

			global mail
			mail.append(int(epochDate))
			mail.sort()

			#First record
			if first:
				recordlist.append(epochDate)
				lista=[epochDate, 1]
				timelist.append(lista)
				first=False
				#Calculate the frequecy of the hours for each record
			else:
				if epochDate in recordlist:
					ind = recordlist.index(epochDate)
					timelist[ind][1]=timelist[ind][1]+1
				else:
					lista=[epochDate, 1]
					timelist.append(lista)
					recordlist.append(epochDate)

			# Get ip (if contains) from each log 
			ip_list = re.findall( r'[0-9]+(?:\.[0-9]+){3}', linea )
			if len(ip_list) > 0:
				ip = ip_list[0]
				#Para realizar las gráficas de IP
				val=[epochDate, ip]
				if first1:
					lista=[epochDate, ip, 1]
					iplist.append(lista)
					listlist.append(val)
					first1=False
				else:
					if val in listlist:
						ind = listlist.index(val)
						iplist[ind][2]=iplist[ind][2]+1
					else:
						lista=[epochDate, ip, 1]
						iplist.append(lista)
						listlist.append(val)
			else:
				ip = '-'

			#########Logs para el fichero comun
			lista2=[epochDate, "mail_log", ip, linea[linea.find('combo'):-1]]
			# write a row to the csv file
			writer.writerow(lista2)

		timeSort = sorted(timelist, key= lambda time : time[0])
		timeSort2 = sorted(iplist, key= lambda time : time[0])
		global mailT
		global mailIP
		mailT = timeSort
		mailIP = timeSort2
	
	### Third log
	if file == 3:
		f = open('./logFiles/error_log')
		for linea in f:
			date_string = linea[linea.find('[')+5:linea.find(']')]
			date_object = datetime.strptime(date_string, "%b %d %X %Y")
			fmt = ("%Y-%m-%d %H:%M:%S")
			epochDate = int(calendar.timegm(time.strptime(str(date_object), fmt)))
			
			global error
			error.append(int(epochDate))
			error.sort()

			#First record
			if first:
				recordlist.append(epochDate)
				lista=[epochDate, 1]
				timelist.append(lista)
				first=False
				#Calculate the frequecy of the hours for each record
			else:
				if epochDate in recordlist:
					ind = recordlist.index(epochDate)
					timelist[ind][1]=timelist[ind][1]+1
				else:
					lista=[epochDate, 1]
					timelist.append(lista)
					recordlist.append(epochDate)

			# Get ip (if contains) from each log 
			ip_list = re.findall( r'[0-9]+(?:\.[0-9]+){3}', linea )
			if len(ip_list) > 0:
				ip = ip_list[0]
				#Para realizar las gráficas de IP
				val=[epochDate, ip]
				if first1:
					lista=[epochDate, ip, 1]
					iplist.append(lista)
					listlist.append(val)
					first1=False
				else:
					if val in listlist:
						ind = listlist.index(val)
						iplist[ind][2]=iplist[ind][2]+1
					else:
						lista=[epochDate, ip, 1]
						iplist.append(lista)
						listlist.append(val)
			else:
				ip = '-'

			#########Logs para el fichero comun
			try:
				linea_aux = linea.split('[client')[1]
				linea_aux= linea_aux.split(']')[1]
				lista2=[epochDate, "error_log", ip, "[error]" + linea_aux  ]
			except: 
				lista2=[epochDate, "error_log", ip, linea[linea.find('] [')+2:-1]  ]
			# write a row to the csv file
			writer.writerow(lista2)

		timeSort = sorted(timelist, key= lambda time : time[0])
		timeSort2 = sorted(iplist, key= lambda time : time[0])
		global errorT
		global errorIP
		errorT = timeSort
		errorIP = timeSort2

#Graficas individuales
def drawgraphictime(sensor, timearray):
	hours=[]
	value=[]
	plt.figure(sensor)
	for i in range(0,len(timearray)):
		hours.append(timearray[i][0])
		value.append(timearray[i][1])
	positionx =np.arange(len(hours))
	plt.bar(positionx,value,align="center")
	
	nvalores=25
	startgraph = hours[0]
	finishgraph = hours[len(hours)-1]
	entre = (hours[len(hours)-1]-hours[0])/nvalores
	index2 = np.arange(len(hours), step=len(hours)/nvalores)
	plt.xticks(index2, np.arange(startgraph, finishgraph, step=entre, dtype=int))
	plt.xticks(rotation=90)
	plt.xlabel("Date")
	plt.ylabel("Number of records")
	plt.title(sensor +" time")
	plt.savefig(sensor +"T.png", bbox_inches="tight", pad_inches = 0.3)
	plt.close()

#Grafica global
def drawgrafictimetotal(access_log, mail_log, error_log):
	hours=[]
	hoursAcc=[]
	hoursMail=[]
	hoursError=[]
	valueAcc=[]
	valueMail=[]
	valueError=[]
	for i in range(0, len(mail_log)):
		hours.append(int(mail_log[i][0]))
		hoursMail.append(int(mail_log[i][0]))
		valueMail.append(int(mail_log[i][1]))
	for i in range(0, len(access_log)):
		hours.append(int(access_log[i][0]))
		hoursAcc.append(int(access_log[i][0]))
		valueAcc.append(int(access_log[i][1]))
	for i in range(0, len(error_log)):
		hours.append(int(error_log[i][0]))
		hoursError.append(int(error_log[i][0]))
		valueError.append(int(error_log[i][1]))
	hours.sort()
	#Elimina los elemento duplicados
	hours2 = sorted(list(set(hours)))
	#Ponemos en todos los sensores elmismo numero de registros, con un 0 
	for i in range(0, len(hours2)):
		if hours2[i] not in hoursAcc :
			valueAcc.insert(i, 0)
		if hours2[i] not in hoursMail :
			valueMail.insert(i, 0)
		if hours2[i] not in hoursError :
			valueError.insert(i, 0)
	#Eliminamos los registros que esten dentro de los X primeros segundos de cada registro
	#sumamos los valores de los registros en esos X primeros segundos
	contador = len(hours2)
	contpop = 0
	for i in range(0, len(hours2)):
		#Esta es la variable que determina la agrupación en segundos
		global step
		if i < contador :
			contpop = 0
			for y in range(0,len(hours2)) :
				if y < contador+contpop  and y>=i :
					if hours2[i]+step >= hours2[y - contpop] and hours2[y - contpop]!=hours2[i] :
						hours2.pop(y - contpop)
						valueAcc[i]=valueAcc[i]+valueAcc[y - contpop]
						valueAcc.pop(y - contpop)
						valueMail[i]=valueMail[i]+valueMail[y - contpop]
						valueMail.pop(y - contpop)
						valueError[i]=valueError[i]+valueError[y - contpop]
						valueError.pop(y - contpop)
						contador = len(hours2)
						contpop = contpop + 1

	index = np.arange(len(hours2))
	plt.bar(index, valueAcc, label='access')
	plt.bar(index, valueMail, label='mail', bottom=np.array(valueAcc))
	plt.bar(index, valueError, label='error', bottom=np.array(valueAcc) + np.array(valueMail))
	nvalores=25
	startgraph = hours2[0]
	finishgraph = hours2[len(hours2)-1]
	entre = (hours2[len(hours2)-1]-hours2[0])/nvalores
	index2 = np.arange(len(hours2), step=len(hours2)/nvalores)
	plt.xticks(index2, np.arange(startgraph, finishgraph, step=entre, dtype=int))
	plt.xticks(rotation=90)
	plt.ylabel("Number of records")
	plt.xlabel("Date")
	plt.title('Total time (Agrupación: '+str(step)+"s)")
	plt.legend()
	plt.savefig(str(step)+"sTotalTime.png", bbox_inches="tight", pad_inches = 0.3)
	plt.close()

#Dibuja las gráficas de las IP
def drawgraphicip(logType, timearray):
	hours=[]
	freq=[]
	value=[]
	ip =[]
	val=[]
	plt.figure(logType)
	plt.subplot(211)
	plt.figure(logType).subplots_adjust(hspace=1.5)
	for i in range(0,len(timearray)):
		if int(timearray[i][2])>=3:
			if timearray[i][0] not in hours:
				hours.append(int(timearray[i][0]))
				lista =[timearray[i][0],1]
				freq.append(lista)
			else:
				ind = hours.index(timearray[i][0])
				freq[ind][1]=freq[ind][1]+1
	for i in range(0,len(freq)):
		value.append(freq[i][1])
	contador = len(hours)
	contpop = 0
	for i in range(0, len(hours)):
		if i < contador :
			contpop = 0
			for y in range(0,len(hours)) :
				if y < contador+contpop  and y>=i :
					if hours[i]+0 >= hours[y - contpop] and hours[y - contpop]!=hours[i] :
						hours.pop(y - contpop)
						value[i]=value[i]+value[y - contpop]
						value.pop(y - contpop)
						contador = len(hours)
						contpop = contpop + 1

	positionx =np.arange(len(hours))
	plt.bar(positionx,value,align="center")
	#Etiquetas xlabel
	plt.xticks(positionx,hours)
	plt.xticks(rotation=90)
	plt.xlabel("Date")
	plt.ylabel("Number of IP")
	plt.title(logType +" , number of IPs that appears 3 or more times in the same sec")

	plt.subplot(212)
	for i in range(0,len(timearray)):
		if int(timearray[i][2])>=3:
			ip.append(timearray[i][1])
			val.append(timearray[i][2])
	positionx =np.arange(len(ip))
	plt.bar(positionx,val,align="center")
	#Etiquetas xlabel
	plt.xticks(positionx,ip)
	plt.xticks(rotation=90)
	plt.xlabel("IP")
	plt.ylabel("Number of records")

	plt.savefig(logType +"ip.png", bbox_inches="tight", pad_inches = 0.3)
	plt.close()

#Functions to call
dateorder(1)
dateorder(2)
dateorder(3)

drawgraphictime("access_log", accessT)
drawgraphictime("mail_log", mailT)
drawgraphictime("error_log", errorT)

drawgraphicip("access_log", accessIP)
drawgraphicip("mail_log", mailIP)
drawgraphicip("error_log", errorIP)

drawgrafictimetotal(accessT,mailT,errorT)

# close the file
f.close()
df = pd.read_csv('ficheroALlLogs.csv', header=None, names=["Epoch Date", "Log Type", "IP Adress", "Log"])
df.to_csv('out.csv') #fichero final.
f.close()
#Se elimina el fichero que ya no es necesario
remove('ficheroALlLogs.csv')

