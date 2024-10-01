from djitellopy import Tello
from pynput import keyboard
#import cv2
import numpy as np
import threading

# Initialize the drone
me = Tello()
me.connect()
print(me.get_battery())
me.takeoff()
#me.streamon()  # Start the video stream


# Function to handle keyboard events
def on_press(key):
    try:
        if key.char == 'w':
            me.send_rc_control(0, 50, 0, 0)
        elif key.char == 's':
            me.send_rc_control(0, -50, 0, 0)
        elif key.char == 'a':
            me.send_rc_control(50, 0, 0, 0)
        elif key.char == 'd':
            me.send_rc_control(-50, 0, 0, 0)
        elif key.char == 'q':
            me.send_rc_control(0, 0, 50, 0)
        elif key.char == 'e':
            me.send_rc_control(0, 0, -50, 0)
        elif key.char == 'z':
            me.send_rc_control(0, 0, 0, 50)
        elif key.char == 'c':
            me.send_rc_control(0, 0, 0, -50)
        elif key.char == 'o':
            me.send_rc_control(0, 0, 0, 0)
            me.land()
            #me.streamoff()  # Stop the video stream
            return False  # Stop listener
    except AttributeError:
        pass  # Ignore other keys


# Function to continuously get and display video feed
def display_video_feed():
    while True:
        try:
            frame = me.get_frame_read().frame

            if frame is None:
                print("Received None frame")
                continue

            if not isinstance(frame, np.ndarray):
                print("Frame is not a numpy array")
                continue

            print(f"Frame dimensions: {frame.shape[1]}x{frame.shape[0]}, Channels: {frame.shape[2]}")
            print(f"Frame data type: {frame.dtype}")

            if frame.size == 0:
                print("Received empty frame")
                continue

            # Convert RGB to BGR if needed
            if frame.shape[2] == 3:  # Assuming it might be RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            img = cv2.resize(frame, (360, 240))
            cv2.imshow("image", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Close the window when 'q' is pressed
                break

        except cv2.error as e:
            print(f"OpenCV error: {e}")
            break
        except Exception as e:
            print(f"Error while getting frame: {e}")
            break


# Start the video feed thread
#video_thread = threading.Thread(target=display_video_feed)
#video_thread.start()

# Collect keyboard events
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

# Clean up
#cv2.destroyAllWindows()
me.end()
