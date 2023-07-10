import time
import random
import board
import neopixel
import digitalio

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
pixel_pin = board.GP1
#pixel_pin = board.GP23 #uncomment when testing onboard led

#other Pins
modePin = digitalio.DigitalInOut(board.GP2)
modePin.switch_to_input(pull=digitalio.Pull.DOWN)

brightPin = digitalio.DigitalInOut(board.GP3)
brightPin.switch_to_input(pull=digitalio.Pull.DOWN)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# The number of NeoPixels
num_pixels = 11

#var
mode = 0
numOfModes = 5

brightnessBase = 1
brightness = 1

baseR = 240
baseG = 60
baseB = 0
r=0
g=0
b=0

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER
)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def candle():
    #for i in range(num_pixels):
    global brightness        
            
    change = (random.randint(-10,10)/500)  #amount of change that is allowed
    diffB = brightnessBase - brightness  #difference bettween current and targeted value
    deveation = diffB/100        #how strong the pull is back to targeted value
    brightness = brightness+change+deveation   #brightness is calculated
    brightness = min(brightness,brightnessBase)  #clamping
            
    r=round(baseR*brightness)
    g=round(baseG*brightness)
    b=baseB
    r= max(min(r,255),0)
    g= max(min(g,255),0)
    #if i == 1:
    print(r,g)
    #pixels[i] = r,g,b
    pixels.fill((r,g,b))
    pixels.show()
    
def algo():
    for i in range(num_pixels):
        global r
        global g
        global b
        global brightness
        change = round(3*brightnessBase) #steps ie how big steps are
        
        diffR = baseR-r
        randR= random.randint(-change,change)+(diffR/100) #how far steps are alowed to deveate from base
        r= max(round((r+randR)*brightnessBase),0)
        
        diffG = baseG-g
        randG = random.randint(-change,change)+(diffG/10)
        g= max(round((g+randG)*brightnessBase),0)
        print(r,g,b,brightnessBase)
        
        
        r= min(r,255)
        g= min(g,255)

        pixels[i] = r,g,b
    pixels.show()
    #print(r,g,b,brightnessBase)
    time.sleep(0.1)
    
while True:
    
    if modePin.value:
        mode += 1
        if mode > numOfModes:
            mode = 0
        print(mode)
        time.sleep(0.5)
    
    if brightPin.value:
        brightnessBase += 0.2
        if brightnessBase > 1:
            brightnessBase = 0.2
        print(brightnessBase)
        time.sleep(0.5)

    if mode == 0:
        candle()
        #algo()
    elif mode == 1: #white
        r = round(255 * brightnessBase)
        g = round(200 * brightnessBase)
        b = round(100 * brightnessBase)
        pixels.fill((r, g, b))
        pixels.show()
        
    elif mode == 2: #warm white
        r = round(255 * brightnessBase)
        g = round(130 * brightnessBase)
        b = round(20 * brightnessBase)
        pixels.fill((r, g, b))
        pixels.show()
        
    elif mode == 3:
        r = 255 * brightnessBase
        g = 130 * brightnessBase
        b = 20 * brightnessBase
        pixels.fill((r, g, b))
        pixels.show()
        
        
        
