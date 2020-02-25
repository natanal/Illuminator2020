from guizero import App, Text, PushButton, TextBox, Picture, Window
import RPi.GPIO as GPIO
import time

# The function for ultrasonic sensor working in a loop.
####### fix the switch timing issue in the while loop!!!!!######
GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 12
LIMIT = 13 
print ("Starting Measurements...")

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(LIMIT, GPIO.OUT)
GPIO.output(TRIG,0)


def take_distance():
        n = 1
        distance = 12
        app.hide()
        while distance > 10:
                print ("waiting for sensor to settle")

                time.sleep(2)
                GPIO.output(TRIG, 1)
                time.sleep(0.00001)
                GPIO.output(TRIG, 0)

                while GPIO.input(ECHO)==0:
                        pulse_start = time.time()

                while GPIO.input(ECHO)==1:
                        pulse_end = time.time()
                #calculating distance via pulses and converting
                #by 343m/s = distance/(time/2) where 'time' is
                #the time it takes for signal to travel there and back
                pulse_duration = pulse_end - pulse_start
                distance = pulse_duration*17150
                distance = round(distance, 2)

                print("This is the distance: ", distance)
                distancestring = str(distance)
                StatText = Text(ProcessWindow, text = distancestring, size=30, font = "Ariel", color="#86BC25", align = "left")
                #StatText = Text(GoingUpWindow, text = distancestring, size=30, font = "Ariel", color="#86BC25", align = "left")
                distance = pulse_duration*17150
                distance = round(distance, 2)
                app.update()
                StatText.destroy()
        ####some kind of light bulb turning####


        ###this is where movement of actuator down until limit is reached#####
        try:
                while not GPIO.input(13):
#                       print("low")
                        pass
        finally:
                if n == 1:
                        ProcessFinish()
                        n += 1
                else:
                        GoingUp()

"""try:
        while True:
                dist = take_distance()
                print ("Distance = ", dist)
                time.sleep(1)
except KeyboardInterrupt:
        print("Measurement stopped by user")
        GPIO.cleanup()
"""
def BulbPressed():
        #summon the next screen that says "In Process" and displays stat/pause button
        distance = 11
        ProcessWindow.show()
        take_distance()
#       app.update()
        app.hide()
def ProcessFinish():
        ProcessWindow.hide()
        SwitchBulbWindow.show()
#       app.update()
def SwitchBulb():
        SwitchBulbWindow.hide()
        GoingUpWindow.show()
        app.update()
        take_distance()
#       app.update()
def GoingUp():
        GoingUpWindow.hide()
        FinalWindow.show()
        app.update()
def FinalWindowCycle():
        #This will bring the app display back into the home screen
        FinalWindow.hide()
        app.show()
#       app.update()

        n = 1   # resetting if loop variable  to 1 for repetition
#       app.exit_full_screen()
def ExitScreen():
        app.exit_full_screen()
        ProcessWindow.exit_full_screen()
        SwitchBulbWindow.exit_full_screen()
        GoingUpWindow.exit_full_screen()
        FinalWindow.exit_full_screen()
        app.update()
app = App(title = "IlluminatorIntro", bg = "white") #Main app acreen

#App/Home screen characteristics
#WelcomeMessage = Text(app, text = "Welcome", size=40, font = "Ariel", color = "#00A3E0", align = "top")
#InstructionsMessage = Text(app, text = "Press Bulb to Start", size = 30, font = "Ariel", color = "#86BC25", align = "bottom")
#PushBulb = PushButton(app, image = "IlluminatorLogo.png", align = "top",command = BulbPressed)
#app.set_full_screen('Esc')

#Initial window that demonstrates bulb removal
ProcessWindow = Window(app, title="IlluminatorProcess", bg = "white")
RemoveBulbMessage = Text(ProcessWindow, text ="Removing Bulb", size=40, font = "Ariel", color = "#00A3E0", align = "top")
PauseButton = PushButton(ProcessWindow, text = "PAUSE", align = "right")
ProcessWindow.hide()
#ProcessWindow.after(5000, ProcessFinish)
ProcessWindow.set_full_screen('Esc')

# New Window for the user to switch out the bulb:
SwitchBulbWindow = Window(app, title="IlluminatorSwitch", bg ="white")
SwitchBulbText = Text(SwitchBulbWindow, text="Please Switch The Light Bulb With a New Bulb", size=40, font = "Ariel", color = "#00A3E0", align ="top")
ReadyButton = PushButton(SwitchBulbWindow, text = "READY")
SwitchBulbWindow.hide()
SwitchBulbButton = PushButton(SwitchBulbWindow, align = "top",command = SwitchBulb)
#SwitchBulbWindow.after(10000, SwitchBulb)
SwitchBulbWindow.set_full_screen('Esc')

#Window 3 for going back up
GoingUpWindow = Window(app, title ="IlluminatorUP", bg ="white")
ProvidingLightText = Text(GoingUpWindow, text="Providing Light...", size=40, font="Ariel", align="top")
GoingUpStartButton = PushButton(GoingUpWindow, text = "START", align ="left")
GoingUpPauseButton = PushButton(GoingUpWindow, text = "PAUSE", align = "right")
GoingUpWindow.hide()
GoingUpButton = PushButton(GoingUpWindow, align = "top",command = GoingUp)
GoingUpWindow.set_full_screen('Esc')

#Final Window to show completion
FinalWindow = Window(app, title="IlluminatorFinal", bg ="white")
FinalText = Text(FinalWindow, text = "that's pretty much it", size = 40, font ="Ariel", color = "#00A3E0")
FinalWindow.hide()
FinalWindow.set_full_screen('Esc')
FinalButton = PushButton(FinalWindow, align = "top",command = FinalWindowCycle)
#FinalWindow.after(20000,FinalWindowCycle)
#App/Home screen characteristics
WelcomeMessage = Text(app, text = "Welcome", size=40, font = "Ariel", color = "#00A3E0", align = "top")
InstructionsMessage = Text(app, text = "Press Bulb to Start", size = 30, font = "Ariel", color = "#86BC25", align = "bottom")
PushBulb = PushButton(app, image = "IlluminatorLogo.png", align = "top",command = BulbPressed)
app.set_full_screen('Esc')

app.after(50000,ExitScreen)
app.display()

#GPIO.cleanup()

