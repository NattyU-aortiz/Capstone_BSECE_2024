#testing interupt

#demodec18_1.py

import time
import RPi.GPIO as GPIO
from time import sleep, strftime 
from PCF8574 import PCF8574_GPIO 
from Adafruit_LCD1602 import Adafruit_CharLCD 
from datetime import datetime 


# GPIO Pin Assignments 
LED_ALERT_PIN = 4    # GPIO pin connected to an LED/autofill soleinoid
SOIL_SENSOR_PIN = 17  # GPIO pin connected to the soil moisture sensor
WATER_LEVEL_PIN = 27  # GPIO pin connected to the water level sensor
BUTTON_SELECT_PIN = 22 # GPIO pin connected to button to select plants
SOLINOID_3_PIN = 5  # channel 3 #1 - GPIO pin connected to the soleinoid for soil moisture sensor 3
SOIL_SENSOR_PIN2 = 6  # GPIO pin connected to the soil moisture sensor 2
SOLINOID_1_PIN = 13  # channel 1 #1 - GPIO pin connected to the soleinoid for soil moisture sensor 1
SOLINOID_2_PIN = 19  # channel 2 #1 - GPIO pin connected to the soleinoid for soil moisture sensor 2
SOLINOID_3_PIN_A = 26 # channel 3 #2 - GPIO pin connected to the soleinoid for soil moisture sensor 3
#2nd bank
SOIL_SENSOR_PIN4 = 18  # GPIO pin connected to the soil moisture sensor 4
SOLINOID_4_PIN = 23 # channel 4 #1 - GPIO pin connected to the soleinoid for soil moisture sensor 4
SOLINOID_4_PIN_A = 24  # channel 4 #2 - GPIO pin connected to the soleinoid for soil moisture sensor 4
SOLINOID_2_PIN_A = 25  # channel 2 #2 - GPIO pin connected to the soleinoid for soil moisture sensor 2
SOLINOID_1_PIN_A = 12 # channel 1 #2 - GPIO pin connected to the soleinoid for soil moisture sensor 1
SOIL_SENSOR_PIN3 = 16  # GPIO pin connected to the soil moisture sensor 3
#LAST BLANK GPIO 20
WATER_PUMP_PIN = 21    # pump pin can use to power both moters with a npn maybe need gpio20


def setup(): #moved this to a global variable 
# Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SOIL_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) #added , pull_up_down=GPIO.PUD_UP also may need to fix logic here pullup/down ##
    GPIO.setup(SOIL_SENSOR_PIN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SOIL_SENSOR_PIN3, GPIO.IN, pull_up_down=GPIO.PUD_UP) #added , pull_up_down=GPIO.PUD_UP also may need to fix logic here pullup/down ##
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
    
def handle_water_level_pin(channel):
    while True: 
        if GPIO.input(WATER_LEVEL_PIN) == GPIO.LOW: 
            GPIO.output(LED_ALERT_PIN, GPIO.HIGH)  # Turn on alert
            display_message("Reservoir level: \n   REFILL!   \n ", lcd_line=0)
            sleep(5)
            continue
        else:
            GPIO.output(LED_ALERT_PIN, GPIO.LOW)  # Turn off alert
            display_message("Reservoir level: \n      OK     \n", lcd_line=0)
            sleep(5)
            break
            
            
def display_message(message, lcd_line=0):
    """
    Outputs messages to both the terminal and the LCD.

    Parameters:
    - message: The message to display.
    - lcd_line: The line number on the LCD (0 for the first line, 1 for the second line).
    """
    print(message)
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
    lcd.clear()  # Clear the LCD before displaying a new message blocked out on 17_2_1
    lcd.setCursor(0, lcd_line)
    lcd.message(message)
    
    
