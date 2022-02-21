#!/usr/bin/python3

import pandas as pd
import seaborn as sns
import json
import sys
from elasticsearch import Elasticsearch
from pathlib import Path
from statistics import *
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import time
from time import strptime, clock
from datetime import datetime
import math
import scipy.stats as st
from scipy.integrate import quad
from scipy.stats import spearmanr, pearsonr , kendalltau
from configparser import ConfigParser
import random

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
	plt.xticks(rotation=90)
	plt.xlabel("Date")
	plt.ylabel("Number of records")
	plt.title(sensor +" time")
	plt.savefig(sensor +"T.png", bbox_inches="tight", pad_inches = 0.3)
	plt.close()

def drawgrafictimetotal(fw,ids_s,radio_f,redes_mov,traf_ids,wifi, siem, bluetooth):
	hours=[]
	hoursfw=[]
	hoursids=[]
	hoursrad=[]
	hoursred=[]
	hourstraf=[]
	hourswifi=[]
	hourssiem=[]
	hoursblue=[]
	valuefw=[]
	valueids=[]
	valuerad=[]
	valuered=[]
	valuewifi=[]
	valuetraf=[]
	valuesiem=[]
	valueblue=[]
	for i in range(0, len(fw)):
		hours.append(int(fw[i][0]))
		hoursfw.append(int(fw[i][0]))
		valuefw.append(int(fw[i][1]))
	for i in range(0, len(ids_s)):
		hours.append(int(ids_s[i][0]))
		hoursids.append(int(ids_s[i][0]))
		valueids.append(int(ids_s[i][1]))
	for i in range(0, len(radio_f)):
		hours.append(int(radio_f[i][0]))
		hoursrad.append(int(radio_f[i][0]))
		valuerad.append(int(radio_f[i][1]))
	for i in range(0, len(redes_mov)):
		hours.append(int(redes_mov[i][0]))
		hoursred.append(int(redes_mov[i][0]))
		valuered.append(int(redes_mov[i][1]))
	for i in range(0, len(traf_ids)):
		hours.append(int(traf_ids[i][0]))
		hourstraf.append(int(traf_ids[i][0]))
		valuetraf.append(int(traf_ids[i][1]))
	for i in range(0, len(wifi)):
		hours.append(wifi[i][0])
		hourswifi.append(wifi[i][0])
		valuewifi.append(wifi[i][1])
	for i in range(0, len(siem)):
		hours.append(siem[i][0])
		hourssiem.append(siem[i][0])
		valuesiem.append(siem[i][1])
	for i in range(0, len(bluetooth)):
		hours.append(bluetooth[i][0])
		hoursblue.append(bluetooth[i][0])
		valueblue.append(bluetooth[i][1])
	hours.sort()
	#Elimina los elemento duplicados
	hours2 = sorted(list(set(hours)))
	#Ponemos en todos los sensores elmismo numero de registros, con un 0 
	for i in range(0, len(hours2)):
		if hours2[i] not in hoursfw :
			valuefw.insert(i, 0)
		if hours2[i] not in hoursids :
			valueids.insert(i, 0)
		if hours2[i] not in hoursrad :
			valuerad.insert(i, 0)
		if hours2[i] not in hoursred :
			valuered.insert(i, 0)
		if hours2[i] not in hourstraf :
			valuetraf.insert(i, 0)
		if hours2[i] not in hourswifi :
			valuewifi.insert(i, 0)
		if hours2[i] not in hourssiem :
			valuesiem.insert(i, 0)
		if hours2[i] not in hoursblue :
			valueblue.insert(i, 0)
	#Eliminamos los registros que esten dentro de los 10 primeros segundos de cada registro
	#sumamos los valores de los registros en esos 10 primeros segundos
	contador = len(hours2)
	contpop = 0
	for i in range(0, len(hours2)):
		global step
		if i < contador :
			contpop = 0
			for y in range(0,len(hours2)) :
				if y < contador+contpop  and y>=i :
					if hours2[i]+step >= hours2[y - contpop] and hours2[y - contpop]!=hours2[i] :
						hours2.pop(y - contpop)
						valuefw[i]=valuefw[i]+valuefw[y - contpop]
						valuefw.pop(y - contpop)
						valueids[i]=valueids[i]+valueids[y - contpop]
						valueids.pop(y - contpop)
						valuerad[i]=valuerad[i]+valuerad[y - contpop]
						valuerad.pop(y - contpop)
						valuered[i]=valuered[i]+valuered[y - contpop]
						valuered.pop(y - contpop)
						valuetraf[i]=valuetraf[i]+valuetraf[y - contpop]
						valuetraf.pop(y - contpop)
						valuewifi[i]=valuewifi[i]+valuewifi[y - contpop]
						valuewifi.pop(y - contpop)
						valueblue[i]=valueblue[i]+valueblue[y - contpop]
						valueblue.pop(y - contpop)
						valuesiem[i]=valuesiem[i]+valuesiem[y - contpop]
						valuesiem.pop(y - contpop)
						contador = len(hours2)
						contpop = contpop + 1

	index = np.arange(len(hours2))
	plt.bar(index, valuefw, label='firewall')
	plt.bar(index, valueids, label='ids_suricata', bottom=np.array(valuefw))
	plt.bar(index, valuerad, label='radio_frec', bottom=np.array(valuefw) + np.array(valueids))
	plt.bar(index, valuered, label='redes_mov', bottom=np.array(valuefw) + np.array(valueids) + np.array(valuerad))
	plt.bar(index, valuewifi, label='wifi', bottom=np.array(valuefw) + np.array(valueids) + np.array(valuerad) + np.array(valuered))
	plt.bar(index, valuetraf, label='traf_ids', bottom=np.array(valuefw) + np.array(valueids) + np.array(valuerad) + np.array(valuered) +np.array(valuewifi))
	plt.bar(index, valuesiem, label='siem', bottom=np.array(valuefw) + np.array(valueids) + np.array(valuerad) + np.array(valuered) +np.array(valuewifi)+ np.array(valuetraf))
	plt.bar(index, valueblue, label='bluetooth', bottom=np.array(valuefw) + np.array(valueids) + np.array(valuerad) + np.array(valuered) +np.array(valuewifi)+ np.array(valuetraf) + np.array(valuesiem))
	plt.xticks(index,hours2)
	plt.xticks(rotation=90)
	plt.ylabel("Number of records")
	plt.xlabel("Date")
	plt.title('Total time')
	plt.legend()
	plt.savefig("totalTime.png", bbox_inches="tight", pad_inches = 0.3)
	plt.close()


