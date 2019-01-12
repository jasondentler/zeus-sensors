import os
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'

def get_devices():
	devices = glob.glob(base_dir + '28*')
	for device in devices:
		yield device + '/w1_slave'

def read_temp_raw():
	devices = get_devices()
	for device in devices:
		f = open(device, 'r')
		lines = f.readlines()
		f.close()
		yield device, lines

def read_temp():
	data = read_temp_raw()
	for item in data:
		device, lines = item
		if lines[0].strip()[-3:] != 'YES':
			print('Device ' + device + ' not ready')
			continue;
		print('Read device ' + device)
		equals_pos = lines[1].find('t=')
		if equals_pos != -1:
			temp_string = lines[1][equals_pos+2:]
			temp_c = float(temp_string) / 1000.0
			temp_f = temp_c * 9.0 / 5.0 + 32.0
			yield device, temp_c, temp_f

while True:
	data = read_temp()
	for item in data:
		print(item)
	time.sleep(1)