def check_soil_pin():
    while True:
        if GPIO.input(SOIL_SENSOR_PIN) == GPIO.HIGH:
            display_message("SOIL MOISTURE 1 \n     TOO LOW   \n ", lcd_line=0)
            sleep(5)
            destroy()
            GPIO.output(WATER_PUMP_PIN, GPIO.HIGH)
            display_message("      PUMP      \n   ACTIVATED    \n", lcd_line=0)
            sleep(2)
            destroy()
            GPIO.output(SOLINOID_1_PIN, GPIO.HIGH)
            GPIO.output(SOLINOID_1_PIN_A, GPIO.LOW)
            sleep(plant1_watering_time)
            sleep(1)
            display_message("      CYCLE    \n   COMPLETED   \n ", lcd_line=0)
            sleep(2)
            destroy()
            GPIO.output(WATER_PUMP_PIN, GPIO.LOW) # Turn off pump V5
            GPIO.output(SOLINOID_1_PIN, GPIO.LOW)
            GPIO.output(SOLINOID_1_PIN_A, GPIO.HIGH)
            sleep(5)
            
            if GPIO.input(SOIL_SENSOR_PIN) == GPIO.LOW:
                GPIO.output(WATER_PUMP_PIN, GPIO.LOW) # Turn off pump V5
                GPIO.output(SOLINOID_1_PIN, GPIO.LOW)
                GPIO.output(SOLINOID_1_PIN_A, GPIO.HIGH)
                display_message("SOIL MOISTURE 1 \n      OK       \n ", lcd_line=0)
                sleep(5)
                destroy()
                break

        else:
            GPIO.output(WATER_PUMP_PIN, GPIO.LOW) # Turn off pump V5
            GPIO.output(SOLINOID_1_PIN, GPIO.LOW)
            GPIO.output(SOLINOID_1_PIN_A, GPIO.HIGH)
            display_message("SOIL MOISTURE 1 \n      OK       \n ", lcd_line=0)
            sleep(5)
            destroy()
            break
            
def check_soil_pin2():
    while True:
        if GPIO.input(SOIL_SENSOR_PIN2) == GPIO.HIGH:
            display_message("SOIL MOISTURE 2 \n     TOO LOW   \n ", lcd_line=0)
            sleep(5)
            destroy()
            GPIO.output(WATER_PUMP_PIN, GPIO.HIGH)
            display_message("      PUMP      \n   ACTIVATED    \n", lcd_line=0)
            sleep(2)
            destroy()
            GPIO.output(SOLINOID_2_PIN, GPIO.HIGH)
            GPIO.output(SOLINOID_2_PIN_A, GPIO.LOW)
            sleep(plant2_watering_time)
            sleep(1)
            display_message("      CYCLE    \n   COMPLETED   \n ", lcd_line=0)
            sleep(2)
            destroy()
            GPIO.output(WATER_PUMP_PIN, GPIO.LOW) # Turn off pump V5
            GPIO.output(SOLINOID_2_PIN, GPIO.LOW)
            GPIO.output(SOLINOID_2_PIN_A, GPIO.HIGH)
            sleep(5)
            
            if GPIO.input(SOIL_SENSOR_PIN2) == GPIO.LOW:
                GPIO.output(WATER_PUMP_PIN, GPIO.LOW) # Turn off pump V5
                GPIO.output(SOLINOID_2_PIN, GPIO.LOW)
                GPIO.output(SOLINOID_2_PIN_A, GPIO.HIGH)
                display_message("SOIL MOISTURE 2 \n      OK       \n ", lcd_line=0)
                sleep(5)
                destroy()
                break

        else:
            GPIO.output(WATER_PUMP_PIN, GPIO.LOW) # Turn off pump V5
            GPIO.output(SOLINOID_2_PIN, GPIO.LOW)
            GPIO.output(SOLINOID_2_PIN_A, GPIO.HIGH)
            display_message("SOIL MOISTURE 2 \n      OK       \n ", lcd_line=0)
            sleep(5)
            destroy()
            break
            
def check_soil_pin3():
    while True:
        if GPIO.input(SOIL_SENSOR_PIN3) == GPIO.HIGH:
            display_message("SOIL MOISTURE 3 \n     TOO LOW   \n ", lcd_line=0)
            sleep(5)
            destroy()
            GPIO.output(WATER_PUMP_PIN, GPIO.HIGH)
            display_message("      PUMP      \n   ACTIVATED    \n", lcd_line=0)
            sleep(2)
            destroy()
            GPIO.output(SOLINOID_3_PIN, GPIO.HIGH)
            GPIO.output(SOLINOID_3_PIN_A, GPIO.LOW)
            sleep(plant3_watering_time)
            sleep(1)
            display_message("      CYCLE    \n   COMPLETED   \n ", lcd_line=0)
            sleep(2)
            destroy()
            GPIO.output(WATER_PUMP_PIN, GPIO.LOW) # Turn off pump V5
            GPIO.output(SOLINOID_3_PIN, GPIO.LOW)
            GPIO.output(SOLINOID_3_PIN_A, GPIO.HIGH)
            sleep(5)
            
            if GPIO.input(SOIL_SENSOR_PIN3) == GPIO.LOW:
                GPIO.output(WATER_PUMP_PIN, GPIO.LOW) # Turn off pump V5
                GPIO.output(SOLINOID_3_PIN, GPIO.LOW)
                GPIO.output(SOLINOID_3_PIN_A, GPIO.HIGH)
                display_message("SOIL MOISTURE 3 \n      OK       \n ", lcd_line=0)
                sleep(5)
                destroy()
                break

        else:
            GPIO.output(WATER_PUMP_PIN, GPIO.LOW) # Turn off pump V5
            GPIO.output(SOLINOID_3_PIN, GPIO.LOW)
            GPIO.output(SOLINOID_3_PIN_A, GPIO.HIGH)
            display_message("SOIL MOISTURE 3 \n      OK       \n ", lcd_line=0)
            sleep(5)
            destroy()
            break
            
            