#Esto es para pintar grfiacas de correlaciones
def datosMatrix(fw,ids_s,radio_f,redes_mov,traf_ids,wifi, siem, bluetooth, t):
	hours=[]
	hoursfw=[]
	hoursids=[]
	hoursrad=[]
	hoursred=[]
	hourstraf=[]
	hourswifi=[]
	hourssiem=[]
	hoursblue=[]
	hoursfw2=[]
	hoursids2=[]
	hoursrad2=[]
	hoursred2=[]
	hourstraf2=[]
	hourswifi2=[]
	hourssiem2=[]
	hoursblue2=[]
	valuefw=[]
	valueids=[]
	valuerad=[]
	valuered=[]
	valuewifi=[]
	valuetraf=[]
	valuesiem=[]
	valueblue=[]
	for i in range(0, len(fw)):
		hours.append(int(fw[i][0]))
		hoursfw.append(int(fw[i][0]))
		valuefw.append(int(fw[i][1]))
	for i in range(0, len(ids_s)):
		hours.append(int(ids_s[i][0]))
		hoursids.append(int(ids_s[i][0]))
		valueids.append(int(ids_s[i][1]))
	for i in range(0, len(radio_f)):
		hours.append(int(radio_f[i][0]))
		hoursrad.append(int(radio_f[i][0]))
		valuerad.append(int(radio_f[i][1]))
	for i in range(0, len(redes_mov)):
		hours.append(int(redes_mov[i][0]))
		hoursred.append(int(redes_mov[i][0]))
		valuered.append(int(redes_mov[i][1]))
	for i in range(0, len(traf_ids)):
		hours.append(int(traf_ids[i][0]))
		hourstraf.append(int(traf_ids[i][0]))
		valuetraf.append(int(traf_ids[i][1]))
	for i in range(0, len(wifi)):
		hours.append(wifi[i][0])
		hourswifi.append(wifi[i][0])
		valuewifi.append(wifi[i][1])
	for i in range(0, len(siem)):
		hours.append(siem[i][0])
		hourssiem.append(siem[i][0])
		valuesiem.append(siem[i][1])
	for i in range(0, len(bluetooth)):
		hours.append(bluetooth[i][0])
		hoursblue.append(bluetooth[i][0])
		valueblue.append(bluetooth[i][1])
	hours.sort()
	#Elimina los elemento duplicados
	hours2 = sorted(list(set(hours)))
	#Ponemos en todos los sensores el mismo numero de registros, con un 0 
	for i in range(0, len(hours2)):
		if hours2[i] not in hoursfw :
			valuefw.insert(i, 0)
		if hours2[i] not in hoursids :
			valueids.insert(i, 0)
		if hours2[i] not in hoursrad :
			valuerad.insert(i, 0)
		if hours2[i] not in hoursred :
			valuered.insert(i, 0)
		if hours2[i] not in hourstraf :
			valuetraf.insert(i, 0)
		if hours2[i] not in hourswifi :
			valuewifi.insert(i, 0)
		if hours2[i] not in hourssiem :
			valuesiem.insert(i, 0)
		if hours2[i] not in hoursblue :
			valueblue.insert(i, 0)
	#Eliminamos los registros que esten dentro de los X primeros segundos de cada registro
	#sumamos los valores de los registros en esos X primeros segundos
	contador = len(hours2)
	contpop = 0
	for i in range(0, len(hours2)):
		global step
		if i < contador :
			contpop = 0
			for y in range(0,len(hours2)) :
				if y < contador+contpop  and y>=i :
					if hours2[i]+step >= hours2[y - contpop] and hours2[y - contpop]!=hours2[i] :
						hours2.pop(y - contpop)
						valuefw[i]=valuefw[i]+valuefw[y - contpop]
						valuefw.pop(y - contpop)
						valueids[i]=valueids[i]+valueids[y - contpop]
						valueids.pop(y - contpop)
						valuerad[i]=valuerad[i]+valuerad[y - contpop]
						valuerad.pop(y - contpop)
						valuered[i]=valuered[i]+valuered[y - contpop]
						valuered.pop(y - contpop)
						valuetraf[i]=valuetraf[i]+valuetraf[y - contpop]
						valuetraf.pop(y - contpop)
						valuewifi[i]=valuewifi[i]+valuewifi[y - contpop]
						valuewifi.pop(y - contpop)
						valueblue[i]=valueblue[i]+valueblue[y - contpop]
						valueblue.pop(y - contpop)
						valuesiem[i]=valuesiem[i]+valuesiem[y - contpop]
						valuesiem.pop(y - contpop)
						contador = len(hours2)
						contpop = contpop + 1

	#Opción para tomar todos los registros en una misma fecha como si fuese solo 1, es decir, que existe anomalia en general en esa fecha
	if t==False:
		model = "Time-IndvAnomaly"
		for i in range(0, len(hours2)):
			if valuefw[i]>0:
				hoursfw2.append(hours2[i])
			else:
				hoursfw2.append(0)
			if valueids[i]>0:
				hoursids2.append(hours2[i])
			else:
				hoursids2.append(0)
			if valuerad[i]>0:
				hoursrad2.append(hours2[i])
			else:
				hoursrad2.append(0)
			if valuered[i]>0:
				hoursred2.append(hours2[i])
			else:
				hoursred2.append(0)
			if valuetraf[i]>0:
				hourstraf2.append(hours2[i])
			else:
				hourstraf2.append(0)
			if valuewifi[i]>0:
				hourswifi2.append(hours2[i])
			else:
				hourswifi2.append(0)
			if valuesiem[i]>0:
				hourssiem2.append(hours2[i])
			else:
				hourssiem2.append(0)
			if valueblue[i]>0:
				hoursblue2.append(hours2[i])
			else:
				hoursblue2.append(0)
	#Opcion para tener en cuenta cada uno de los registros de una fecha para realizar la correlacion
	else:
		model = "Time-NormalAnomalies"
		for i in range(0, len(hours2)):

			arr = np.array([valuefw[i], valueids[i], valuerad[i], valuered[i], valuetraf[i], valuewifi[i], valuesiem[i], valueblue[i]])
			maxval = np.amax(arr)

			if valuefw[i]>0:
				for y in range (0, valuefw[i]):
					hoursfw2.append(hours2[i])
				for y in range(0,maxval-valuefw[i]):
					hoursfw2.append(0)
			else:
				for y in range (0, maxval):
					hoursfw2.append(0)
			if valueids[i]>0:
				for y in range (0, valueids[i]):
					hoursids2.append(hours2[i])
				for y in range(0,maxval-valueids[i]):
					hoursids2.append(0)
			else:
				for y in range (0, maxval):
					hoursids2.append(0)
			if valuerad[i]>0:
				for y in range (0, valuerad[i]):
					hoursrad2.append(hours2[i])
				for y in range(0,maxval-valuerad[i]):
					hoursrad2.append(0)
			else:
				for y in range (0, maxval):
					hoursrad2.append(0)
			if valuered[i]>0:
				for y in range (0, valuered[i]):
					hoursred2.append(hours2[i])
				for y in range(0,maxval-valuered[i]):
					hoursred2.append(0)
			else:
				for y in range (0, maxval):
					hoursred2.append(0)
			if valuetraf[i]>0:
				for y in range (0, valuetraf[i]):
					hourstraf2.append(hours2[i])
				for y in range(0,maxval-valuetraf[i]):
					hourstraf2.append(0)
			else:
				for y in range (0, maxval):
					hourstraf2.append(0)
			if valuewifi[i]>0:
				for y in range (0, valuewifi[i]):
					hourswifi2.append(hours2[i])
				for y in range(0,maxval-valuewifi[i]):
					hourswifi2.append(0)
			else:
				for y in range (0, maxval):
					hourswifi2.append(0)
			if valuesiem[i]>0:
				for y in range (0, valuesiem[i]):
					hourssiem2.append(hours2[i])
				for y in range(0,maxval-valuesiem[i]):
					hourssiem2.append(0)
			else:
				for y in range (0, maxval):
					hourssiem2.append(0)
			if valueblue[i]>0:
				for y in range (0, valueblue[i]):
					hoursblue2.append(hours2[i])
				for y in range(0,maxval-valueblue[i]):
					hoursblue2.append(0)
			else:
				for y in range (0, maxval):
					hoursblue2.append(0)	

	global idfw
	global idids
	global idrad
	global idred
	global idtraf
	global idwifi
	global idblue
	global idsiem

