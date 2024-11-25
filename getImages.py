import cv2

# Initialize video capture from the default camera (0)
cap = cv2.VideoCapture(0)

num = 0  # Counter for saved images

while cap.isOpened():
    # Read a frame from the camera
    ret, img = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    img = cv2.flip(img, 1)  # Flip the image horizontally for a mirror effect

    # Wait for a key press for 5 ms
    k = cv2.waitKey(5)

    if k == 27:  # Exit on 'Esc' key
        break
    elif k == ord('s'):  # Save the image on 's' key press
        cv2.imwrite('images/image_' + str(num) + '.png', img)  # Save the image
        print("Image saved!")
        num += 1  # Increment the image counter

    # Display the captured image
    cv2.imshow('Img', img)

# Release the camera and destroy all windows before termination
cap.release()
cv2.destroyAllWindows()
