import time
from tango import Tango

t = Tango()

# move Tango forward to the first speed, go for 1 second, and stop
t.drive(True)
time.sleep(1)
t.stop()

# move back to 2nd speed, go for 1 sec, stop
t.drive(False)
t.drive(False)
time.sleep(1)
t.stop()

# twist left, then right
t.twist(False)
time.sleep(1)
t.twist(True)
t.twist(True)
time.sleep(1)

# look up to max, look down to maximum
t.head(t.UPDOWN, True)
t.head(t.UPDOWN, True)
time.sleep(1)
t.head(t.UPDOWN, False)
t.head(t.UPDOWN, False)
t.head(t.UPDOWN, False)
t.head(t.UPDOWN, False)

# look left to max, look right to maximum
t.head(t.SIDE, True)
t.head(t.SIDE, True)
time.sleep(1)
t.head(t.SIDE, False)
t.head(t.SIDE, False)
t.head(t.SIDE, False)
t.head(t.SIDE, False)

time.sleep(5)
t.reset() # reset everything before continuing on with tests
