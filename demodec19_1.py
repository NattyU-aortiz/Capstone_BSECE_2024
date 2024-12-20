#demodec19_1.py   created at 1 PM dec 19
#cleaned up and slimmed down



# Import necessary libraries
import time
import RPi.GPIO as GPIO
from time import sleep
from PCF8574 import PCF8574_GPIO 
from Adafruit_LCD1602 import Adafruit_CharLCD 
from datetime import datetime 

# GPIO Pin Assignments 
LED_ALERT_PIN = 4    
SOIL_SENSOR_PIN = 17  
WATER_LEVEL_PIN = 27  
BUTTON_SELECT_PIN = 22 
SOLINOID_3_PIN = 5  
SOIL_SENSOR_PIN2 = 6  
SOLINOID_1_PIN = 13  
SOLINOID_2_PIN = 19  
SOLINOID_3_PIN_A = 26 
SOIL_SENSOR_PIN4 = 18  
SOLINOID_4_PIN = 23 
SOLINOID_4_PIN_A = 24  
SOLINOID_2_PIN_A = 25  
SOLINOID_1_PIN_A = 12 
SOIL_SENSOR_PIN3 = 16  
WATER_PUMP_PIN = 21    

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SOIL_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SOIL_SENSOR_PIN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SOIL_SENSOR_PIN3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SOIL_SENSOR_PIN4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(WATER_LEVEL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.setup(WATER_PUMP_PIN, GPIO.OUT)
    GPIO.setup(LED_ALERT_PIN, GPIO.OUT) 
    GPIO.setup(SOLINOID_1_PIN, GPIO.OUT)
    GPIO.setup(SOLINOID_1_PIN_A, GPIO.OUT)
    GPIO.setup(SOLINOID_2_PIN, GPIO.OUT)
    GPIO.setup(SOLINOID_2_PIN_A, GPIO.OUT)
    GPIO.setup(SOLINOID_3_PIN, GPIO.OUT)
    GPIO.setup(SOLINOID_3_PIN_A, GPIO.OUT)
    GPIO.setup(SOLINOID_4_PIN, GPIO.OUT)
    GPIO.setup(SOLINOID_4_PIN_A, GPIO.OUT)
    GPIO.output(LED_ALERT_PIN, GPIO.LOW)
    GPIO.output(WATER_PUMP_PIN, GPIO.LOW)
    GPIO.output(SOLINOID_1_PIN, GPIO.LOW)
    GPIO.output(SOLINOID_1_PIN_A, GPIO.HIGH)
    GPIO.output(SOLINOID_2_PIN, GPIO.LOW)
    GPIO.output(SOLINOID_2_PIN_A, GPIO.HIGH)
    GPIO.output(SOLINOID_3_PIN, GPIO.LOW)
    GPIO.output(SOLINOID_3_PIN_A, GPIO.HIGH)
    GPIO.output(SOLINOID_4_PIN, GPIO.LOW)
    GPIO.output(SOLINOID_4_PIN_A, GPIO.HIGH)
    GPIO.setup(BUTTON_SELECT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
halt_flag = False

def handle_water_level_pin(channel):
    global halt_flag
    if GPIO.input(WATER_LEVEL_PIN) == GPIO.LOW: 
        GPIO.output(LED_ALERT_PIN, GPIO.HIGH)
        display_message("Reservoir level: \n   REFILL!   \n ", lcd_line=0)
        halt_flag = True
    else:
        GPIO.output(LED_ALERT_PIN, GPIO.LOW)
        display_message("Reservoir level: \n      OK     \n", lcd_line=0)
        halt_flag = False

def display_message(message, lcd_line=0):
    print(message)
    mcp.output(3,1)
    lcd.begin(16,2)
    lcd.clear()
    lcd.setCursor(0, lcd_line)
    lcd.message(message)

def calculate_water_duration(size, climate):
    water_duration = size * climate
    return water_duration    

def destroy():
    lcd.clear()
    mcp.output(3,0)
    
PCF8574_address = 0x27
PCF8574A_address = 0x3F
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

SHORT_PRESS_DURATION = 1
LONG_PRESS_DURATION = 3

def handle_button_input_numofplants():
    numofplants = {1: "1", 2: "2", 3: "3", 4: "4"}
    current_numofplants = 4

    print("Waiting for user button input...\n")
    display_message("Press button to\nselect options\n", lcd_line=0)

    display_message("Select number\n    of plants   \n", lcd_line=0)
    while True:
        if GPIO.input(BUTTON_SELECT_PIN) == GPIO.LOW:
            press_start_time = time.time()
            while GPIO.input(BUTTON_SELECT_PIN) == GPIO.LOW:
                pass
            press_duration = time.time() - press_start_time

            if press_duration < SHORT_PRESS_DURATION:
                current_numofplants = (current_numofplants % 4) + 1
                display_message(f"Number of Plants:\n{numofplants[current_numofplants]}\n", lcd_line=0)
                sleep(1)
            elif press_duration < LONG_PRESS_DURATION:
                selected_numofplants = current_numofplants
                display_message(f"Selected number:\n{numofplants[selected_numofplants]}\n", lcd_line=0)
                sleep(2)
                break
    return {"numofplants": selected_numofplants}

def handle_button_input():
    climates = {1: "arid", 2: "temperate", 3: "tropical"}
    sizes = {1: "small", 2: "medium", 3: "large"}
    current_climate = 3
    current_size = 3

    print("Waiting for user button input...\n")
    display_message("Press button to\nselect options\n", lcd_line=0)

    while True:
        if GPIO.input(BUTTON_SELECT_PIN) == GPIO.LOW:
            press_start_time = time.time()
            while GPIO.input(BUTTON_SELECT_PIN) == GPIO.LOW:
                pass
            press_duration = time.time() - press_start_time

            if press_duration < SHORT_PRESS_DURATION:
                current_climate = (current_climate % 3) + 1
                display_message(f"Climate Option:\n{climates[current_climate]}\n", lcd_line=0)
                sleep(1)
            elif press_duration < LONG_PRESS_DURATION:
                selected_climate = current_climate
                display_message(f"Selected Climate:\n{climates[selected_climate]}\n", lcd_line=0)
                sleep(2)
                break

    display_message("Select Planter\n     Size      \n", lcd_line=0)
    while True:
        if GPIO.input(BUTTON_SELECT_PIN) == GPIO.LOW:
            press_start_time = time.time()
            while GPIO.input(BUTTON_SELECT_PIN) == GPIO.LOW:
                pass
            press_duration = time.time() - press_start_time

            if press_duration < SHORT_PRESS_DURATION:
                current_size = (current_size % 3) + 1
                display_message(f"Planter Size:\n{sizes[current_size]}\n", lcd_line=0)
                sleep(1)
            elif press_duration < LONG_PRESS_DURATION:
                selected_size = current_size
                display_message(f"Selected Size:\n{sizes[selected_size]}\n", lcd_line=0)
                sleep(2)
                break
    return {
        "climate": selected_climate,
        "size": selected_size,
    }

def poll_soil_sensor(sensor_pin, plant_number, watering_time, water_plant_func):
    if GPIO.input(sensor_pin):
        display_message(f"SOIL MOISTURE {plant_number} \n     TOO LOW   \n", lcd_line=0)
        sleep(2)
        mcp.output(3, 0)
        sleep(.5)
        lcd.clear()
        sleep(.5)
        water_plant_func()
        sleep(2)
    else:
        display_message(f"SOIL MOISTURE {plant_number} \n      OK       \n", lcd_line=0)
        sleep(2)
        mcp.output(3, 0)
        sleep(.5)
        lcd.clear()
        sleep(1)

def water_plant(gpio_pins, watering_time):
    GPIO.output(WATER_PUMP_PIN, GPIO.HIGH)
    for pin in gpio_pins:
        GPIO.output(pin, GPIO.HIGH if pin != gpio_pins[-1] else GPIO.LOW)
    sleep(watering_time)
    GPIO.output(WATER_PUMP_PIN, GPIO.LOW)
    for pin in gpio_pins:
        GPIO.output(pin, GPIO.LOW if pin != gpio_pins[-1] else GPIO.HIGH)
    display_message("Plant Watered\n      OK       \n", lcd_line=0)
    sleep(2)
    mcp.output(3, 0)
    sleep(.5)
    lcd.clear()
    sleep(1)

if __name__ == "__main__":
    try:
        display_message("System Starting...\n", lcd_line=0)
        setup()
        sleep(2)
        numofplants = handle_button_input_numofplants()
        plant_configs = []

        for i in range(1, numofplants["numofplants"] + 1):
            display_message(f"Configure Plant\n    {i}          ", lcd_line=0)
            sleep(2)
            plant_config = handle_button_input()
            plant_climate = plant_config["climate"]
            plant_size = plant_config["size"]
            watering_time = calculate_water_duration(plant_size, plant_climate)
            if watering_time == 9:
                watering_time = 15
            elif watering_time == 6:
                watering_time = 13
            elif watering_time == 3 or watering_time == 4:
                watering_time = 10
            elif watering_time == 2:
                watering_time = 7
            elif watering_time == 1:
                watering_time = 5
            display_message(f"Plant {i}: {watering_time}\nsec", lcd_line=0)
            sleep(2)
            plant_configs.append((plant_climate, plant_size, watering_time))

        GPIO.add_event_detect(WATER_LEVEL_PIN, GPIO.BOTH, callback=handle_water_level_pin, bouncetime=200)

        while True:
            while halt_flag:
                sleep(1)

            for i, (climate, size, watering_time) in enumerate(plant_configs, start=1):
                poll_soil_sensor(eval(f"SOIL_SENSOR_PIN{i}"), i, watering_time, eval(f"water_plant_{i}"))
                sleep(1)
            sleep(15)
            
    except KeyboardInterrupt:
        print("Shutting down the system...")
        mcp.output(3,0)
        sleep(.5)
        lcd.clear()
        sleep(.5)
        GPIO.cleanup()
    finally:
        mcp.output(3,0)
        sleep(.5)
        lcd.clear()
        sleep(.5)
        GPIO.cleanup()