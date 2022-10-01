import sys
import _thread

sys.path.insert(0, '/Drone')
import esc as sc
import socket as sk

_thread.start_new_thread(sk.connect, ())

# this thread works fine but i need to allocate a lock
# acquire a lock and release the lock in the function
# to be ran by the thread

# make sure run only works after calibrate had been done
# and that run cannot be done while calibrating is in progress