
#!/usr/bin/python3
# This code is based on a GUI prepared for BR_InternetRadio project:
# https://github.com/wzab/BR_Internet_Radio/tree/gpio_simple/QemuVirt64/GUI
# Which in turn was based on the following sources:
# https://lazka.github.io/pgi-docs
# https://python-gtk-3-tutorial.readthedocs.io/en/latest/button_widgets.html
# https://developer.gnome.org/gtk3/stable/
# Threads: https://wiki.gnome.org/Projects/PyGObject/Threading

# What must be installed in the virtual environment:
# pip install tinyrpc gevent werkzeug pgi
import pgi
pgi.require_version("Gtk", "3.0")
from pgi.repository import Gtk, GLib, Gdk
import gevent
import threading

#Global variables (will be filled when bulding the GUI)
class glb:
    pass

import random
import time
    
def generate_bouncing():
    if glb.bouncing_active.get_active():
        # Generate the odd number of transient times (3,5 or 7) between 0
        # and the duration time of the bouncing
        ntr = random.choice((3,5,7))
        duration = glb.bouncing_duration.get_value()
        trs = [random.randint(0,duration) for i in range(0,ntr)]
        trs.sort()
        return trs
    else:
        return (0,)

def send_bounced_change(nof_pin,state):
    if not glb.bouncing_active.get_active():
        send_change(nof_pin,state)
    else:
        trs = generate_bouncing()
        last = 0
        for trans in trs:
            time.sleep(0.001*(trans-last))
            last = trans
            send_change(nof_pin,state)
            state = 1 - state

def send_change(nof_pin, state):
    do_irq = (rpc.gpios[nof_pin].val != state)
    rpc.gpios[nof_pin].val = state
    if do_irq:
        with rpc.gpios[nof_pin].wait_both:
            rpc.gpios[nof_pin].wait_both.notify_all()
        if state == 1:
            with rpc.gpios[nof_pin].wait_rise:
                rpc.gpios[nof_pin].wait_rise.notify_all()
        if state == 0:
            with rpc.gpios[nof_pin].wait_fall:
                rpc.gpios[nof_pin].wait_fall.notify_all()

def recv_change(nof_pin, s):
    GLib.idle_add(MyControls[nof_pin].change_state,s)
        
class MySwitch(Gtk.Switch):
    dir = 0 #Input
    def __init__(self,number):
        super().__init__()
        self.number = number
        self.state = 0
    def change_state(self,state):
        pass

class MyButton(Gtk.Button):
    dir = 0 #Input
    def __init__(self,number):
        super().__init__(label=str(number))
        self.number = number
        self.state = 1
    def change_state(self,state):
        pass
        
class MyLed(Gtk.Label):
    dir = 1 # Output
    color = Gdk.color_parse('gray')
    rgba0 = Gdk.RGBA.from_color(color)
    color = Gdk.color_parse('green')
    rgba1 = Gdk.RGBA.from_color(color)
    del color
    
    def __init__(self, number):
        super().__init__( label=str(number))
        self.number = number
        self.change_state(0)
        self.state = 0
    def change_state(self,state):
        self.state = state
        if state == 1:
            self.override_background_color(0,self.rgba1)
        else:
            self.override_background_color(0,self.rgba0)
    
MyControls = {}
    
class SwitchBoardWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Switch Demo")
        self.set_border_width(10)
        mainvbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        self.add(mainvbox)
        #Create the switches
        label = Gtk.Label(label = "Stable switches: left 0, right 1")
        mainvbox.pack_start(label,True,True,0)
        hbox = Gtk.Box(spacing=6)
        for i in range(0,12):
            vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
            label = Gtk.Label(label = str(i))
            vbox.pack_start(label,True,True,0)            
            switch = MySwitch(i)
            switch.connect("state_set", self.on_switch_activated)
            switch.set_active(False)
            MyControls[i] = switch
            rpc.gpios[i] = rpc.gpio("switch"+str(i),switch)
            vbox.pack_start(switch,True,True,0)            
            hbox.pack_start(vbox, True, True, 0)
        mainvbox.pack_start(hbox,True,True,0)
        #Create the buttons
        label = Gtk.Label(label = "Unstable buttons: pressed 0, released 1")
        mainvbox.pack_start(label,True,True,0)
        hbox = Gtk.Box(spacing=6)
        for i in range(12,24):
            button = MyButton(i)
            button.connect("button-press-event", self.on_button_clicked,0)
            button.connect("button-release-event", self.on_button_clicked,1)
            MyControls[i] = button
            rpc.gpios[i] = rpc.gpio("button"+str(i),button)
            hbox.pack_start(button,True,True,0)            
        mainvbox.pack_start(hbox,True,True,0)
        #Create the LEDS
        label = Gtk.Label(label = "LEDs")
        mainvbox.pack_start(label,True,True,0)
        hbox = Gtk.Box(spacing=6)
        for i in range(24,32):
            led = MyLed(i)
            MyControls[i] = led
            rpc.gpios[i] = rpc.gpio("led"+str(i),led)
            hbox.pack_start(led,True,True,0)            
        mainvbox.pack_start(hbox,True,True,0)
        #Add the configuration controlls
        hbox = Gtk.Box(spacing=6)
        #Add the reconnect button
        #button = Gtk.Button(label="Reconnect")
        #button.connect("clicked", Reconnect)
        hbox.pack_start(button,True,True,0)
        #Add the contact bouncing settings
        button=Gtk.CheckButton(label="Bouncing")
        button.set_active(1)
        glb.bouncing_active = button
        hbox.pack_start(button,True,True,0)
        label=Gtk.Label(label="duration [ms]")
        hbox.pack_start(label,True,True,0)
        spinner=Gtk.SpinButton()
        spinner.set_range(0,300)
        spinner.set_value(200)
        spinner.set_increments(1,10)
        glb.bouncing_duration=spinner
        hbox.pack_start(spinner,True,True,0)
        mainvbox.pack_start(hbox,True,True,0)
        
    def on_switch_activated(self, switch, gparam):
        if switch.get_active():
            state = 1
        else:
            state = 0
        #MyLeds[switch.number].change_state(state)
        send_bounced_change(switch.number,state)
        self.state = state
        #print("Switch #"+str(switch.number)+" was turned", state)
        return True

    def on_button_clicked(self, button,gparam, state):
        #print("pressed!")
        send_bounced_change(button.number,state)
        self.state = state
        #print("Button #"+str(button.number)+" was turned", state)
        return True

import rpc

win = SwitchBoardWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()

def rpc_start(x):
    rpc.start(x)

#rpc.rpc_server.serve_forever()    
thread = threading.Thread(target=Gtk.main)
thread.daemon = True
thread.start()
rpc_start(recv_change)


