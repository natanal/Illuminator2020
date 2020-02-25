from guizero import App, Text, PushButton, TextBox, Picture, Window
def BulbPressed():
        #summon the next screen that says "In Process" and displays stat/pause button
        ProcessWindow.show()
        app.hide()
        app.update()
def ProcessFinish():
        ProcessWindow.hide()
        SwitchBulbWindow.show()
        app.update()
def SwitchBulb():
        SwitchBulbWindow.hide()
        GoingUpWindow.show()
        app.update()
def GoingUp():
        GoingUpWindow.hide()
        FinalWindow.show()
        app.update()
def FinalWindowCycle():
        #This will bring the app display back into the home screen
        FinalWindow.hide()
        app.show()
        app.update()
        def ExitScreen():
        app.exit_full_screen()
        ProcessWindow.exit_full_screen()
        SwitchBulbWindow.exit_full_screen()
        GoingUpWindow.exit_full_screen()
        FinalWindow.exit_full_screen()
        app.update()
app = App(title = "IlluminatorIntro", bg = "white") #Main app acreen
#Initial window that demonstrates bulb removal
ProcessWindow = Window(app, title="IlluminatorProcess", bg = "white")
RemoveBulbMessage = Text(ProcessWindow, text ="Removing Bulb", size=40, font = "Ariel", color = "#00A3E0", align = "top")
PauseButton = PushButton(ProcessWindow, text = "PAUSE", align = "right")
StatText = Text(ProcessWindow, text = "randotext", size=30, font = "Ariel", color="#86BC25", align = "left")
ProcessWindow.hide()
ProcessWindow.after(5000, ProcessFinish)
ProcessWindow.set_full_screen('Esc')

# New Window for the user to switch out the bulb:
SwitchBulbWindow = Window(app, title="IlluminatorSwitch", bg ="white")
SwitchBulbText = Text(SwitchBulbWindow, text="Please Switch The Light Bulb With a New Bulb", size=40, font = "Ariel", color = "#00A3E0", align ="top")
ReadyButton = PushButton(SwitchBulbWindow, text = "READY")
SwitchBulbWindow.hide()
SwitchBulbWindow.after(10000, SwitchBulb)
SwitchBulbWindow.set_full_screen('Esc')

#Window 3 for going back up
GoingUpWindow = Window(app, title ="IlluminatorUP", bg ="white")
ProvidingLightText = Text(GoingUpWindow, text="Providing Light...", size=40, font="Ariel", align="top")
GoingUpStartButton = PushButton(GoingUpWindow, text = "START", align ="left")
GoingUPPauseButton = PushButton(GoingUpWindow, text = "PAUSE", align = "right")
GoingUpWindow.hide()
GoingUpWindow.after(15000, GoingUp)
GoingUpWindow.set_full_screen('Esc')

#Final Window to show completion
FinalWindow = Window(app, title="IlluminatorFinal", bg ="white")
FinalText = Text(FinalWindow, text = "that's pretty much it", size = 40, font ="Ariel", color = "#00A3E0")
FinalWindow.hide()
FinalWindow.set_full_screen('Esc')
FinalWindow.after(20000,FinalWindowCycle)

#App/Home screen characteristics
WelcomeMessage = Text(app, text = "Welcome", size=40, font = "Ariel", color = "#00A3E0", align = "top")
InstructionsMessage = Text(app, text = "Press Bulb to Start", size = 30, font = "Ariel", color = "#86BC25", align = "bottom")
PushBulb = PushButton(app, image = "IlluminatorLogo.png", align = "top",command = BulbPressed)
app.set_full_screen('Esc')
app.after(30000,ExitScreen)
app.display()