def check_soil_pin4():
    while True:
        if GPIO.input(SOIL_SENSOR_PIN4) == GPIO.HIGH:
            display_message("SOIL MOISTURE 4 \n     TOO LOW   \n ", lcd_line=0)
            sleep(5)
            destroy()
            GPIO.output(WATER_PUMP_PIN, GPIO.HIGH)
            display_message("      PUMP      \n   ACTIVATED    \n", lcd_line=0)
            sleep(2)
            destroy()
            GPIO.output(SOLINOID_4_PIN, GPIO.HIGH)
            GPIO.output(SOLINOID_4_PIN_A, GPIO.LOW)
            sleep(plant4_watering_time)
            sleep(1)
            display_message("      CYCLE    \n   COMPLETED   \n ", lcd_line=0)
            sleep(2)
            destroy()
            GPIO.output(WATER_PUMP_PIN, GPIO.LOW) # Turn off pump V5
            GPIO.output(SOLINOID_4_PIN, GPIO.LOW)
            GPIO.output(SOLINOID_4_PIN_A, GPIO.HIGH)
            sleep(5)
            
            if GPIO.input(SOIL_SENSOR_PIN4) == GPIO.LOW:
                GPIO.output(WATER_PUMP_PIN, GPIO.LOW) # Turn off pump V5
                GPIO.output(SOLINOID_4_PIN, GPIO.LOW)
                GPIO.output(SOLINOID_4_PIN_A, GPIO.HIGH)
                display_message("SOIL MOISTURE 4 \n      OK       \n ", lcd_line=0)
                sleep(5)
                destroy()
                break

        else:
            GPIO.output(WATER_PUMP_PIN, GPIO.LOW) # Turn off pump V5
            GPIO.output(SOLINOID_4_PIN, GPIO.LOW)
            GPIO.output(SOLINOID_4_PIN_A, GPIO.HIGH)
            display_message("SOIL MOISTURE 4 \n      OK       \n ", lcd_line=0)
            sleep(5)
            destroy()
            break






def calculate_water_duration(size, climate):
    water_duration = size * climate
    return water_duration    

def destroy():
    lcd.clear()
    mcp.output(3,0)
    
PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)




# Constants for button interaction timing
SHORT_PRESS_DURATION = 1  # seconds
LONG_PRESS_DURATION = 3  # seconds

def handle_button_input_numofplants():
    """
    Handles user input using a push button for num of plats.
    - Short press (< 3 seconds): Cycles through options (e.g., climates and sizes).
    - Long press (>= 3 seconds): Selects the current option.
    """

    numofplants = {1: "1", 2: "2", 3: "3", 4: "4"}
    current_numofplants = 4

    print("Waiting for user button input...\n")
    display_message("Press button to\nselect options\n", lcd_line=0)

    # Wait for numofplants selection
    display_message("Select number\n    of plants   \n", lcd_line=0)
    while True:
        if GPIO.input(BUTTON_SELECT_PIN) == GPIO.LOW:  # Button pressed
            press_start_time = time.time()

            # Wait for button release
            while GPIO.input(BUTTON_SELECT_PIN) == GPIO.LOW:
                pass
            press_duration = time.time() - press_start_time

            if press_duration < SHORT_PRESS_DURATION:
                # Cycle through sizes
                current_numofplants = (current_numofplants % 4) + 1
                display_message(f"Number of Plants:\n{numofplants[current_numofplants]}\n", lcd_line=0)
                sleep(1)
            elif press_duration < LONG_PRESS_DURATION:
                # Select Size
                selected_numofplants = current_numofplants
                display_message(f"Selected number:\n{numofplants[selected_numofplants]}\n", lcd_line=0)
                #print(f"Selected Size: {sizes[selected_size]}\n")
                sleep(2)
                break
    return {
        "numofplants": selected_numofplants
        }


