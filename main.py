import network
import socket
import time
from machine import Pin, PWM
from time import sleep

relay = Pin(17, Pin.OUT) # The pin that is connected to the Input Circuit of the Relay
ssid = 'PEN TEST'
password = 'ConstantGrowth#999'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)


html = """<!DOCTYPE html>
<html>
<style>
.button {
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
}

.button1 {background-color: #04AA6D;} /* Green */
.button2 {background-color: #008CBA;} /* Blue */
</style>
    <body> <h1 style="font-size:2vw">Caveman's Corner - Treat Launcher</h1>
        <p style="font-size:5vw">%s</p>
        <iframe src="https://giphy.com/embed/5xaOcLGm3mKRQuDYCgU" width="480" height="250" style="" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/cat-rocket-5xaOcLGm3mKRQuDYCgU">via GIPHY</a></p>
        <form action="http://30.30.30.204/launch">
            <input style="font-size:10vw" class="button1" type="submit" value="launch" />
        </form>
        <p></p>
        <form action="http://30.30.30.204/act_2_on">
            <input style="font-size:2vw" type="submit" value="act_2_on" />
        </form>
    </body>
</html>
"""

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

temp = 'off'


# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print(request)

        request = str(request)
        launch = request.find('/launch')
        act_2_on = request.find('/act_2_on')
        #print( 'outlet on = ' + str(outlet_on))
        #print( 'outlet off = ' + str(outlet_off))
        stateis = ""

        if launch == 6:
            #turn stuff on goes here
            print("launch")
            #outlet.value(1)
            stateis = "launch"
            #outlet.value(1)
            #pwm.duty_u16(40000)
            #time.sleep(2)
            #pwm = PWM(21, freq=1000, duty_u16=0)  # create a PWM object on a pin            pwm = PWM(21, freq=1000, duty_u16=30000)  # create a PWM object on a pin
            relay.value(1)
            time.sleep(1.5)
            pwm = PWM(21, freq=700, duty_u16=25000)
            sleep(0.1)
            pwm = PWM(21, freq=700, duty_u16=60000)
            sleep(0.1)
            pwm = PWM(21, freq=700, duty_u16=25000)
            sleep(1)
            # create a PWM object on a pin
            pwm = PWM(21, freq=700, duty_u16=0)  # create a PWM object on a pin
            time.sleep(1)
            relay.value(0)
        



        if act_2_on == 6:
            #turn stuff off goes here
            print("act_2_on")
            #outlet.value(0)
            stateis = "act_2_on"
            #outlet.value(0)

        response = html % stateis

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')