#Comprobación de hipotesis nula para las horas
	pValue(hoursfw2,"Firewall", hoursids2,"ids_suricata", idfw, idids, hours2, model)
	pValue(hoursfw2,"Firewall", hoursrad2,"radio_frecuencia", idfw, idrad, hours2, model)
	pValue(hoursfw2,"Firewall", hoursred2,"redes_moviles", idfw, idred, hours2, model)
	pValue(hoursfw2,"Firewall", hourstraf2,"trafico_ids", idfw, idtraf, hours2, model)
	pValue(hoursfw2,"Firewall", hourswifi2,"wifi", idfw, idwifi, hours2, model)
	pValue(hoursfw2,"Firewall", hourssiem2,"siem", idfw, idsiem, hours2, model)
	pValue(hoursfw2,"Firewall", hoursblue2,"bluetooth", idfw, idblue, hours2, model)
	pValue(hoursids2,"ids_suricata", hoursrad2,"radio_frecuencia", idids, idrad, hours2, model)
	pValue(hoursids2,"ids_suricata", hoursred2,"redes_moviles", idids, idred, hours2, model)
	pValue(hoursids2,"ids_suricata", hourstraf2,"trafico_ids", idids, idtraf, hours2, model)
	pValue(hoursids2,"ids_suricata", hourswifi2,"wifi", idids, idwifi, hours2, model)
	pValue(hoursids2,"ids_suricata", hourssiem2,"siem", idids, idsiem, hours2, model)
	pValue(hoursids2,"ids_suricata", hoursblue2,"bluetooth", idids, idblue, hours2, model)
	pValue(hoursrad2,"radio_frecuencia", hoursred2,"redes_moviles", idrad, idred, hours2, model)
	pValue(hoursrad2,"radio_frecuencia", hourstraf2,"trafico_ids", idrad, idtraf, hours2, model)
	pValue(hoursrad2,"radio_frecuencia", hourswifi2,"wifi", idrad, idwifi, hours2, model)
	pValue(hoursrad2,"radio_frecuencia", hourssiem2,"siem", idrad, idsiem, hours2, model)
	pValue(hoursrad2,"radio_frecuencia", hoursblue2,"bluetooth", idrad, idblue, hours2, model)
	pValue(hoursred2,"redes_moviles", hourstraf2,"trafico_ids", idred, idtraf, hours2, model)
	pValue(hoursred2,"redes_moviles", hourswifi2,"wifi", idred, idwifi, hours2, model)
	pValue(hoursred2,"redes_moviles", hourssiem2,"siem", idred, idsiem, hours2, model)
	pValue(hoursred2,"redes_moviles", hoursblue2,"bluetooth", idred, idblue, hours2, model)
	pValue(hourstraf2,"trafico_ids", hourswifi2,"wifi", idtraf, idwifi, hours2, model)
	pValue(hourstraf2,"trafico_ids", hourssiem2,"siem", idtraf, idsiem, hours2, model)
	pValue(hourstraf2,"trafico_ids", hoursblue2,"bluetooth", idtraf, idblue, hours2, model)
	pValue(hourswifi2,"wifi", hourssiem2,"siem", idwifi, idsiem, hours2, model)
	pValue(hourswifi2,"wifi", hoursblue2,"bluetooth", idwifi, idblue, hours2, model)
	pValue(hourssiem2,"siem", hoursblue2,"bluetooth", idsiem, idblue, hours2, model)
	
	
