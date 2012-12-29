#!/usr/bin/python

from Xlib.display import Display
from Xlib import X, XK

dpy = Display()
root = dpy.screen().root


print "# grab:", root.grab_pointer(False, X.ButtonPressMask | X.ButtonReleaseMask,
	X.GrabModeSync, X.GrabModeAsync, X.NONE, X.NONE, X.CurrentTime)

try:
	while True:
		dpy.allow_events(X.SyncPointer, X.CurrentTime)
		ev = root.display.next_event()
		print "event:", ev
		
	pass
finally:
	dpy.ungrab_pointer(X.CurrentTime)

print "# done"
