import RPi.GPIO as GPIO
import time, os, statistics, sys

GPIO_TRIGGER = 18
GPIO_ECHO = 24

THRESHOLD = 80 # cm
TIMEOUT = 20 # sec

############################
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

LAST_MOVE = time.time()

SCREEN_STATE = 1

TIMER_STARTED = 0

    TIMER = sys.argv[1];
else:
    TIMER = 1;

def distance(sample_size=5, sample_wait=0.01):
    # https://raw.githubusercontent.com/alaudet/hcsr04sensor/master/hcsr04sensor/sensor.py
    speed_of_sound = 331.3
    sample = []
    for distance_reading in range(sample_size):
        GPIO.output(GPIO_TRIGGER, GPIO.LOW)
        time.sleep(sample_wait)
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        echo_status_counter = 1
        sonar_signal_on, sonar_signal_off = time.time()+1, time.time()
        while GPIO.input(GPIO_ECHO) == 0 and echo_status_counter < 1000:
            sonar_signal_off = time.time()
            echo_status_counter += 1
        while GPIO.input(GPIO_ECHO) == 1:
            sonar_signal_on = time.time()
        time_passed = sonar_signal_on - sonar_signal_off
        distance_cm = time_passed * ((speed_of_sound * 100) / 2)
        sample.append(distance_cm)
    return statistics.median(sample)

def doCheck():
    global LAST_MOVE, SCREEN_STATE, TIMER_STARTED
    d = distance()
    now = time.time()
    last_move_diff = now - LAST_MOVE
    if d <= THRESHOLD:
        if SCREEN_STATE == 0 and TIMER_STARTED == 0:
            os.system("echo 0 > /sys/class/backlight/rpi_backlight/bl_power") # on
            print(time.strftime('%Y-%m-%d %H:%M:%S'),
                  'Screen on                       ')
        print(time.strftime('%Y-%m-%d %H:%M:%S'), 
              "Object in" , round(d, 2),
              'cm detected          ', end="\r")
        SCREEN_STATE = 1
        TIMER_STARTED = 1
        LAST_MOVE = now
    else:
        if last_move_diff >= TIMEOUT and SCREEN_STATE == 1:
            os.system("echo 1 > /sys/class/backlight/rpi_backlight/bl_power") # off
            print(time.strftime('%Y-%m-%d %H:%M:%S'),
                  'Screen off                     ')
            SCREEN_STATE = 0
            TIMER_STARTED = 0
        elif last_move_diff < TIMEOUT and SCREEN_STATE == 1:
            remain = round(TIMEOUT - last_move_diff)
            message = time.strftime('%Y-%m-%d %H:%M:%S') + ' Screen off in %s seconds   '
            print(message % (remain), end="\r")

os.system("echo 0 > /sys/class/backlight/rpi_backlight/bl_power") # on
try:
    print(time.strftime('%Y-%m-%d %H:%M:%S'), 'Start displaystandby.py')
    while True:
        doCheck()
        time.sleep(TIMER)
except KeyboardInterrupt:
    print(time.strftime('%Y-%m-%d %H:%M:%S'), 'End displaystandby.py')

GPIO.cleanup()
os.system("echo 0 > /sys/class/backlight/rpi_backlight/bl_power") # on
 