#Comprobación de hipotesis nula para las frecuencias
	if t==True:
		pValue(valuefw,"Firewall", valueids,"ids_suricata", idfw, idids, hours2, "Time-Freq")
		pValue(valuefw,"Firewall", valuerad,"radio_frecuencia", idfw, idrad, hours2, "Time-Freq")
		pValue(valuefw,"Firewall", valuered,"redes_moviles", idfw, idred, hours2, "Time-Freq")
		pValue(valuefw,"Firewall", valuetraf,"trafico_ids", idfw, idtraf, hours, "Time-Freq")
		pValue(valuefw,"Firewall", valuewifi,"wifi", idfw, idwifi, hours2, "Time-Freq")
		pValue(valuefw,"Firewall", valuesiem,"siem", idfw, idsiem, hours2, "Time-Freq")
		pValue(valuefw,"Firewall", valueblue,"bluetooth", idfw, idblue, hours2, "Time-Freq")
		pValue(valueids,"ids_suricata", valuerad,"radio_frecuencia", idids, idrad, hours2, "Time-Freq")
		pValue(valueids,"ids_suricata", valuered,"redes_moviles", idids, idred, hours2, "Time-Freq")
		pValue(valueids,"ids_suricata", valuetraf,"trafico_ids", idids, idtraf, hours2, "Time-Freq")
		pValue(valueids,"ids_suricata", valuewifi,"wifi", idids, idwifi, hours2, "Time-Freq")
		pValue(valueids,"ids_suricata", valuesiem,"siem", idids, idsiem, hours2, "Time-Freq")
		pValue(valueids,"ids_suricata", valueblue,"bluetooth", idids, idblue, hours2, "Time-Freq")
		pValue(valuerad,"radio_frecuencia", valuered,"redes_moviles", idrad, idred, hours2, "Time-Freq")
		pValue(valuerad,"radio_frecuencia", valuetraf,"trafico_ids", idrad, idtraf, hours2, "Time-Freq")
		pValue(valuerad,"radio_frecuencia", valuewifi,"wifi", idrad, idwifi, hours2, "Time-Freq")
		pValue(valuerad,"radio_frecuencia", valuesiem,"siem", idrad, idsiem, hours2, "Time-Freq")
		pValue(valuerad,"radio_frecuencia", valueblue,"bluetooth", idrad, idblue, hours2, "Time-Freq")
		pValue(valuered,"redes_moviles", valuetraf,"trafico_ids", idred, idtraf, hours2, "Time-Freq")
		pValue(valuered,"redes_moviles", valuewifi,"wifi", idred, idwifi, hours2, "Time-Freq")
		pValue(valuered,"redes_moviles", valuesiem,"siem", idred, idsiem, hours2, "Time-Freq")
		pValue(valuered,"redes_moviles", valueblue,"bluetooth", idred, idblue, hours2, "Time-Freq")
		pValue(valuetraf,"trafico_ids", valuewifi,"wifi", idtraf, idwifi, hours2, "Time-Freq")
		pValue(valuetraf,"trafico_ids", valuesiem,"siem", idtraf, idsiem, hours2, "Time-Freq")
		pValue(valuetraf,"trafico_ids", valueblue,"bluetooth", idtraf, idblue, hours2, "Time-Freq")
		pValue(valuewifi,"wifi", valuesiem,"siem", idwifi, idsiem, hours2, "Time-Freq")
		pValue(valuewifi,"wifi", valueblue,"bluetooth", idwifi, idblue, hours2, "Time-Freq")
		pValue(valuesiem,"siem", valueblue,"bluetooth", idsiem, idblue, hours2, "Time-Freq")
	
	
