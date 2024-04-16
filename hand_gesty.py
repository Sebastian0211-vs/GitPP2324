import cv2
import mediapipe as mp
import math

# Global variables
fingers_tip_id = [4, 8, 12, 16, 20]

# Initializes MediaPipe Hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=2,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

def is_hand_closed_except_thumb(hand_landmarks):
    """Check if the hand is closed by comparing fingertips with their MCPs."""
    # Landmarks for fingertips and MCP (Metacarpophalangeal) joints.
    fingertips = [mp_hands.HandLandmark.INDEX_FINGER_TIP,
                  mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP,
                  mp_hands.HandLandmark.PINKY_TIP]

    mcp_joints = [mp_hands.HandLandmark.INDEX_FINGER_MCP,
                  mp_hands.HandLandmark.MIDDLE_FINGER_MCP, mp_hands.HandLandmark.RING_FINGER_MCP,
                  mp_hands.HandLandmark.PINKY_MCP]

    closed_fingers = 0
    for fingertip, mcp in zip(fingertips, mcp_joints):
        if hand_landmarks.landmark[fingertip].y > hand_landmarks.landmark[mcp].y:
            closed_fingers += 1

    # Considering the hand closed if all fingers are closed.
    return closed_fingers == 4

def calculate_distance(landmark1, landmark2):
    """Calculates the Euclidean distance between two landmarks."""
    return math.sqrt((landmark1.x - landmark2.x) ** 2 + (landmark1.y - landmark2.y) ** 2 + (landmark1.z - landmark2.z) ** 2)

def count_extended_fingers(hand_landmarks):
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    index_base = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]

    # Fingertip and MCP joint IDs for the four fingers (excluding thumb)
    finger_tips_ids = [mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                       mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP]
    finger_mcp_ids = [mp_hands.HandLandmark.INDEX_FINGER_MCP, mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
                      mp_hands.HandLandmark.RING_FINGER_MCP, mp_hands.HandLandmark.PINKY_MCP]

    nbr_extended_fingers = 0
    for tip_id, mcp_id in zip(finger_tips_ids, finger_mcp_ids):
        fingertip = hand_landmarks.landmark[tip_id]
        finger_base = hand_landmarks.landmark[mcp_id]

        # Calculates distances
        distance_wrist_to_tip = calculate_distance(wrist, fingertip)
        distance_wrist_to_base = calculate_distance(wrist, finger_base)

        # Determines if the finger is extended
        if distance_wrist_to_tip > distance_wrist_to_base * 1.2:  # Threshold can be adjusted
            nbr_extended_fingers += 1

    # Handles thumb separately
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_base = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC]
    distance_thumb_tip_to_index_base = calculate_distance(thumb_tip, index_base)
    distance_thumb_base_to_index_base = calculate_distance(thumb_base, index_base)

    # You may need to adjust the threshold based on empirical testing
    if distance_thumb_tip_to_index_base > distance_thumb_base_to_index_base * 0.6:
        nbr_extended_fingers += 1

    return nbr_extended_fingers

#def count_fingers(hand_landmarks):
    # Tips and base joints of each finger
    finger_tips = [8, 12, 16, 20]  # Excluding the thumb for simplicity
    finger_mcp = [5, 9, 13, 17]  # MCP (Metacarpophalangeal joints) base of each finger

    nbr_fingers_up = 0

    # Check each finger except the thumb
    for tip, mcp in zip(finger_tips, finger_mcp):
        # Get the landmarks
        tip_landmark = hand_landmarks.landmark[tip]
        mcp_landmark = hand_landmarks.landmark[mcp]
        pip_landmark = hand_landmarks.landmark[tip - 2]  # PIP (Proximal Interphalangeal joint)

        # Calculate distances
        tip_to_pip_distance = find_distance(tip_landmark, pip_landmark)
        pip_to_mcp_distance = find_distance(pip_landmark, mcp_landmark)

        # A simple approach: if the distance from tip to PIP is greater than from PIP to MCP, consider the finger extended.
        if tip_to_pip_distance > pip_to_mcp_distance:
            nbr_fingers_up += 1

    # Special case for the thumb, comparing x-coordinates because the thumb opens sideways
    thumb_tip = hand_landmarks.landmark[4]
    thumb_mcp = hand_landmarks.landmark[1]
    if thumb_tip.x > thumb_mcp.x:  # This assumes a right hand, invert the comparison for the left hand
        nbr_fingers_up += 1

    return nbr_fingers_up

