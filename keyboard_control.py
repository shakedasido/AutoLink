import keyboard
import numpy as np
import cv2
import time

# Initialize a blank image for the motor display
motorsImg = np.zeros((500, 600, 3), dtype=np.uint8)

# Motor speed variables
lm, rm = 0, 0
time0 = time.time()
time1 = time.time()
time2 = time.time()
time3 = time.time()

# Control variables
extra1 = 0
extra2 = 0
latch = False
fsa = 60  # forward straight acceleration
bsa = 30  # backward straight acceleration
ta = 60  # turning acceleration
fmt = 30  # forward mixed turning acceleration

# Speed limits
up_forward_limit = 40
up_backward_limit = 35
up_forward_turn_limit = 55
turnMotorLimit = 25


def motors(Lm, Rm, Latch, up_arm, down_arm, l_turn, r_turn, back_lm, back_rm):
    """
       Visualize motor states and controls on a blank image.

       Args:
           Lm (int): Speed of the left motor (0-100).
           Rm (int): Speed of the right motor (0-100).
           Latch (int): Latch status (0/1).
           up_arm (int): Status for raising the arm (0/1).
           down_arm (int): Status for lowering the arm (0/1).
           l_turn (int): Status for left turning (0/1).
           r_turn (int): Status for right turning (0/1).
           back_lm (int): Backward motion status for left motor (0/1).
           back_rm (int): Backward motion status for right motor (0/1).
    """

    motorsImg.fill(0)  # Clear the image

    font = cv2.FONT_HERSHEY_SIMPLEX

    # draw motor speed rectangles
    cv2.rectangle(motorsImg, (410, 480), (460, (480 - int((Lm / 100) * 450))), (0, 180, 120), -1)
    cv2.rectangle(motorsImg, (470, 480), (520, (480 - int((Rm / 100) * 450))), (0, 180, 120), -1)

    # draw additional indicators for turning and direction
    cv2.rectangle(motorsImg, (540, 480), (580, (480 - int(abs(((Rm - Lm) / 100) * 450)))), (255, 100, 0), -1)
    if (back_rm and not back_lm) or (back_lm and not back_rm):
        cv2.rectangle(motorsImg, (540, 480), (580, (480 - int(((Lm + Rm) / 100) * 450))), (255, 100, 0), -1)

    cv2.rectangle(motorsImg, (400, 480), (590, 5), (200, 200, 200), 4)

    # Draw control indicators
    cv2.circle(motorsImg, (120, 80), 15, (200, 200, 200), 3)
    cv2.circle(motorsImg, (260, 80), 15, (200, 200, 200), 3)

    if back_lm and back_rm:
        cv2.circle(motorsImg, (260, 80), 13, (0, 0, 255), -1)
    elif Lm != 0 or Rm != 0:
        cv2.circle(motorsImg, (120, 80), 13, (0, 0, 255), -1)

    # Add text labels and lines for visual guidance
    cv2.putText(motorsImg, "forward", (60, 130), font, 1, (200, 0, 255), 2)
    cv2.putText(motorsImg, "backward", (200, 130), font, 1, (200, 0, 255), 2)
    cv2.line(motorsImg, (0, 145), (400, 145), (200, 200, 200), 4)

    # Draw turning arm direction indicators
    cv2.circle(motorsImg, (120, 180), 15, (200, 200, 200), 3)
    cv2.circle(motorsImg, (260, 180), 15, (200, 200, 200), 3)
    if l_turn:
        cv2.circle(motorsImg, (120, 180), 13, (0, 0, 255), -1)
    elif r_turn:
        cv2.circle(motorsImg, (260, 180), 13, (0, 0, 255), -1)

    # Display arm control labels
    cv2.putText(motorsImg, "L turn", (70, 230), font, 1, (200, 0, 255), 2)
    cv2.putText(motorsImg, "R turn", (215, 230), font, 1, (200, 0, 255), 2)
    cv2.line(motorsImg, (0, 245), (400, 245), (200, 200, 200), 4)

    # Draw arm control indicators
    cv2.circle(motorsImg, (120, 280), 15, (200, 200, 200), 3)
    cv2.circle(motorsImg, (260, 280), 15, (200, 200, 200), 3)
    if up_arm:
        cv2.circle(motorsImg, (120, 280), 13, (0, 0, 255), -1)
    elif down_arm:
        cv2.circle(motorsImg, (260, 280), 13, (0, 0, 255), -1)

    # Display latch control labels
    cv2.putText(motorsImg, "up_arm", (50, 330), font, 1, (200, 0, 255), 2)
    cv2.putText(motorsImg, "down_arm", (200, 330), font, 1, (200, 0, 255), 2)
    cv2.line(motorsImg, (0, 345), (400, 345), (200, 200, 200), 4)

    # Draw latch indicators
    cv2.circle(motorsImg, (120, 380), 15, (200, 200, 200), 3)
    cv2.circle(motorsImg, (260, 380), 15, (200, 200, 200), 3)
    if Latch:
        cv2.circle(motorsImg, (120, 380), 13, (0, 255, 0), -1)
    else:
        cv2.circle(motorsImg, (260, 380), 13, (0, 0, 255), -1)

    # Display latch status labels
    cv2.putText(motorsImg, "latch_on", (45, 430), font, 1, (200, 0, 255), 2)
    cv2.putText(motorsImg, "latch_off", (200, 430), font, 1, (200, 0, 255), 2)
    cv2.line(motorsImg, (0, 480), (400, 480), (200, 200, 200), 4)

    # Draw borders
    cv2.line(motorsImg, (185, 5), (185, 480), (200, 200, 200), 1)
    cv2.line(motorsImg, (0, 5), (0, 480), (200, 200, 200), 4)
    cv2.line(motorsImg, (0, 5), (400, 5), (200, 200, 200), 4)

    cv2.waitKey(1)  # Wait for a short period
    cv2.imshow("robot control", motorsImg)  # Display the control window


