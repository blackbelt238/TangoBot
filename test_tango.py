import time
from tango import Tango

t = Tango()

# move Tango forward to the first speed, go for 1 second, and stop
t.drive(False)
time.sleep(1)
t.stop()
