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
 MinDeger = input("En düşük sıcaklığı belirleyiniz:")
 MaxDeger = input("En yüksek sıcaklığı belirleyiniz:")
 if MinDeger>=MaxDeger:
   print("En düşük sıcaklık, en yüksek sıcaklıktan büyük veya eşit olamaz.")
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
   print "Başlama zamanı:", localtime
   if read_temp() < MinOrtamSicakligi:
	GPIO.output(17, GPIO.LOW)
	GPIO.output(22, GPIO.LOW)
	print 'Rezistans ve motor çalıştırıldı.', 'Sıcaklık', read_temp(), 'C derece.'
   else:
	GPIO.output(17, GPIO.HIGH)
	GPIO.output(22, GPIO.HIGH)
	print 'Rezistans ve motor durduruldu', 'Sıcaklık', read_temp(), 'C derece.'
   if read_temp() >= MaxOrtamSicakligi:
	GPIO.output(17, GPIO.LOW)
	GPIO.output(27, GPIO.LOW)
	print "Soğutucu ve motor çalıştırıldı", "Sıcaklık", read_temp(), "C derece."
   else:
	GPIO.output(17, GPIO.HIGH)
	GPIO.output(27, GPIO.HIGH)
	print "Soğutucu ve motor durduruldu", "Sıcaklık", read_temp(), "C derece."
#   print(read_temp()) 
   sleep(60)
print "Local current time :", localtime