def keyboard_reader():
    """
        Read keyboard inputs to control motors and other actions.

        Returns:
            lm (int): Speed of the left motor.
            rm (int): Speed of the right motor.
            latch (bool): Latch status.
            up_arm (bool): Status for raising the arm.
            down_arm (bool): Status for lowering the arm.
            l_turn (bool/int): Status for left turning (0/1).
            r_turn (bool/int): Status for right turning (0/1).
            back_lm (bool): Backward motion status for left motor.
            back_rm (bool): Backward motion status for right motor.
            disconnect (bool): Disconnect status.
    """
    global lm, rm, time0, time1, time2, time3, extra1, extra2, latch
    up_arm = 0
    down_arm = 0
    l_turn = 0
    r_turn = 0
    back_lm = 0
    back_rm = 0
    disconnect = False
    emergency_stop = False
    nothing = 1

    # Check for Emergency Stop
    if keyboard.is_pressed('esc'):  # Emergency Stop key
        emergency_stop = True
        return lm, rm, latch, up_arm, down_arm, back_lm, back_rm, disconnect, emergency_stop

    # Control logic for left, right, up, and down movements
    if keyboard.is_pressed('left') and not keyboard.is_pressed('up') and not keyboard.is_pressed('down'):
        l_turn = True
        back_lm = 1
        nothing = 0
        rm = 10
        lm = 10

    if keyboard.is_pressed('right') and not keyboard.is_pressed('up') and not keyboard.is_pressed('down'):
        r_turn = True
        back_rm = 1
        nothing = 0
        rm = 10
        lm = 10

    if keyboard.is_pressed('up') and not keyboard.is_pressed('left') and not keyboard.is_pressed('right'):
        nothing = 0
        time1 = time.time()
        rm = extra1 + int((time1 - time0) * fsa)
        lm = rm
        rm = max(0, min(rm, up_forward_limit))
        lm = max(0, min(lm, up_forward_limit))
    elif not keyboard.is_pressed('down'):
        time0 = time.time()

    if keyboard.is_pressed('up + right'):
        r_turn = 1
        nothing = 0
        time2 = time.time()
        if rm < turnMotorLimit:
            lm = int(extra2 + (time2 - time3) * fmt)
        elif lm > turnMotorLimit:
            rm = int(extra2 - (time2 - time3) * fmt)
        rm = max(0, min(rm, up_forward_turn_limit))
        lm = max(0, min(lm, up_forward_turn_limit))
        extra1 = lm
    elif not keyboard.is_pressed('up + left') and not keyboard.is_pressed('down'):
        extra2 = rm
        time3 = time.time()

    if keyboard.is_pressed('up + left'):
        l_turn = 1
        nothing = 0
        time2 = time.time()
        if lm < turnMotorLimit:
            rm = int(extra2 + (time2 - time3) * fmt)
        elif rm > turnMotorLimit:
            lm = int(extra2 - (time2 - time3) * fmt)
        rm = max(0, min(rm, up_forward_turn_limit))
        lm = max(0, min(lm, up_forward_turn_limit))
        extra1 = rm
    elif not keyboard.is_pressed('up + right') and not keyboard.is_pressed('down'):
        extra2 = lm
        time3 = time.time()

    if keyboard.is_pressed('down'):
        back_lm = 1
        back_rm = 1
        nothing = 0
        time1 = time.time()
        rm = extra1 + int((time1 - time0) * bsa)
        lm = rm
        if keyboard.is_pressed('left'):
            l_turn = 1
            back_rm = 0
            rm = 5
        elif keyboard.is_pressed('right'):
            r_turn = 1
            back_lm = 0
            rm = 5
        rm = max(0, min(rm, up_backward_limit))
        lm = max(0, min(lm, up_backward_limit))

    elif not keyboard.is_pressed('up'):
        time0 = time.time()

    # U/Y - tests only: designed for the developer/tester tests.
    if keyboard.is_pressed('u') or keyboard.is_pressed('U'):
        up_arm = 1

    elif keyboard.is_pressed('y') or keyboard.is_pressed('Y'):
        down_arm = 1

    # L - tests only: designed for the developer/tester tests.
    if keyboard.is_pressed('l') or keyboard.is_pressed('L'):
        latch = 1 - latch  # Toggle latch status
        time.sleep(0.4)  # debounce delay

    elif keyboard.is_pressed('d') or keyboard.is_pressed('D'):
        disconnect = True  # set disconnect flag

    # uf no keys pressed, stop motors
    if nothing == 1:
        rm = 0
        lm = 0
        extra1 = 0

    # Update motor visuals
    motors(lm, rm, latch, up_arm, down_arm, l_turn, r_turn, back_lm, back_rm)
    return lm, rm, latch, up_arm, down_arm, back_lm, back_rm, disconnect, emergency_stop


# cleanup openCV windows
cv2.destroyAllWindows()
