from guizero import App, Text, PushButton, TextBox, Picture, Window
import RPi.GPIO as GPIO
import time

# The function for ultrasonic sensor working in a loop.
####### fix the switch timing issue in the while loop!!!!!######
GPIO.setmode(GPIO.BCM)

#Ultrasonic Pins being used
TRIG = 23
ECHO = 12
LIMIT = 13 
#Pins being used for Relays
DCpos = 17 #D1
DCneg = 27 #D2
actpos = 22 #D3
actneg = 5 #D4

print ("Starting Measurements...")

###Setup all necessary GPIO pins
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(LIMIT, GPIO.OUT)
#GPIO.output(TRIG,0)

#GPIO for Relays
GPIO.setup(DCpos, GPIO.OUT)
GPIO.setup(DCneg, GPIO.OUT)
GPIO.setup(actpos, GPIO.OUT)
GPIO.setup(actneg, GPIO.OUT)

###Set GPIO pins to output
GPIO.output(TRIG, 0)
GPIO.output(DCpos, GPIO.LOW)
GPIO.output(DCneg, GPIO.LOW)
GPIO.output(actpos, GPIO.LOW)
GPIO.output(actneg, GPIO.LOW)
GPIO.output(LIMIT, GPIO.LOW)

n =1
x =1
i =1