def pValue(sensor1,sname1, sensor2, sname2, array1, array2, hours, model):
	#La longitud debe ser mayor de 2 ya que sino no se puede calcular la correlacion
	if len(sensor1)>=2 and len(sensor2)>=2:

		if model = "Time-Freq":
			hipCorr = spearmanr(sensor1,sensor2)
			if hipCorr[0]>=umbral and hipCorr[1]<= hipnull:
				alert(sname1, sname2, array1, array2, hours, "spearman", hipCorr[0], model)
		else:
			hipCorr = pearsonr(sensor1,sensor2)
			if hipCorr[0]>=umbral and hipCorr[1]<= hipnull:
				alert(sname1, sname2, array1, array2, hours, "pearson", hipCorr[0], model)


def datosMatrix2(fw,ids_s,radio_f,redes_mov,traf_ids,wifi, siem, bluetooth, t):
	hours=[]
	hoursfw=[]
	hoursids=[]
	hoursrad=[]
	hoursred=[]
	hourstraf=[]
	hourswifi=[]
	hourssiem=[]
	hoursblue=[]
	hoursfw2=[]
	hoursids2=[]
	hoursrad2=[]
	hoursred2=[]
	hourstraf2=[]
	hourswifi2=[]
	hourssiem2=[]
	hoursblue2=[]
	valuefw=[]
	valueids=[]
	valuerad=[]
	valuered=[]
	valuewifi=[]
	valuetraf=[]
	valuesiem=[]
	valueblue=[]
	for i in range(0, len(fw)):
		hours.append(int(fw[i][0]))
		hoursfw.append(int(fw[i][0]))
		valuefw.append(int(fw[i][1]))
	for i in range(0, len(ids_s)):
		hours.append(int(ids_s[i][0]))
		hoursids.append(int(ids_s[i][0]))
		valueids.append(int(ids_s[i][1]))
	for i in range(0, len(radio_f)):
		hours.append(int(radio_f[i][0]))
		hoursrad.append(int(radio_f[i][0]))
		valuerad.append(int(radio_f[i][1]))
	for i in range(0, len(redes_mov)):
		hours.append(int(redes_mov[i][0]))
		hoursred.append(int(redes_mov[i][0]))
		valuered.append(int(redes_mov[i][1]))
	for i in range(0, len(traf_ids)):
		hours.append(int(traf_ids[i][0]))
		hourstraf.append(int(traf_ids[i][0]))
		valuetraf.append(int(traf_ids[i][1]))
	for i in range(0, len(wifi)):
		hours.append(wifi[i][0])
		hourswifi.append(wifi[i][0])
		valuewifi.append(wifi[i][1])
	for i in range(0, len(siem)):
		hours.append(siem[i][0])
		hourssiem.append(siem[i][0])
		valuesiem.append(siem[i][1])
	for i in range(0, len(bluetooth)):
		hours.append(bluetooth[i][0])
		hoursblue.append(bluetooth[i][0])
		valueblue.append(bluetooth[i][1])
	hours.sort()
	#Elimina los elemento duplicados
	hours2 = sorted(list(set(hours)))
	#Ponemos en todos los sensores elmismo numero de registros, con un 0 
	for i in range(0, len(hours2)):
		if hours2[i] not in hoursfw :
			valuefw.insert(i, 0)
		if hours2[i] not in hoursids :
			valueids.insert(i, 0)
		if hours2[i] not in hoursrad :
			valuerad.insert(i, 0)
		if hours2[i] not in hoursred :
			valuered.insert(i, 0)
		if hours2[i] not in hourstraf :
			valuetraf.insert(i, 0)
		if hours2[i] not in hourswifi :
			valuewifi.insert(i, 0)
		if hours2[i] not in hourssiem :
			valuesiem.insert(i, 0)
		if hours2[i] not in hoursblue :
			valueblue.insert(i, 0)
	#Eliminamos los registros que esten dentro de los 10 primeros segundos de cada registro
	#sumamos los valores de los registros en esos 10 primeros segundos
	contador = len(hours2)
	contpop = 0
	for i in range(0, len(hours2)):
		global step
		if i < contador :
			contpop = 0
			for y in range(0,len(hours2)) :
				if y < contador+contpop  and y>=i :
					if hours2[i]+step >= hours2[y - contpop] and hours2[y - contpop]!=hours2[i] :
						hours2.pop(y - contpop)
						valuefw[i]=valuefw[i]+valuefw[y - contpop]
						valuefw.pop(y - contpop)
						valueids[i]=valueids[i]+valueids[y - contpop]
						valueids.pop(y - contpop)
						valuerad[i]=valuerad[i]+valuerad[y - contpop]
						valuerad.pop(y - contpop)
						valuered[i]=valuered[i]+valuered[y - contpop]
						valuered.pop(y - contpop)
						valuetraf[i]=valuetraf[i]+valuetraf[y - contpop]
						valuetraf.pop(y - contpop)
						valuewifi[i]=valuewifi[i]+valuewifi[y - contpop]
						valuewifi.pop(y - contpop)
						valueblue[i]=valueblue[i]+valueblue[y - contpop]
						valueblue.pop(y - contpop)
						valuesiem[i]=valuesiem[i]+valuesiem[y - contpop]
						valuesiem.pop(y - contpop)
						contador = len(hours2)
						contpop = contpop + 1

	if t==False:
		for i in range(0, len(hours2)):
			if valuefw[i]>0:
				hoursfw2.append(hours2[i])
			else:
				hoursfw2.append(0)
			if valueids[i]>0:
				hoursids2.append(hours2[i])
			else:
				hoursids2.append(0)
			if valuerad[i]>0:
				hoursrad2.append(hours2[i])
			else:
				hoursrad2.append(0)
			if valuered[i]>0:
				hoursred2.append(hours2[i])
			else:
				hoursred2.append(0)
			if valuetraf[i]>0:
				hourstraf2.append(hours2[i])
			else:
				hourstraf2.append(0)
			if valuewifi[i]>0:
				hourswifi2.append(hours2[i])
			else:
				hourswifi2.append(0)
			if valuesiem[i]>0:
				hourssiem2.append(hours2[i])
			else:
				hourssiem2.append(0)
			if valueblue[i]>0:
				hoursblue2.append(hours2[i])
			else:
				hoursblue2.append(0)
	else:
		for i in range(0, len(hours2)):

			arr = np.array([valuefw[i], valueids[i], valuerad[i], valuered[i], valuetraf[i], valuewifi[i], valuesiem[i], valueblue[i]])
			maxval = np.amax(arr)

			if valuefw[i]>0:
				for y in range (0, valuefw[i]):
					hoursfw2.append(hours2[i])
				for y in range(0,maxval-valuefw[i]):
					hoursfw2.append(0)
			else:
				for y in range (0, maxval):
					hoursfw2.append(0)
			if valueids[i]>0:
				for y in range (0, valueids[i]):
					hoursids2.append(hours2[i])
				for y in range(0,maxval-valueids[i]):
					hoursids2.append(0)
			else:
				for y in range (0, maxval):
					hoursids2.append(0)
			if valuerad[i]>0:
				for y in range (0, valuerad[i]):
					hoursrad2.append(hours2[i])
				for y in range(0,maxval-valuerad[i]):
					hoursrad2.append(0)
			else:
				for y in range (0, maxval):
					hoursrad2.append(0)
			if valuered[i]>0:
				for y in range (0, valuered[i]):
					hoursred2.append(hours2[i])
				for y in range(0,maxval-valuered[i]):
					hoursred2.append(0)
			else:
				for y in range (0, maxval):
					hoursred2.append(0)
			if valuetraf[i]>0:
				for y in range (0, valuetraf[i]):
					hourstraf2.append(hours2[i])
				for y in range(0,maxval-valuetraf[i]):
					hourstraf2.append(0)
			else:
				for y in range (0, maxval):
					hourstraf2.append(0)
			if valuewifi[i]>0:
				for y in range (0, valuewifi[i]):
					hourswifi2.append(hours2[i])
				for y in range(0,maxval-valuewifi[i]):
					hourswifi2.append(0)
			else:
				for y in range (0, maxval):
					hourswifi2.append(0)
			if valuesiem[i]>0:
				for y in range (0, valuesiem[i]):
					hourssiem2.append(hours2[i])
				for y in range(0,maxval-valuesiem[i]):
					hourssiem2.append(0)
			else:
				for y in range (0, maxval):
					hourssiem2.append(0)
			if valueblue[i]>0:
				for y in range (0, valueblue[i]):
					hoursblue2.append(hours2[i])
				for y in range(0,maxval-valueblue[i]):
					hoursblue2.append(0)
			else:
				for y in range (0, maxval):
					hoursblue2.append(0)	
		
