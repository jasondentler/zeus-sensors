import os
import time
import math
import pygame, sys
from pygame.locals import *
import RPi.GPIO as GPIO

boardRevision = GPIO.RPI_REVISION
GPIO.setmode(GPIO.BCM) # use real GPIO numbering
GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_UP)

pygame.init()

VIEW_WIDTH = 0
VIEW_HEIGHT = 0
pygame.display.set_caption('Flow')

pouring = False
lastPinState = False
pinState = 0
lastPinChange = int(time.time() * 1000)
pourStart = 0
pinChange = lastPinChange
pinDelta = 0
hertz = 0
flow = 0
litersPoured = 0
pintsPoured = 0
tweet = ''
BLACK = (0,0,0)
WHITE = (255, 255, 255)

windowSurface = pygame.display.set_mode((VIEW_WIDTH,VIEW_HEIGHT), FULLSCREEN, 32)
FONTSIZE = 48
LINEHEIGHT = 52
basicFont = pygame.font.SysFont(None, FONTSIZE)

def renderThings(lastPinChange, pinChange, pinDelta, hertz, flow, pintsPoured, pouring, pourStart, tweet, windowSurface, basicFont):
  # Clear the screen
  windowSurface.fill(BLACK)
  
  # Draw LastPinChange
  text = basicFont.render('Last Pin Change: '+time.strftime('%H:%M:%S', time.localtime(lastPinChange/1000)), True, WHITE, BLACK)
  textRect = text.get_rect()
  windowSurface.blit(text, (40,1*LINEHEIGHT))
  
  # Draw PinChange
  text = basicFont.render('Pin Change: '+time.strftime('%H:%M:%S', time.localtime(pinChange/1000)), True, WHITE, BLACK)
  textRect = text.get_rect()
  windowSurface.blit(text, (40,2*LINEHEIGHT))
  
  # Draw PinDelta
  text = basicFont.render('Pin Delta: '+str(pinDelta) + ' ms', True, WHITE, BLACK)
  textRect = text.get_rect()
  windowSurface.blit(text, (40,3*LINEHEIGHT))
  
  # Draw hertz
  text = basicFont.render('Hertz: '+str(hertz) + 'Hz', True, WHITE, BLACK)
  textRect = text.get_rect()
  windowSurface.blit(text, (40,4*LINEHEIGHT))

  # Draw instantaneous speed
  text = basicFont.render('Flow: '+str(flow) + ' L/sec', True, WHITE, BLACK)
  textRect = text.get_rect()
  windowSurface.blit(text, (40,5*LINEHEIGHT))

  # Draw Liters Poured
  text = basicFont.render('Pints Poured: '+str(pintsPoured) + ' pints', True, WHITE, BLACK)
  textRect = text.get_rect()
  windowSurface.blit(text, (40,6*LINEHEIGHT))
  
  # Draw Pouring
  text = basicFont.render('Pouring: '+str(pouring), True, WHITE, BLACK)
  textRect = text.get_rect()
  windowSurface.blit(text, (40,7*LINEHEIGHT))

  # Draw Pour Start
  text = basicFont.render('Last Pour Started At: '+time.strftime('%H:%M:%S', time.localtime(pourStart/1000)), True, WHITE, BLACK)
  textRect = text.get_rect()
  windowSurface.blit(text, (40,8*LINEHEIGHT))
  
  # Draw Tweet
  text = basicFont.render('Tweet: '+str(tweet), True, WHITE, BLACK)
  textRect = text.get_rect()
  windowSurface.blit(text, (40,9*LINEHEIGHT))

  # Display everything
  pygame.display.flip()

while True:
	currentTime = int(time.time() * 1000)
	if GPIO.input(17):
		pinState = True
	else:
		pinState = False

	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
			pygame.quit()
			sys.exit()

# If we have changed pin states low to high...
	if(pinState != lastPinState and pinState == True):
		if(pouring == False):
			pourStart = currentTime
		pouring = True
		# get the current time
		pinChange = currentTime
		pinDelta = pinChange - lastPinChange
		if (pinDelta < 1000):
			# calculate the instantaneous speed
			hertz = 1000.0000 / pinDelta
			flow = hertz / (60 * 7.5) # L/s
			litersPoured += flow * (pinDelta / 1000.0000)
			pintsPoured = litersPoured * 2.11338

	renderThings(lastPinChange, pinChange, pinDelta, hertz, flow, pintsPoured, pouring, pourStart, tweet, windowSurface, basicFont)
	lastPinChange = pinChange
	lastPinState = pinState


