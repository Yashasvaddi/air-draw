import cv2
import numpy as np
import mediapipe as mp
import streamlit as st
import time

# Streamlit setup
st.title("Virtual Keyboard with Hand Tracking")
run_app = st.checkbox("Run Keyboard Application")

# Setup for Mediapipe hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Initialize video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    st.error("Error: Could not open video capture.")
    st.stop()

# Array to store pressed keys
pressed_keys = []

# Create keyboard layout
keyboard_layout = [
    "QWERTYUIOP",
    "ASDFGHJKL",
    "ZXCVBNM"
]

# Key positions for tracking
key_positions = []
y_start = 70
for row in keyboard_layout:
    x_start = 10
    row_positions = []
    for char in row:
        row_positions.append((x_start, y_start, x_start + 50, y_start + 50))  # Store key position
        x_start += 55
    key_positions.append(row_positions)
    y_start += 55

# Add DELETE and SPACE button positions
delete_button_pos = (10, y_start + 10, 110, y_start + 60)
space_button_pos = (120, y_start + 10, 220, y_start + 60)

# Timer for frame processing
last_capture_time = time.time()
capture_interval = 1.25  # Time interval in seconds

# Display placeholder for the captured image
image_placeholder = st.empty()
text_placeholder = st.empty()

# Application loop
while run_app:
    ret, frame = cap.read()
    if not ret:
        st.error("Error: Frame not captured.")
        break

    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Redraw the keyboard layout on the frame
    y_start = 70
    for i, row in enumerate(keyboard_layout):
        x_start = 10
        for char in row:
            cv2.rectangle(frame, (x_start, y_start), (x_start + 50, y_start + 50), (0, 0, 0), 2)
            cv2.putText(frame, char, (x_start + 15, y_start + 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
            x_start += 55
        y_start += 55

    # Draw the DELETE and SPACE buttons
    cv2.rectangle(frame, (delete_button_pos[0], delete_button_pos[1]), (delete_button_pos[2], delete_button_pos[3]), (0, 0, 0), 2)
    cv2.putText(frame, "DELETE", (delete_button_pos[0] + 10, delete_button_pos[1] + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.rectangle(frame, (space_button_pos[0], space_button_pos[1]), (space_button_pos[2], space_button_pos[3]), (0, 0, 0), 2)
    cv2.putText(frame, "SPACE", (space_button_pos[0] + 10, space_button_pos[1] + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

    # Process the frame only if 1.5 seconds have passed since the last capture
    current_time = time.time()
    if current_time - last_capture_time >= capture_interval:
        last_capture_time = current_time

        # Process the frame to find hands
        result = hands.process(framergb)
        cursor_position = None

        if result.multi_hand_landmarks:
            for handslms in result.multi_hand_landmarks:
                mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)
                index_finger_tip = handslms.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = handslms.landmark[mpHands.HandLandmark.THUMB_TIP]
                center = (int(index_finger_tip.x * frame.shape[1]), int(index_finger_tip.y * frame.shape[0]))
                cursor_position = center

                distance = np.sqrt((center[0] - int(thumb_tip.x * frame.shape[1]))**2 + 
                                   (center[1] - int(thumb_tip.y * frame.shape[0]))**2)

                if distance < 30:
                    cursor_position = None
                    continue

                for row in key_positions:
                    for key_pos in row:
                        if key_pos[0] < center[0] < key_pos[2] and key_pos[1] < center[1] < key_pos[3]:
                            row_index = key_positions.index(row)
                            col_index = row.index(key_pos)
                            key_char = keyboard_layout[row_index][col_index]

                            if key_char:
                                pressed_keys.append(key_char)
                                text_placeholder.write("".join(pressed_keys))

                            cv2.rectangle(frame, (key_pos[0], key_pos[1]), 
                                          (key_pos[2], key_pos[3]), (0, 255, 0), 2)

                if delete_button_pos[0] < center[0] < delete_button_pos[2] and delete_button_pos[1] < center[1] < delete_button_pos[3]:
                    if pressed_keys:
                        pressed_keys.pop()
                        text_placeholder.write("".join(pressed_keys))

                if space_button_pos[0] < center[0] < space_button_pos[2] and space_button_pos[1] < center[1] < space_button_pos[3]:
                    pressed_keys.append(' ')
                    text_placeholder.write("".join(pressed_keys))

        if cursor_position:
            cv2.circle(frame, cursor_position, 10, (255, 0, 0), -1)

    # Convert frame to displayable format and update the Streamlit image
    image_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

# Release resources after the loop
cap.release()
cv2.destroyAllWindows()
