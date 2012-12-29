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
esc_keycode = dpy.keysym_to_keycode(XK.XK_Escape)

print "# grab pointer:", root.grab_pointer(False,
	X.ButtonPressMask | X.ButtonReleaseMask,
	X.GrabModeAsync, X.GrabModeAsync, X.NONE, cursor, X.CurrentTime)
print "# grab keyboard:", root.grab_keyboard(False,
	X.GrabModeAsync, X.GrabModeAsync, X.CurrentTime)

try:
	while True:
		ev = root.display.next_event()
		print "event:", ev

		if ev.type == X.KeyRelease and ev.detail == esc_keycode:
			print "# escape"
			break
finally:
	dpy.ungrab_keyboard(X.CurrentTime)
	dpy.ungrab_pointer(X.CurrentTime)

print "# done"
