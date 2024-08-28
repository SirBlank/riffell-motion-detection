import digitalio # 0.55

'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'D4', 'D5', 'D6', 'D7'

def init(pins):
    for pin in pins:
        GPIO = digitalio.DigitalInOut(pin)
        GPIO.direction = digitalio.Direction.OUTPUT
        GPIO.value = False
    
    
def LED_on (pin):
    GPIO = digitalio.DigitalInOut(pin)
    GPIO.direction = digitalio.Direction.OUTPUT
    GPIO.value = True 

def LED_off (pin):
    GPIO = digitalio.DigitalInOut(pin)
    GPIO.direction = digitalio.Direction.OUTPUT
    GPIO.value = False 