#Para sacar las gráficas
	matrixCorr(hoursfw2,hoursids2,hoursrad2,hoursred2,hourstraf2,hourswifi2,hourssiem2,hoursblue2, "pearson")
	matrixCorr(hoursfw2,hoursids2,hoursrad2,hoursred2,hourstraf2,hourswifi2,hourssiem2,hoursblue2, "spearman")
	matrixCorr(hoursfw2,hoursids2,hoursrad2,hoursred2,hourstraf2,hourswifi2,hourssiem2,hoursblue2, "kendall")
	matrixCorr(valuefw,valueids,valuerad,valuered,valuetraf,valuewifi,valuesiem,valueblue, "pearson")
	matrixCorr(valuefw,valueids,valuerad,valuered,valuetraf,valuewifi,valuesiem,valueblue, "spearman")
	matrixCorr(valuefw,valueids,valuerad,valuered,valuetraf,valuewifi,valuesiem,valueblue, "kendall")


def matrixCorr(fw,ids_s,radio_f,redes_mov,traf_ids,wifi, siem, bluetooth, corr):
	sensors_df = pd.DataFrame({
		'Firewall': fw,
		'ids_suricata': ids_s,
		'radio_frec': radio_f,
		'redes_mov': redes_mov,
		'traf_ids': traf_ids,
		'wifi': wifi,
		'siem': siem,
		'bluetooth': bluetooth
	})

	if corr == "pearson":
		corr_df = sensors_df.corr(method='pearson')
	elif corr == "spearman":
		corr_df = sensors_df.corr(method='spearman')
	else:
		corr_df = sensors_df.corr(method='kendall')	

	plt.figure(figsize=(8,6))
	sns.heatmap(corr_df, annot=True)
	plt.savefig("matrixCorr"+ corr +".png", bbox_inches="tight", pad_inches = 0.3)





	#Codigo para preparar los logs
