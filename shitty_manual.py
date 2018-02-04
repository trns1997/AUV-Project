from pynput import keyboard
import time
import pigpio

SERVO_1 = 4
SERVO_2 = 16

pi = pigpio.pi() # Connect to local Pi.
init = 1460
forward = 1560
reverse = 1360

print("init")
pi.set_servo_pulsewidth(SERVO_1, init)
pi.set_servo_pulsewidth(SERVO_2, init)

def on_press(key):
	if key == keyboard.Key.up:
		print("forward")
		pi.set_servo_pulsewidth(SERVO_1, forward)
		pi.set_servo_pulsewidth(SERVO_2, forward)
	elif key == keyboard.Key.down:
		print("backward")
		pi.set_servo_pulsewidth(SERVO_1, reverse)
		pi.set_servo_pulsewidth(SERVO_2, reverse)
	elif key == keyboard.Key.right:
		print("right")
		pi.set_servo_pulsewidth(SERVO_1, reverse)
		pi.set_servo_pulsewidth(SERVO_2, forward)
	elif key == keyboard.Key.left:
		print("left")
		pi.set_servo_pulsewidth(SERVO_1, forward)
		pi.set_servo_pulsewidth(SERVO_2, reverse)

def on_release(key):
	pi.set_servo_pulsewidth(SERVO_1, init)
	pi.set_servo_pulsewidth(SERVO_2, init)
	if key == keyboard.Key.esc:
		# Stop listener
		return False

# Collect events until released
with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
	listener.join()