# Button-based User Interaction  DamienDec15_2 needs to delete the numofplants variable!!!!!!!!!!!!!!
def handle_button_input():
    """
    Handles user input using a push button.
    - Short press (< 3 seconds): Cycles through options (e.g., climates and sizes).
    - Long press (>= 3 seconds): Selects the current option.
    """
    climates = {1: "arid", 2: "temperate", 3: "tropical"}
    sizes = {1: "small", 2: "medium", 3: "large"}
    current_climate = 3
    current_size = 3

    print("Waiting for user button input...\n")
    display_message("Press button to\nselect options\n", lcd_line=0)

    # Wait for user interactions
    while True:
        if GPIO.input(BUTTON_SELECT_PIN) == GPIO.LOW:  # Button pressed
            press_start_time = time.time()

            # Wait for button release to measure the press duration
            while GPIO.input(BUTTON_SELECT_PIN) == GPIO.LOW:
                pass
            press_duration = time.time() - press_start_time

            if press_duration < SHORT_PRESS_DURATION:
                # Cycle through options
                current_climate = (current_climate % 3) + 1
                display_message(f"Climate Option:\n{climates[current_climate]}\n", lcd_line=0)
                sleep(1)
            elif press_duration < LONG_PRESS_DURATION:
                # Select Climate
                selected_climate = current_climate
                display_message(f"Selected Climate:\n{climates[selected_climate]}\n", lcd_line=0)
                #print(f"Selected Climate: {climates[selected_climate]}\n")
                sleep(2)
                break

    # Wait for size selection
    display_message("Select Planter\n     Size      \n", lcd_line=0)
    while True:
        if GPIO.input(BUTTON_SELECT_PIN) == GPIO.LOW:  # Button pressed
            press_start_time = time.time()

            # Wait for button release
            while GPIO.input(BUTTON_SELECT_PIN) == GPIO.LOW:
                pass
            press_duration = time.time() - press_start_time

            if press_duration < SHORT_PRESS_DURATION:
                # Cycle through sizes
                current_size = (current_size % 3) + 1
                display_message(f"Planter Size:\n{sizes[current_size]}\n", lcd_line=0)
                sleep(1)
            elif press_duration < LONG_PRESS_DURATION:
                # Select Size
                selected_size = current_size
                display_message(f"Selected Size:\n{sizes[selected_size]}\n", lcd_line=0)
                #print(f"Selected Size: {sizes[selected_size]}\n")
                sleep(2)
                break
                


    return {
        "climate": selected_climate,
        "size": selected_size,
    }
    
    


def poll_soil_sensor_1():
    if GPIO.input(SOIL_SENSOR_PIN):
        display_message("SOIL MOISTURE 1 \n     TOO LOW   \n", lcd_line=0)
        sleep(2)
        mcp.output(3,0)
        sleep(.5)
        lcd.clear()
        sleep(.5)
        water_plant_1()
        sleep(2)
    else:
        display_message("SOIL MOISTURE 1 \n      OK       \n ", lcd_line=0)
        sleep(2)
        mcp.output(3,0)
        sleep(.5)
        lcd.clear()
        sleep(1)

def poll_soil_sensor_2():
    if GPIO.input(SOIL_SENSOR_PIN2):
        display_message("SOIL MOISTURE 2 \n     TOO LOW   \n", lcd_line=0)
        sleep(2)
        mcp.output(3,0)
        sleep(.5)
        lcd.clear()
        sleep(.5)
        water_plant_2()
        sleep(2)
    else:
        display_message("SOIL MOISTURE 2 \n      OK       \n ", lcd_line=0)
        sleep(2)
        mcp.output(3,0)
        sleep(.5)
        lcd.clear()
        sleep(1)

def poll_soil_sensor_3():
    if GPIO.input(SOIL_SENSOR_PIN3):
        display_message("SOIL MOISTURE 3 \n     TOO LOW   \n", lcd_line=0)
        sleep(2)
        mcp.output(3,0)
        sleep(.5)
        lcd.clear()
        sleep(.5)
        water_plant_3()
        sleep(2)
    else:
        display_message("SOIL MOISTURE 3 \n      OK       \n ", lcd_line=0)
        sleep(2)
        mcp.output(3,0)
        sleep(.5)
        lcd.clear()
        sleep(1)