def pred1(sensor, t):
	c = 0
	recordlist=[]
	timelist=[]
	ind = 0
	first = True
	if sensor == "ids_suricata" or sensor == "trafico_ids":
		res1 = es.search(index=sensor, body={"size":10000, "query":{ "bool":{ "must": [{"range": { t:{ "gte":time.mktime(time.localtime())-execution, "lte":time.mktime(time.localtime())}}}, {"match":{"prediction": "1"}}]}}})
	else:
		res1 = es.search(index=sensor, body={"size":10000, "query":{ "bool":{ "must": [{"range": { t:{ "gte": exe, "lte":"now"}}}, {"match":{"anomalia": True}}]}}})
	for hit in res1['hits']['hits']:
		c = c +1
		#convert same type of Epoch time
		if sensor == "ids_suricata" or sensor == "trafico_ids":
			mytm = (hit['_source'][t])
		else:
			mytma= (hit['_source'][t])
			mytm = mytma[0:19]
		fmt = ("%Y-%m-%dT%H:%M:%S")
		if sensor == "ids_suricata":
			epochDate= (math.floor(mytm))
		elif sensor == "trafico_ids":
			h= str(mytm)
			temp = len(h)
			epochDate =int(h[:temp - 3])
		else:
			epochDate = int(calendar.timegm(time.strptime(mytm, fmt)))

		if sensor == "firewall":
			global firewallTs
			firewallTs.append(int(epochDate))
			firewallTs.sort()
		if sensor == "ids_suricata":
			global ids_suricataTs
			ids_suricataTs.append(int(epochDate))
			ids_suricataTs.sort()
		if sensor == "radio_frecuencia":
			global radio_frecuenciaTs
			radio_frecuenciaTs.append(int(epochDate))
			radio_frecuenciaTs.sort()
		if sensor == "redes_moviles":
			global redes_movilesTs
			redes_movilesTs.append(int(epochDate))
			redes_movilesTs.sort()
		if sensor == "trafico_ids":
			global trafico_idsTs
			trafico_idsTs.append(int(epochDate))
			trafico_idsTs.sort()
		if sensor == "wifi":
			global wifiTs
			wifiTs.append(int(epochDate))
			wifiTs.sort()
		if sensor == "bluetooth":
			global bluetoothTs
			bluetoothTs.append(int(epochDate))
			bluetoothTs.sort()
		if sensor == "siem":
			global siemTs
			siemTs.append(int(epochDate))
			siemTs.sort()

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

	timeSort = sorted(timelist, key= lambda time : time[0])
	if sensor == "firewall":
		global firewallT
		firewallT = timeSort
	if sensor == "ids_suricata":
		global ids_suricataT
		ids_suricataT = timeSort
	if sensor == "radio_frecuencia":
		global radio_frecuenciaT
		radio_frecuenciaT = timeSort
	if sensor == "redes_moviles":
		global redes_movilesT
		redes_movilesT = timeSort
	if sensor == "trafico_ids":
		global trafico_idsT
		trafico_idsT = timeSort
	if sensor == "wifi":
		global wifiT
		wifiT = timeSort
	if sensor == "bluetooth":
		global bluetoothT
		bluetoothT = timeSort
	if sensor == "siem":
		global siemT
		siemT = timeSort

