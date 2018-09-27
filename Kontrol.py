#!/usr/bin/python
# -*- coding: iso-8859-9 -*-
import sys
import os
import glob
import RPi.GPIO as GPIO
import time
import datetime
from time import sleep


localtime = time.asctime( time.localtime(time.time()) )

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

GPIO.setmode (GPIO.BCM)

#Uyarilari Gosterme

GPIO.setwarnings(False)

#Kullanilacak Anahtar icin Pin Numaralari

pinListesi = [17, 27, 22, 18]

while True:
 MinDeger = input("En dÃ¼ÅÃ¼k sÄ±caklÄ±ÄÄ± belirleyiniz:")
 MaxDeger = input("En yÃ¼ksek sÄ±caklÄ±ÄÄ± belirleyiniz:")
 if MinDeger>=MaxDeger:
   print("En dÃ¼ÅÃ¼k sÄ±caklÄ±k, en yÃ¼ksek sÄ±caklÄ±ktan bÃ¼yÃ¼k veya eÅit olamaz.")
 else:
   break

MinOrtamSicakligi = MinDeger
MaxOrtamSicakligi = MaxDeger

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')




for i in pinListesi: 
    GPIO.setup(i, GPIO.OUT) 
    GPIO.output(i, GPIO.HIGH)

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c

while True:
   print "BaÅlama zamanÄ±:", localtime
   if read_temp() < MinOrtamSicakligi:
	GPIO.output(18, GPIO.LOW)
	GPIO.output(22, GPIO.LOW)
	print 'Rezistans ve motor Ã§alÄ±ÅtÄ±rÄ±ldÄ±.', 'SÄ±caklÄ±k', read_temp(), 'C derece.'
   else:
	GPIO.output(18, GPIO.HIGH)
	GPIO.output(22, GPIO.HIGH)
	print 'Rezistans ve motor durduruldu', 'SÄ±caklÄ±k', read_temp(), 'C derece.'
   if read_temp() >= MaxOrtamSicakligi:
	GPIO.output(17, GPIO.LOW)
	GPIO.output(27, GPIO.LOW)
	print "SoÄutucu ve motor Ã§alÄ±ÅtÄ±rÄ±ldÄ±", "SÄ±caklÄ±k", read_temp(), "C derece."
   else:
	GPIO.output(17, GPIO.HIGH)
	GPIO.output(27, GPIO.HIGH)
	print "SoÄutucu ve motor durduruldu", "SÄ±caklÄ±k", read_temp(), "C derece."
#   print(read_temp()) 
   sleep(60)
print "Local current time :", localtime