def poll_soil_sensor_4():
    if GPIO.input(SOIL_SENSOR_PIN4):
        display_message("SOIL MOISTURE 4 \n     TOO LOW   \n", lcd_line=0)
        mcp.output(3,0)
        sleep(.5)
        lcd.clear()
        sleep(.5)
        water_plant_4()
        sleep(2)
    else:
        display_message("SOIL MOISTURE 4 \n      OK       \n ", lcd_line=0)
        sleep(2)
        mcp.output(3,0)
        sleep(.5)
        lcd.clear()
        sleep(1)
        
    
# Watering Functions
def water_plant_1():
    GPIO.output(WATER_PUMP_PIN, GPIO.HIGH)
    GPIO.output(SOLINOID_1_PIN, GPIO.HIGH)
    GPIO.output(SOLINOID_1_PIN_A, GPIO.LOW)
    sleep(plant1_watering_time)
    GPIO.output(WATER_PUMP_PIN, GPIO.LOW)
    GPIO.output(SOLINOID_1_PIN, GPIO.LOW)
    GPIO.output(SOLINOID_1_PIN_A, GPIO.HIGH)
    display_message("Plant 1 Watered\n      OK       \n", lcd_line=0)
    sleep(2)
    mcp.output(3,0)
    sleep(.5)
    lcd.clear()
    sleep(1)

def water_plant_2():
    GPIO.output(WATER_PUMP_PIN, GPIO.HIGH)
    GPIO.output(SOLINOID_2_PIN, GPIO.HIGH)
    GPIO.output(SOLINOID_2_PIN_A, GPIO.LOW)
    sleep(plant2_watering_time)
    GPIO.output(WATER_PUMP_PIN, GPIO.LOW)
    GPIO.output(SOLINOID_2_PIN, GPIO.LOW)
    GPIO.output(SOLINOID_2_PIN_A, GPIO.HIGH)
    display_message("Plant 2 Watered\n      OK       \n", lcd_line=0)
    sleep(2)
    mcp.output(3,0)
    sleep(.5)
    lcd.clear()
    sleep(1)
        
        
        
def water_plant_3():
    GPIO.output(WATER_PUMP_PIN, GPIO.HIGH)
    GPIO.output(SOLINOID_3_PIN, GPIO.HIGH)
    GPIO.output(SOLINOID_3_PIN_A, GPIO.LOW)
    sleep(plant3_watering_time)
    GPIO.output(WATER_PUMP_PIN, GPIO.LOW)
    GPIO.output(SOLINOID_3_PIN, GPIO.LOW)
    GPIO.output(SOLINOID_3_PIN_A, GPIO.HIGH)
    display_message("Plant 3 Watered\n      OK       \n", lcd_line=0)
    sleep(2)
    mcp.output(3,0)
    sleep(.5)
    lcd.clear()
    sleep(1)

def water_plant_4():
    GPIO.output(WATER_PUMP_PIN, GPIO.HIGH)
    GPIO.output(SOLINOID_4_PIN, GPIO.HIGH)
    GPIO.output(SOLINOID_4_PIN_A, GPIO.LOW)
    sleep(plant4_watering_time)
    GPIO.output(WATER_PUMP_PIN, GPIO.LOW)
    GPIO.output(SOLINOID_4_PIN, GPIO.LOW)
    GPIO.output(SOLINOID_4_PIN_A, GPIO.HIGH)
    display_message("Plant 4 Watered\n      OK       \n", lcd_line=0)
    sleep(2)
    mcp.output(3,0)
    sleep(.5)
    lcd.clear()
    sleep(1)
    

