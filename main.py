from aruco_detection import aruco_detecting
import mapping_processing
import connection_functions
import cv2 as cv

# initialize video capture from the default camera
cap = cv.VideoCapture(0)
first_permission = True
first_no_detection = True
first_no_permission = True
while True:
    # read a frame from the camera
    ret, frame = cap.read()

    if not ret:
        print("There is a camera problem")
        break
    key = cv.waitKey(1)  # wait for a short period for key press

    # Detect aruco markers in the frame
    aruco_image, detection, distance, wheelX, wheelZ, wheelAngle = aruco_detecting(frame)

    if detection:
        # process the mapping based on detected marker data
        map_image, goodPos, turnRad, x1 = mapping_processing.mapping_image(wheelX, wheelZ, wheelAngle)

        if goodPos:
            if first_permission:
                print("You got a permission to connect: press 'c' for connection")
                first_permission = False
                first_no_permission = True
                first_no_detection = True
            if key == ord("c") or key == ord("C"):  # Check for user input to connect
                # >>>>>>>>>>>>>  AUTO CONNECTION
                connection_successful = connection_functions.auto_connection()

                if not connection_successful:
                    print("Connection interrupted. Returning to detection step.")
                    # initialize video capture from the default camera
                    first_permission = True
                    first_no_detection = True
                    cap = cv.VideoCapture(0)
                    continue  # Restart the loop to detect and process again

                print("connected , press 'd' for disconnection\n")
                # >>>>>>>>>>>>>  USER CONTROL
                print("user control...")
                connection_functions.user_control()

                # >>>>>>>>>>>>>  DISCONNECTING
                print("disconnecting")
                connection_functions.disconnection()

                # Re-initialize camera after disconnection
                cap = cv.VideoCapture(0)
        else:
            if first_no_permission:
                print("No permission to connect, adjust the wheelchair position ")
                first_no_permission = False
                first_permission = True
                first_no_detection = True

    else:
        # If no detection, show a blank map image
        map_image = mapping_processing.blankImg()
        if first_no_detection:
            print("No detection\n")
            first_no_detection = False
            first_permission = True
            first_no_permission = True

    # display the aruco detection image and the mapped image
    cv.imshow("aruco", aruco_image)
    cv.imshow("mapp", map_image)
    if key == ord("q") or key == ord("Q"):  # exit if 'q' is pressed
        break

# Release the camera and destroy all openCV windows
cap.release()
cv.destroyAllWindows()
