#!/usr/bin/python

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
Motor1A = 26
Motor1B = 24
Motor1E = 22
Motor2A = 32
Motor2B = 36
Motor2E = 38
GPIO.setup(40,GPIO.OUT)
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)
import time

from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

spd = 0

@app.route('/')
def index():
    return render_template('drive.html')

@socketio.on('command', namespace='/car')
def command(message):
	if message['cmd'] == 37:
		drive('L')
	elif message['cmd'] == 38:
		global spd
		if spd != 255: spd += 1
		drive('U')
	elif message['cmd'] == 39:
		drive('R')
	elif message['cmd'] == 40:
		global spd
		if spd != 0: spd -= 1
		drive('D')
	elif message['cmd'] == 83:
		global spd
		spd = 0
		drive('S')
	elif message['cmd'] == 0:
		print 'off'
		drive('0')
	elif message['cmd'] == 1:
		print 'on'
		drive('1')
		
def drive(sts):
	if sts == 'U':
		GPIO.output(Motor1A,GPIO.HIGH)
		GPIO.output(Motor1B,GPIO.LOW)
		GPIO.output(Motor1E,GPIO.HIGH)
		GPIO.output(Motor2A,GPIO.HIGH)
		GPIO.output(Motor2B,GPIO.LOW)
		GPIO.output(Motor2E,GPIO.HIGH)
		print sts, " ", spd
	elif sts == 'D':
		GPIO.output(Motor1A,GPIO.LOW)
		GPIO.output(Motor1B,GPIO.HIGH)
		GPIO.output(Motor1E,GPIO.HIGH)
		GPIO.output(Motor2A,GPIO.LOW)
		GPIO.output(Motor2B,GPIO.HIGH)
		GPIO.output(Motor2E,GPIO.HIGH)
		print sts, " ", spd
	elif sts == 'L':
		GPIO.output(Motor1E,GPIO.HIGH)
		GPIO.output(Motor2E,GPIO.LOW)
		print sts, " ", spd
	elif sts == 'R':
		GPIO.output(Motor1E,GPIO.LOW)
		GPIO.output(Motor2E,GPIO.HIGH)
		print sts, " ", spd
	elif sts == 'S':
		GPIO.output(Motor1E,GPIO.LOW)
		GPIO.output(Motor2E,GPIO.LOW)
		print sts, " ", spd
	elif sts == '0':
		GPIO.output(40,GPIO.LOW)
	elif sts == '1':
		GPIO.output(40,GPIO.HIGH)

if __name__ == '__main__':
    app.debug = True
    socketio.run(app, host='0.0.0.0')
