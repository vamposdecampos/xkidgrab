#!/usr/bin/python

from Xlib.display import Display
from Xlib import X, XK, Xcursorfont

def create_font_cursor(dpy, cursor_idx):
	cursor_font = dpy.open_font('cursor')
	return cursor_font.create_glyph_cursor(cursor_font,
		cursor_idx, cursor_idx + 1,
		# swapped bg/fg colors
		(0xffff, 0xffff, 0xffff), (0, 0, 0))

dpy = Display()
root = dpy.screen().root

cursor = create_font_cursor(dpy, Xcursorfont.pirate)

print "# grab:", root.grab_pointer(False, X.ButtonPressMask | X.ButtonReleaseMask,
	X.GrabModeSync, X.GrabModeAsync, X.NONE, cursor, X.CurrentTime)

try:
	while True:
		dpy.allow_events(X.SyncPointer, X.CurrentTime)
		ev = root.display.next_event()
		print "event:", ev
		
	pass
finally:
	dpy.ungrab_pointer(X.CurrentTime)

print "# done"
