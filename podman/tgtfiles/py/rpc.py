import gevent
import gevent.pywsgi
import gevent.queue
import threading
import time

from tinyrpc.server.gevent import RPCServerGreenlets
from tinyrpc.server import RPCServer
from tinyrpc.dispatch import RPCDispatcher
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.wsgi import WsgiServerTransport

dispatcher = RPCDispatcher()
transport = WsgiServerTransport(queue_class=gevent.queue.Queue)

# start wsgi server as a background-greenlet
wsgi_server = gevent.pywsgi.WSGIServer(('127.0.0.1', 8001), transport.handle, log=None)

#rpc_server = RPCServer(
rpc_server = RPCServerGreenlets(
    transport,
    JSONRPCProtocol(),
    dispatcher
)

class gpio:
   def __init__(self,name,control):
      self.name = name
      self.dir = 0
      self.val = 0
      self.wait_rise = threading.Condition()
      self.wait_fall = threading.Condition()
      self.wait_both = threading.Condition()
      self.control = control
gpios = {}

@dispatcher.public
def reverse_string(s):
    return s[::-1]


@dispatcher.public
def test(*x):
    #print(x)
    return "OK"

@dispatcher.public
def num_gpios(x):
    return ("OK",len(gpios))
   
@dispatcher.public
def gpio_name(n):
    return ("OK",gpios[n].name)

@dispatcher.public
def direction(n):
    return ("OK",gpios[n].dir)

@dispatcher.public
def set_direction(n,d,v):
    gpios[n].dir = d
    #if d == 2:
    #   gpios[n].val = v
    return ("OK")

@dispatcher.public
def value(n):
    return ("OK",gpios[n].val)

@dispatcher.public
def set_value(n,v):
    gpios[n].val = v
    rpc_server.change_handler(n,v)
    return ("OK")

@dispatcher.public
def set_irq_type(n,v):
    gpios[n].irq_type = v
    return ("OK")

@dispatcher.public
def wait_for_interrupt(n):
    if gpios[n].irq_type == 1: # RISING
       with gpios[n].wait_rise:
           if not gpios[n].wait_rise.wait(timeout=1):
               return ("OK",0)
    if gpios[n].irq_type == 2: # FALLING
       with gpios[n].wait_fall:
          if not gpios[n].wait_fall.wait(timeout=1):
               return ("OK",0)
    if gpios[n].irq_type == 3: # BOTH
       with gpios[n].wait_both:
          if not gpios[n].wait_both.wait(timeout=1):
               return ("OK",0)
    return ("OK",1)

def start(change_handler):
  gevent.spawn(wsgi_server.serve_forever)
  rpc_server.change_handler = change_handler
  rpc_server.serve_forever()


