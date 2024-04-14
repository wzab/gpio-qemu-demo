#!/usr/bin/python
import tornado.ioloop
import tornado.web
import os
import gpiod
chip = gpiod.Chip('gpiochip0')
#define pins
LEDS = [24, 25, 26, 27]
LED_PINS = {}
for i in LEDS:
    LED_PINS[i] = chip.get_line(i)
    LED_PINS[i].request(consumer = "Web IF", type = gpiod.LINE_REQ_DIR_OUT)
SWS = [0, 1, 2]
SWS_PINS = {}
for i in SWS:
    SWS_PINS[i] = chip.get_line(i)
    SWS_PINS[i].request(consumer = "Web IF", type = gpiod.LINE_REQ_DIR_IN)

class MyFormHandler(tornado.web.RequestHandler):
    def get(self):
        led_state={}
        switch_state={}
        #Read state of leds
        for i in LEDS:
            led_state[i]=LED_PINS[i].get_value()
        #Read state of switches
        for i in SWS:
            #SWS_PINS[i].update()
            switch_state[i]=SWS_PINS[i].get_value()
        resp='<html><body>'
        resp+='<form action="/" method="post">'
        for i in LEDS:
          print(led_state[i])
          if led_state[i] == 1:
             state1=' checked ="checked" '
             state2=''
          else:
             state1=''
             state2=' checked ="checked" '
          resp+='<input type="radio" name="L'+str(i)+'" value="0" '+state2+'"/> Off '
          resp+='<input type="radio" name="L'+str(i)+'" value="1" '+state1+'"/> On L'+str(i)+'<p>'
        for i in SWS:
          resp+='Switch '+str(i)+': '+str(switch_state[i])+'<p>'
        resp+='<input type="submit" value="Submit">'
        resp+='</form></body></html>'
        print(resp)
        self.write(resp)

    def post(self):
        #self.set_header("Content-Type", "text/plain")
        #self.write("You wrote " + self.get_argument("message"))
        for i in LEDS:
            v=self.get_argument("L"+str(i))
            #a='checked'
            #print i, a
            #if a=="checked":
            #   v='1'
            #else:
            #   v='0'
            print("switching LED"+str(i)+" to:"+v)
            LED_PINS[i].set_value(int(v))
        self.get()

application = tornado.web.Application([
    (r"/", MyFormHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


