import time
from datetime import datetime
import calendar
import matplotlib.pyplot as plt
import numpy as np
import re

#Variable para definir los segundos en los que se van a agrupar los ficheros
step=3600

access=[]
mail=[]
error=[]

accessT=[]
mailT=[]
errorT=[]

all=[]

def dateorder(file):
    c = 0
    recordlist=[]
    timelist=[]
    ind = 0
    first = True

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
            else:
                ip = '-'

            #########Logs para el fichero comun
            lista2=[epochDate, "access_log", ip, linea[:linea.find('[')]+linea[linea.find(']')+1:-1]]
            all.append(lista2)

        timeSort = sorted(timelist, key= lambda time : time[0])
        global accessT
        accessT = timeSort


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
            else:
                ip = '-'

            #########Logs para el fichero comun
            lista2=[epochDate, "mail_log", ip, linea[linea.find('combo'):-1]]
            all.append(lista2)

        timeSort = sorted(timelist, key= lambda time : time[0])
        global mailT
        mailT = timeSort
    
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
            else:
                ip = '-'

            #########Logs para el fichero comun
            lista2=[epochDate, "error_log", ip, linea[linea.find('] [')+2:-1]]
            all.append(lista2)

        timeSort = sorted(timelist, key= lambda time : time[0])
        global errorT
        errorT = timeSort

#Escribe el fichero con todos los logs ordenados (hay que llamar antes a dateorder con cada fichero)
def writefile():
    s = open("ficheroAllLogs", "w")
    allSorted = sorted(all, key= lambda time : time[0])
    for i in range(0, len(all)):
        s.write(str(allSorted[i])+"\n")
    s.close()

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
	#Etiquetas xlabel
	plt.xticks(positionx,hours)
	#plt.xticks()
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
	plt.xticks(index,hours2)
	plt.xticks(rotation=90)
	plt.ylabel("Number of records")
	plt.xlabel("Date")
	plt.title('Total time (Agrupación: '+str(step)+"s)")
	plt.legend()
	plt.savefig(str(step)+"sTotalTime.png", bbox_inches="tight", pad_inches = 0.3)
	plt.close()

#Functions to call
dateorder(1)
dateorder(2)
dateorder(3)
writefile()

drawgraphictime("access_log", accessT)
drawgraphictime("mail_log", mailT)
drawgraphictime("error_log", errorT)

drawgrafictimetotal(accessT,mailT,errorT)