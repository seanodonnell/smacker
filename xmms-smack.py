#!/usr/bin/env python
#
#reqires  PyXMMS (http://people.via.ecp.fr/~flo/index.en.xhtml)
#apt-get install python-xmms on debian/ubuntu
#start and open your playlist before smacks will have any effect
#
#based on http://www.oakcourt.dyndns.org/~andrew/journal/?p=28 by Andrew Barr
#which was in turn based on http://blog.micampe.it/articles/2006/06/04/here-comes-the-smackpad by Michele Campeotto
#inspired by the original http://blog.medallia.com/2006/05/smacbook_pro.html
#
#(c)2006 Sean O'Donnell <sean@odonnell.nu>, GPLv2
import xmms.control
import sys, re, time

class Smacker:
    """A class that can be extended to control the effect of smacking your
     thinkpad. Make sure to to override the add on_left and on_right methods.
    """

    POS_FILE = '/sys/devices/platform/hdaps/position'
    CAL_FILE = '/sys/devices/platform/hdaps/calibrate'
    POS_RX = re.compile('^\((-?\d+),(-?\d+)\)$')
    
    def __init__(self,sensitivity = 6, interval = 0.005,stability = 30):
        """sensitivity control the sensitivity of the laptop
           to smacks and other disturbances, its should be an integer,
           the lower it is the more sensitive. The default is 4.

           interval is the time between position checks, measured in 
           seconds. This should be an integer or floating point number.
           The default is 0.01"""

        self.sensitivity = sensitivity 
        self.interval = interval
        self.stability = 30

    def start(self):
        """Starts handling smack events"""
        try:
            self._loop()
        except KeyboardInterrupt:
            pass

    def _loop(self):
        #get the starting position of the laptop
        calx, caly = self.get_calibration()
        stable = 0
        while True:
            # get the current position
            x, y = self.get_pos()
            if x == 0: continue
            #the difference between the starting and current x position
            delta = x - calx
            #get the absolute value of the difference
            adelta = abs(delta)
            #if the difference is less than 5
            if adelta < 5:
                #increment stable
                stable += 1
            #if the difference is greater than the sensitivity 
            #and stable is greater than i.e. the laptop has been stable for
            #a while, and now its been struck, prevents the effent firing
            # more than once per strike
            if adelta > self.sensitivity and stable > self.stability:
                #reset stable
                stable = 0
                #if the laptop hit on the left side
                if delta < 0:
                    self.on_left()
                else:
                    self.on_right() 
            time.sleep(self.interval)

    def on_left(self):
        """Handler for when the laptop is smacked to the left, should be overwritten"""
        pass
    def on_right(self):
        """Handler for when the laptop is smacked to the left, should be overwritten"""
        pass

    def get_pos(self):
        """get the position of the laptop, returns an x,y tuple,
           a low x indicates the left hand side of the laptop is raised,
           a high x , that the right hand side is raised, these correspond
           with a smack to the left and right (hopefully). A low y indicates
           that the laptop is tiled forward, a high y that it is tiled backward"""
        pos = open(Smacker.POS_FILE).read()
        match = Smacker.POS_RX.match(pos)
        return (int(match.groups()[0]), int(match.groups()[1]))

    def get_calibration(self):
        """get the calibration of the laptop"""
        pos = open(Smacker.CAL_FILE).read()
        match = Smacker.POS_RX.match(pos)
        return (int(match.groups()[0]), int(match.groups()[1]))


class XMMSSmack(Smacker):
    def on_left(self):
        self.next_tune()

    def on_right(self):
        self.on_left()

    def next_tune(self):
        xmms.control.playlist_next()

class TestSmack(Smacker):
    def on_left(self):
        print "left"

    def on_right(self):
        print "right"

def main():
    smacker = XMMSSmack()
    smacker.start()

if __name__ == "__main__":
    main()
    