if __name__ == "__main__":
    try:
        display_message("System Starting...\n", lcd_line=0)
        setup()
        sleep(2)
        numofplants = handle_button_input_numofplants()
        # Configure Plant 1
        display_message("Configure Plant\n    1          ", lcd_line=0)
        sleep(2)
        plant1_config = handle_button_input()
        plant1_climate = plant1_config["climate"]
        plant1_size = plant1_config["size"]
        plant1_watering_time = calculate_water_duration(plant1_size, plant1_climate)
        
        #added for dec17th
        if plant1_watering_time == 9:
            plant1_watering_time = 15
        elif plant1_watering_time == 6:
            plant1_watering_time = 13
        elif plant1_watering_time == 3 or plant1_watering_time == 4:
            plant1_watering_time = 10
        elif plant1_watering_time == 2:
            plant1_watering_time = 7
        elif plant1_watering_time == 1:
            plant1_watering_time = 5
        
        display_message(f"Plant 1: {plant1_watering_time}\nsec", lcd_line=0)
        sleep(2)

        # Configure Plant 2
        display_message("Configure Plant\n    2          ", lcd_line=0)
        sleep(2)
        plant2_config = handle_button_input()
        plant2_climate = plant2_config["climate"]
        plant2_size = plant2_config["size"]
        plant2_watering_time = calculate_water_duration(plant2_size, plant2_climate)
        if plant2_watering_time == 9:
            plant2_watering_time = 15
        elif plant2_watering_time == 6:
            plant2_watering_time = 13
        elif plant2_watering_time == 3 or plant2_watering_time == 4:
            plant2_watering_time = 10
        elif plant2_watering_time == 2:
            plant2_watering_time = 7
        elif plant2_watering_time == 1:
            plant2_watering_time = 5
        
        display_message(f"Plant 2: {plant2_watering_time}\nsec", lcd_line=0)
        sleep(2)
        
        # Configure Plant 3
        display_message("Configure Plant\n    3          ", lcd_line=0)
        sleep(2)
        plant3_config = handle_button_input()
        plant3_climate = plant3_config["climate"]
        plant3_size = plant3_config["size"]
        plant3_watering_time = calculate_water_duration(plant3_size, plant3_climate)
        if plant3_watering_time == 9:
            plant3_watering_time = 15
        elif plant3_watering_time == 6:
            plant3_watering_time = 13
        elif plant3_watering_time == 3 or plant3_watering_time == 4:
            plant3_watering_time = 10
        elif plant3_watering_time == 2:
            plant3_watering_time = 7
        elif plant3_watering_time == 1:
            plant3_watering_time = 5
        
        display_message(f"Plant 3: {plant3_watering_time}\nsec", lcd_line=0)
        sleep(2)

        # Configure Plant 4
        display_message("Configure Plant\n    4          ", lcd_line=0)
        sleep(2)
        plant4_config = handle_button_input()
        plant4_climate = plant4_config["climate"]
        plant4_size = plant4_config["size"]
        plant4_watering_time = calculate_water_duration(plant4_size, plant4_climate)
        
        if plant4_watering_time == 9:
            plant4_watering_time = 15
        elif plant4_watering_time == 6:
            plant4_watering_time = 13
        elif plant4_watering_time == 3 or plant4_watering_time == 4:
            plant4_watering_time = 10
        elif plant4_watering_time == 2:
            plant4_watering_time = 7
        elif plant4_watering_time == 1:
            plant4_watering_time = 5
        display_message(f"Plant 4: {plant4_watering_time}\nsec", lcd_line=0)
        sleep(2)

        # Display configurations
        print(f"Plant 1: Climate-{plant1_climate}, Size-{plant1_size}, Watering-{plant1_watering_time}s")
        print(f"Plant 2: Climate-{plant2_climate}, Size-{plant2_size}, Watering-{plant2_watering_time}s")
        print(f"Plant 3: Climate-{plant3_climate}, Size-{plant3_size}, Watering-{plant3_watering_time}s")
        print(f"Plant 4: Climate-{plant3_climate}, Size-{plant4_size}, Watering-{plant4_watering_time}s")
        
        GPIO.add_event_detect(WATER_LEVEL_PIN, GPIO.BOTH, callback=handle_water_level_pin, bouncetime=200)
        
        while True:
            #check_soil_pin()
            # check_water_reservoir()
            #check_soil_pin2()
            # check_water_reservoir()
            #check_soil_pin3()
            # check_water_reservoir()
            #check_soil_pin4()
            
            
            
            poll_soil_sensor_1()
            poll_soil_sensor_2()
            poll_soil_sensor_3()
            poll_soil_sensor_4()
            sleep(15)
            
    except KeyboardInterrupt:
        print("Shutting down the system...")
        mcp.output(3,0)
        sleep(.5)
        lcd.clear()
        sleep(.5)
        GPIO.cleanup ()
    finally:
        mcp.output(3,0)
        sleep(.5)
        lcd.clear()
        sleep(.5)
        GPIO.cleanup ()
    