def is_thumbs_up(hand_landmarks):
    """Logic to detect 'thumbs up' gesture based on landmarks."""
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

    thumb_up = True
    for landmark in hand_landmarks.landmark:
        if landmark is thumb_tip:
            continue
        else:
            # Check if the thumb tip is above the thumb MCP (considering image coordinates).
            if thumb_tip.y > landmark.y:  # Smaller y value means higher in the image.
                thumb_up = False

    return thumb_up and is_hand_closed_except_thumb(hand_landmarks)

def is_thumbs_down(hand_landmarks):
    """Logic to detect 'thumbs down' gesture based on landmarks."""
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

    thumb_down = True
    for landmark in hand_landmarks.landmark:
        if landmark is thumb_tip:
            continue
        else:
            # Check if the thumb tip is above the thumb MCP (considering image coordinates).
            if thumb_tip.y < landmark.y:  # Smaller y value means higher in the image.
                thumb_down = False

    return thumb_down and is_hand_closed_except_thumb(hand_landmarks)

def global_hand_direction(hand_landmarks):
    nbr_fingers_links = 0
    nbr_fingers_right = 0
    nbr_fingers_up = 0
    nbr_fingers_down = 0
    nbr_landmarks_links = 0
    nbr_landmarks_right = 0
    nbr_landmarks_up = 0
    nbr_landmarks_down = 0

    # Checks links direction
    for landmark_id in range(1, 21):
        if (hand_landmarks.landmark[landmark_id].x < hand_landmarks.landmark[0].x):
            nbr_landmarks_links += 1

        if (nbr_landmarks_links == 4):
            nbr_fingers_links += 1

        if (landmark_id % 4 == 0):
            nbr_landmarks_links = 0

    if (nbr_fingers_links == 5):
        return "links"

    # Checks right direction
    for landmark_id in range(1, 21):
        if (hand_landmarks.landmark[landmark_id].x > hand_landmarks.landmark[0].x):
            nbr_landmarks_right += 1

        if (nbr_landmarks_right == 4):
            nbr_fingers_right += 1

        if (landmark_id % 4 == 0):
            nbr_landmarks_right = 0

    if (nbr_fingers_right == 5):
        return "right"

    # Checks upper direction
    for landmark_id in range(1, 21):
        if (hand_landmarks.landmark[landmark_id].y < hand_landmarks.landmark[0].y):
            nbr_landmarks_up += 1

        if (nbr_landmarks_up == 4):
            nbr_fingers_up += 1

        if (landmark_id % 4 == 0):
            nbr_landmarks_up = 0

    if (nbr_fingers_up == 5):
        return "up"

    # Checks downwards direction
    for landmark_id in range(1, 21):
        if (hand_landmarks.landmark[landmark_id].y > hand_landmarks.landmark[0].y):
            nbr_landmarks_down += 1

        if (nbr_landmarks_down == 4):
            nbr_fingers_down += 1

        if (landmark_id % 4 == 0):
            nbr_landmarks_down = 0

    if (nbr_fingers_down == 5):
        return "down"

# Starts capturing video from the webcam.
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flips the image horizontally for a mirror effect
    image = cv2.flip(image, 1)

    # Converts the image from BGR color (which OpenCV uses) to RGB color.
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to pass by reference.
    image.flags.writeable = False
    results = hands.process(image)

    # Draws the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Checks for "thumbs up" gesture.
            if is_thumbs_up(hand_landmarks):
                print("Thumbs Up detected!")

            # Checks for "thumbs down" gesture.
            if is_thumbs_down(hand_landmarks):
                print("Thumbs Down detected!")

            # Counts extended fingers
            nbr_extended_fingers = count_extended_fingers(hand_landmarks)
            print(nbr_extended_fingers)

            # Checks hand's global direction
            hand_global_direction = global_hand_direction(hand_landmarks)
            print(hand_global_direction)

    # Displays the resulting image.
    cv2.imshow('Hand Tracking', image)
    if cv2.waitKey(5) & 0xFF == 27:  # Press 'ESC' to exit.
        break

# Releases resources
hands.close()
cap.release()
cv2.destroyAllWindows()
