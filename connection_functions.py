import GPIO_activation
from aruco_detection import aruco_detecting
import mapping_processing
import cv2 as cv
import keyboard_control
import time

# Initialize motor control variables
lm, rm, up_arm, down_arm, back_lm, back_rm = 0, 0, 0, 0, 0, 0


def auto_connection():
    """
    Automatically connects a motorized device to a wheelchair using ArUco marker detection.

    The function captures video frames from the camera, detects ArUco markers,
    and processes the detected information to maneuver the device into position.
    """
    cap = cv.VideoCapture(0)  # Open the camera
    step = 1
    first_step = True
    midle_dis = 45  # Threshold distance to the wheelchair
    min_dis = 20  # Minimum distance for stopping
    min_ang = 4  # Minimum angle in degrees
    motor_speed1 = 90  # Speed for the first motor
    motor_speed2 = 25  # Speed for the second motor
    detection_lost_count = 0  # Counter for lost marker detection
    max_detection_lost = 1000  # Maximum retries for marker detection, adjust it per controller

    while True:
        ret, frame = cap.read()  # Read frame from the camera
        if not ret:
            print("Camera issue detected. Exiting auto_connection.")
            return False  # Fail if the camera is not working

        aruco_image, detection, distance, wheelX, wheelZ, wheelAngle = aruco_detecting(frame)

        if not detection:
            detection_lost_count += 1
            print(f"Marker not detected. Retry {detection_lost_count}/{max_detection_lost}")

            if detection_lost_count >= max_detection_lost:
                print("Marker detection failed. Stopping the process.")
                # Stop all motors or reset process
                GPIO_activation.low_output()
                return False  # Return failure flag
            else:
                # Retry by continuing to look for the marker
                cv.imshow("aruco", frame)
                continue
        else:
            detection_lost_count = 0  # Reset counter when marker is detected

        # Process mapping and connection steps
        map_image, goodPos, turnRad, x1 = mapping_processing.mapping_image(wheelX, wheelZ, wheelAngle)

        if step == 1:
            if first_step:
                print(f'step {step}')
                first_step = False
            # Step 1: Approach the wheelchair
            d = 50  # Half of the distance between the motors
            i = float((turnRad - d) / (turnRad + d))  # Calculate rotation ratio

            # Adjust motor speeds based on the turn ratio. 
            # x1 bigger then 0 means the machine turns right, else left.  <----x1---->
            if x1 > 0:
                lm = motor_speed1
                rm = lm * i
            else:
                rm = motor_speed1
                lm = rm * i

            GPIO_activation.GPIO_activation(lm, rm, 0, 0, 0, 0, 0)

            if distance < midle_dis:
                GPIO_activation.low_output()  # Stop motors
                time.sleep(1)
                step = 2  # Move to next step
                first_step = True

        elif step == 2:
            # Step 2: Adjust angle towards the wheelchair
            if first_step:
                print(f'step {step}')
                first_step = False
            if wheelAngle > 0:
                lm = motor_speed2
                rm = lm
                back_lm = 1
                back_rm = 0
            else:
                lm = motor_speed2
                rm = lm
                back_lm = 0
                back_rm = 1

            GPIO_activation.GPIO_activation(lm, rm, 0, 0, 0, back_lm, back_rm)

            if abs(wheelAngle) < min_ang:
                GPIO_activation.low_output()  # Stop motors
                time.sleep(1)
                step = 3  # Move to next step
                first_step = True

        elif step == 3:
            # Step 3: Move closer to the wheelchair
            if first_step:
                print(f'step {step}')
                first_step = False
            lm = motor_speed2
            rm = lm
            GPIO_activation.GPIO_activation(lm, rm, 0, 0, 0, 0, 0)

            if distance < min_dis:
                GPIO_activation.low_output()  # Stop motors
                time.sleep(1)
                step = 4  # Move to next step
                first_step = True

        elif step == 4:
            # Step 4: Perform final connection
            if first_step:
                print(f'step {step}\n')

            up_arm = 1  # Raise arm to connect
            GPIO_activation.GPIO_activation(0, 0, 0, up_arm, 0, 0, 0)
            time.sleep(3)

            GPIO_activation.low_output()  # Stop all outputs
            time.sleep(1)

            cap.release()  # Release camera
            cv.destroyAllWindows()  # Close OpenCV windows
            return True

        cv.waitKey(1)  # Wait for a key press
        cv.imshow("aruco", aruco_image)  # Show detected ArUco image
        cv.imshow("mapp", map_image)  # Show mapping image


def user_control():
    """
    Provides user control over the motorized device via keyboard input.

    This function continuously reads user inputs and sends corresponding
    activation commands to the motors until a disconnect command is received.
    """
    while True:
        # Read user commands from keyboard
        lm, rm, latch, up_arm, down_arm, back_lm, back_rm, disconnect, emergency_stop = keyboard_control.keyboard_reader()
        if emergency_stop:
            print("Emergency Stop Activated. Halting all operations.")
            GPIO_activation.low_output()  # Stop all GPIO outputs
            cv.destroyAllWindows()  # Close all OpenCV windows
            time.sleep(0.5)  # Small delay to ensure smooth termination
            break  # Exit the loop immediately
        GPIO_activation.GPIO_activation(lm, rm, latch, up_arm, down_arm, back_lm, back_rm)

        if disconnect:
            GPIO_activation.low_output()  # Stop motors
            time.sleep(1)
            cv.destroyAllWindows()  # Close OpenCV windows
            break


def disconnection():
    """
    Handles the disconnection process for the motorized device.

    This function lowers the arm, moves the device backward, and stops all outputs.
    """
    motor_speed2 = 25  # Speed for backward movement

    down_arm = 1  # Lower the arm
    GPIO_activation.GPIO_activation(0, 0, 0, 0, down_arm, 0, 0)
    time.sleep(3)

    GPIO_activation.low_output()  # Stop all outputs
    time.sleep(1)

    # Move backward
    lm = motor_speed2
    rm = lm
    back_lm = 1
    back_rm = 1
    GPIO_activation.GPIO_activation(lm, rm, 0, 0, 0, back_lm, back_rm)
    time.sleep(5)

    GPIO_activation.low_output()  # Stop all outputs
    time.sleep(1)
