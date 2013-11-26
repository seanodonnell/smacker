smacker
=======

Library for controlling you laptop via the acceleromater

After playing with smack.py (http://www.oakcourt.dyndns.org/~andrew/journal/?p=28) and enjoying thumping my laptop to switch desktops, I began thinking of other uses for the smacking interface. One finally hit me. Depending on my mood I sometimes play music on my Thinkpad while I work , however if I get bored, or annoyed by a song I have 2 choices. Be irritated, or break my flow while I maximize XMMS and move on in my playlist.

It just seems so perfect, dont like the music? Smack the screen and move on! So I adapted the original smack.py script and here you are, xmms-smack.py. Once its running, if you thump your Thinkpad XMMS will move on to the next song on your playlist. xmms-smack.py requires that you have HDAPS (http://hdaps.sourceforge.net/) on your Thinkpad, and you have PyXMMS ("sudo apt-get install python-xmms" on debian/ubuntu) installed as well as Python. To start it just run "python xmms-smack.py".

While I was at it I decided to make future smack based scripts a little easier to get up and running. I created the smacker class. To create a left/right based smacker just extend the Smacker class like so.

class TestSmack(Smacker):

    """an example smacker implementation"""

    def on_left(self):
        print "left"

    def on_right(self):
        print "right"

I may adapt Smacker to also handle forward/back tilting and anything else thats handy as the need arises. If anyone wants to try it before I do, Ill be happy to take their patches.

