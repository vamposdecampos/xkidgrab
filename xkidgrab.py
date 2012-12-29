#!/usr/bin/python

ESCAPE_COUNT = 3
from Xlib.display import Display
from Xlib import X, XK, Xcursorfont

def create_font_cursor(dpy, cursor_idx,
		fore=(0xffff, 0xffff, 0xffff),
		back=(0, 0, 0)):
	cursor_font = dpy.open_font('cursor')
	return cursor_font.create_glyph_cursor(cursor_font,
		cursor_idx, cursor_idx + 1,
		fore, back)

dpy = Display()
root = dpy.screen().root

cursor = create_font_cursor(dpy, Xcursorfont.pirate)
active_cursor = create_font_cursor(dpy, Xcursorfont.pirate, fore=(0xffff, 0, 0))
esc_keycode = dpy.keysym_to_keycode(XK.XK_Escape)

# other intersting keys:
XK.load_keysym_group('xf86')
XK.XK_XF86_PowerOff
XK.XK_XF86_AudioMedia

print "# grab pointer:", root.grab_pointer(False,
	X.ButtonPressMask | X.ButtonReleaseMask,
	X.GrabModeAsync, X.GrabModeAsync, X.NONE, cursor, X.CurrentTime)
print "# grab keyboard:", root.grab_keyboard(False,
	X.GrabModeAsync, X.GrabModeAsync, X.CurrentTime)

# cheap.
import os
os.system('notify-send "XKidGrab" "Keyboard and mouse buttons grabbed.' +
	'  Exit by pressing Escape %d times."' % ESCAPE_COUNT)

active_cnt = 0
escape_cnt = 0
try:
	while True:
		ev = root.display.next_event()
		print "event:", ev

		last_active = active_cnt
		if ev.type in (X.ButtonPress, X.KeyPress):
			active_cnt += 1
		elif ev.type in (X.ButtonRelease, X.KeyRelease):
			if active_cnt > 0:
				active_cnt -= 1

		if (not not last_active) != (not not active_cnt):
			dpy.change_active_pointer_grab(X.ButtonPressMask | X.ButtonReleaseMask,
				active_cursor if active_cnt else cursor,
				X.CurrentTime)

		if ev.type == X.KeyRelease:
			if ev.detail == esc_keycode:
				escape_cnt += 1
				print "# escape:", escape_cnt
			else:
				escape_cnt = 0
			if escape_cnt >= ESCAPE_COUNT:
				break
finally:
	dpy.ungrab_keyboard(X.CurrentTime)
	dpy.ungrab_pointer(X.CurrentTime)

print "# done"