def take_distance():
        #had constants here
        global n
        global i
        global x
        distance = 12
        app.hide()
        while distance > 10:
                print ("waiting for sensor to settle")

                time.sleep(2)
                GPIO.output(TRIG, 1)
                time.sleep(0.00001)
                GPIO.output(TRIG, 0)
                #actuator going up until distance < 10
                GPIO.output(actpos, GPIO.HIGH)
                GPIO.output(actneg, GPIO.LOW)

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
                StatText = Text(ProcessWindow, text = distancestring, size=30, $
                #StatText = Text(GoingUpWindow, text = distancestring, size=30,$
                distance = pulse_duration*17150
                distance = round(distance, 2)
                app.update()
                StatText.destroy()
        #set actuator to LOW state
        GPIO.output(actpos, GPIO.LOW)
        GPIO.output(actneg, GPIO.LOW)
        #set DC motor to HIGH
        if x == 1:
               GPIO.output(DCpos, GPIO.HIGH)
                GPIO.output(DCneg, GPIO.LOW)
                time.sleep(5)
                #set DC motor to LOW
                GPIO.output(DCpos, GPIO.LOW)
                GPIO.output(DCneg, GPIO.LOW)
        else:
                GPIO.output(DCpos, GPIO.LOW)
                GPIO.output(DCneg, GPIO.HIGH)
                time.sleep(5)
                #set DC motor to LOW
                GPIO.output(DCpos, GPIO.LOW)
                GPIO.output(DCneg, GPIO.LOW)

        ###this is where movement of actuator down until limit is reached#####
        try:
                while not GPIO.input(13):
#                       print("low")
                        #set actuator to go DOWN
                        GPIO.output(actpos, GPIO.LOW)
                        GPIO.output(actneg, GPIO.HIGH)
                        pass
                #set actuator to LOW at bottom
                GPIO.output(actpos, GPIO.LOW)
                GPIO.output(actneg, GPIO.LOW)
        finally:
                if n == 1 and i == 1: #we need to not go here if Limit switch x2
                        ProcessFinish()
                        n += 1
                        i += 1
                        x += 1
               #have counter for limit switch
                #if i == 1 #add this to n==1 condition
                else:
                        GoingUp()

def BulbPressed():
        #summon the next screen that says "In Process" and displays stat/pause $
        distance = 11
        ProcessWindow.show()
        take_distance()
        #set actuator to go DOWN?????? here instead of take_distance
        time.sleep(30)
#       app.update()
        app.hide()
def ProcessFinish():
        ProcessWindow.hide()
        SwitchBulbWindow.show()
        app.update() #may need to take out CHANGE 1
def SwitchBulb():
        SwitchBulbWindow.hide()
        GoingUpWindow.show()
        app.update()
        take_distance()
        app.update() # may need to take out CHANGE 2
def GoingUp():
        GoingUpWindow.hide() #hide ProvidingLight window
        FinalWindow.show()
        app.update()
def FinalWindowCycle():
        #This will bring the app display back into the home screen
        FinalWindow.hide()
        app.show()
#       app.update()

        n = 1   # resetting if loop variable  to 1 for repetition
        x = 1   # resetting DC motor constant
#       app.exit_full_screen()

def ExitScreen():
        app.exit_full_screen()
        ProcessWindow.exit_full_screen()
        SwitchBulbWindow.exit_full_screen()
        GoingUpWindow.exit_full_screen()
        FinalWindow.exit_full_screen()
        app.update()
        i = 1
app = App(title = "IlluminatorIntro", bg = "white") #Main app acreen

#App/Home screen characteristics
#WelcomeMessage = Text(app, text = "Welcome", size=40, font = "Ariel", color = $
#InstructionsMessage = Text(app, text = "Press Bulb to Start", size = 30, font $
#PushBulb = PushButton(app, image = "IlluminatorLogo.png", align = "top",comman$
#app.set_full_screen('Esc')

####Initial window that demonstrates bulb removal
ProcessWindow = Window(app, title="IlluminatorProcess", bg = "white")
RemoveBulbMessage = Text(ProcessWindow, text ="Removing Bulb", size=40, font = $
PauseButton = PushButton(ProcessWindow, text = "PAUSE", align = "right")
ProcessWindow.hide()
#ProcessWindow.after(5000, ProcessFinish)
ProcessWindow.set_full_screen('Esc')


########### New Window for the user to switch out the bulb:
SwitchBulbWindow = Window(app, title="IlluminatorSwitch", bg ="white")
SwitchBulbText = Text(SwitchBulbWindow, text="Please Switch The Light Bulb With$
#ReadyButton = PushButton(SwitchBulbWindow, text = "READY")
SwitchBulbWindow.hide()
#testing an IF statement for actuator##################
#if GPIO.input(13):
#       GPIO.output(actpos, GPIO.LOW) #set actuator to LOW
#       GPIO.output(actneg, GPIO.LOW)
#       SwitchBulb() #switchbulb function
SwitchBulbButton = PushButton(SwitchBulbWindow, text="Ready",align = "top",comm$
#SwitchBulbWindow.after(10000, SwitchBulb)#
SwitchBulbWindow.set_full_screen('Esc')

##############Window 3 for going back up
#if ReadyButton HIGH
#       GoingUp function
GoingUpWindow = Window(app, title ="IlluminatorUP", bg ="white")
ProvidingLightText = Text(GoingUpWindow, text="Providing Light...", size=40, fo$
#GoingUpStartButton = PushButton(GoingUpWindow, text = "START", align ="left")
GoingUpPauseButton = PushButton(GoingUpWindow, text = "PAUSE", align = "right")
GoingUpWindow.hide()
GoingUpButton = PushButton(GoingUpWindow, align = "top",command = GoingUp)
GoingUpWindow.set_full_screen('Esc')

###############Final Window to show completion
FinalWindow = Window(app, title="IlluminatorFinal", bg ="white")
FinalText = Text(FinalWindow, text = "that's pretty much it", size = 40, font =$
FinalWindow.hide()
FinalWindow.set_full_screen('Esc')
FinalButton = PushButton(FinalWindow, align = "top",command = FinalWindowCycle)
#FinalWindow.after(20000,FinalWindowCycle)

###############App/Home screen characteristics
WelcomeMessage = Text(app, text = "Welcome", size=40, font = "Ariel", color = "$
InstructionsMessage = Text(app, text = "Press Bulb to Start", size = 30, font =$
PushBulb = PushButton(app, image = "IlluminatorLogo.png", align = "top",command$
app.set_full_screen('Esc')

app.after(50000,ExitScreen)
app.display()

#GPIO.cleanup()
