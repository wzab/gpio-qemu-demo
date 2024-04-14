#!/usr/bin/python
import tornado.ioloop
import tornado.web
import os
#define pins
base=480
LEDS=[base+24,base+25,base+26,base+27]
SWS=[base+0,base+1,base+2]
#Export pins
for i in LEDS+SWS:
  os.system("echo "+str(i)+" > /sys/class/gpio/export")
#Set LEDS to outputs and switch them off
for i in LEDS:
  os.system("echo low > /sys/class/gpio/gpio"+str(i)+'/direction')

class MyFormHandler(tornado.web.RequestHandler):
    def get(self):
        led_state={}
        switch_state={}
        #Read state of leds
        for i in LEDS:
            with open('/sys/class/gpio/gpio'+str(i)+'/value','r') as f:
                led_state[i]=int(f.read())
        #Read state of switches
        for i in SWS:
            with open('/sys/class/gpio/gpio'+str(i)+'/value','r') as f:
                switch_state[i]=int(f.read())
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
            with open('/sys/class/gpio/gpio'+str(i)+'/value','w') as f:
               f.write(v)
        self.get()

application = tornado.web.Application([
    (r"/", MyFormHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