#Escirbe todos los logs de cada sensor
def write(sensor):
	c = 0
	res1 = es.search(index=sensor, body={"size":10000})
	fout = open("./"+ sensor+".txt", "w")
	for hit in res1['hits']['hits']:
		#Write a file with all the registers "prediction=1"
		fout.write(str(hit)+"\n\n")
		c = c +1
	print(sensor + ": got %d Hits" % c)
	fout.close()



#Para sacar las correlaciones de los tiempo de recepcion:
pred2("firewall",'Time')
pred2("ids_suricata", 'timestamp')
pred2("radio_frecuencia", 'time')
pred2("redes_moviles", 'time')
pred2("trafico_ids",'time_stamp')
pred2("wifi",'time')
pred2("bluetooth",'last_seen')
pred2("siem",'Date')
drawgrafictimetotal(firewallT2,ids_suricataT2,radio_frecuenciaT2,redes_movilesT2,trafico_idsT2,wifiT2, siemT2, bluetoothT2)


#Correlation between time and timestamp
correTimeTimestamp("firewall",firewallTim, firewallTs)
correTimeTimestamp("ids_suricata",ids_suricataTim, ids_suricataTs)
correTimeTimestamp("radio_frecuencia",radio_frecuenciaTim, radio_frecuenciaTs)
correTimeTimestamp("redes_moviles", redes_movilesTim, redes_movilesTs)
correTimeTimestamp("traf_ids", trafico_idsTim, trafico_idsTs)
correTimeTimestamp("wifi",wifiTim, wifiTs)
correTimeTimestamp("siem",siemTim, siemTs)
correTimeTimestamp("bluetooth",bluetoothTim, bluetoothTs)

datosMatrix(firewallT,ids_suricataT,radio_frecuenciaT,redes_movilesT,trafico_idsT,wifiT, siemT, bluetoothT, True)
datosMatrix(firewallT,ids_suricataT,radio_frecuenciaT,redes_movilesT,trafico_idsT,wifiT, siemT, bluetoothT, False)


#Para escribir los ficheros con todos los registros
write("firewall")
write("ids_suricata")
write("radio_frecuencia")
write("redes_moviles")
write("trafico_ids")
write("wifi")
write("bluetooth")
write("siem")