import cv2 as cv
import numpy as np
import math

# Initialize a blank image for the mapping and robot display
pathImg = np.zeros((1200, 1800, 3), dtype=np.uint8)  # graph image dimensions
x0, y0 = int(pathImg.shape[1] / 2), pathImg.shape[0]  # center coordinates
w, h = 800, 700  # the 'pathImg' really bigger then the showing image, the showing image size is w and h
cameraPos = (x0, y0 - 110)  # camera position offset
robImg = cv.imread("robot.png")  # load and resize robot image
robImg = cv.resize(robImg, (0, 0), fx=0.2, fy=0.15)


def blankImg():
    """
        Create a blank image with a grid, robot image, and frame borders.

        Returns:
            np.ndarray: The generated blank image.
    """
    pathImg = np.zeros((1200, 1800, 3), dtype=np.uint8)

    # green grid
    for i in range(0, pathImg.shape[1], 20):
        cv.line(pathImg, (i, 0), (i, pathImg.shape[1]), (0, 50, 0), 1)
    for i in range(0, pathImg.shape[0], 20):
        cv.line(pathImg, (0, i), (pathImg.shape[1], i), (0, 50, 0), 1)

    # place the robot image on the grid
    pathImg[(y0 - robImg.shape[0]):y0, (x0 - int(robImg.shape[1] / 2)): (x0 - int(robImg.shape[1] / 2)
                                                                         + robImg.shape[1])] = robImg

    # draw grey frame borders
    greyColor = (100, 100, 100)
    for i in range(0, pathImg.shape[0], 100):
        cv.line(pathImg, (0, i), (int((pathImg.shape[1] - w) / 2 + 10), i), greyColor, 4)
        cv.line(pathImg, (int(pathImg.shape[1] - ((pathImg.shape[1] - w) / 2 + 10)), i), (pathImg.shape[1], i),
                greyColor, 2)
    for i in range(0, pathImg.shape[1], 100):
        cv.line(pathImg, (i, 0), (i, (pathImg.shape[0] - h + 10)), greyColor, 2)
        cv.line(pathImg, (i, (pathImg.shape[0] - 10)), (i, pathImg.shape[0]), greyColor, 2)

    # it draws the outer rectangle for the display
    cv.rectangle(pathImg, (int((pathImg.shape[1] - w) / 2), (pathImg.shape[0] - h)),
                 (int(pathImg.shape[1] - ((pathImg.shape[1] - w) / 2)), pathImg.shape[0]), greyColor, 5)

    # draw the camera position
    cv.circle(pathImg, cameraPos, 4, (0, 200, 0), -1)

    # now it crops the image to the display size
    pathImg = pathImg[(y0 - h):y0, (x0 - int(w / 2)):(x0 + int(w / 2))]
    return pathImg


def mapping_image(wheelX, wheelY, wheelAngle):
    """
        Map the robot's position and orientation based on wheel data.

        Args:
            wheelX (float): X position of the wheel.
            wheelY (float): Y position of the wheel.
            wheelAngle (float): Orientation angle of the wheel.

        Returns:
            tuple: (pathImg, goodPos, turnRad, x1)
                - pathImg (np.ndarray): The updated mapping image.
                - goodPos (bool): Indicates if the position is valid for connecting.
                - turnRad (int): Turning radius.
                - x1 (float): X displacement from the camera position.
    """
    goodPos = False
    pathImg = np.zeros((1200, 1800, 3), dtype=np.uint8)  # create a new blank image
    pathImg[(y0 - h):y0, (x0 - int(w / 2)):(x0 + int(w / 2))] = blankImg()

    # load and position the wheelchair image
    wheelImg = cv.imread("wheel_chair.png")
    # wheelImg = cv.resize(wheelImg, (0, 0), fx=0.6, fy=0.6)
    wheelPos = (int(x0 + wheelX * 4.5), int(y0 - 110 - wheelY * 4.5))
    height, width = wheelImg.shape[:2]
    centerX, centerY = (width // 2, height // 2)

    # rotate the wheelchair image
    M = cv.getRotationMatrix2D((centerX, centerY + 50), wheelAngle, 0.5)
    wheelImg = cv.warpAffine(wheelImg, M, (width, height))

    # it places the wheelchair image if it's within bounds
    if (500 < wheelPos[0] < 1300) and (500 < wheelPos[1] < 1100):
        pathImg[(wheelPos[1] - int(wheelImg.shape[0] * 0.62)): (
                wheelPos[1] - int(wheelImg.shape[0] * 0.62) + wheelImg.shape[0]), (wheelPos[0]
                                                                                   - int(wheelImg.shape[1] / 2)):
                                                                                  (wheelPos[0] - int(wheelImg.shape[1] /
                                                                                                     2) +
                                                                                   wheelImg.shape[1])] = wheelImg

    # Draw grid lines
    for i in range(0, pathImg.shape[1], 20):
        cv.line(pathImg, (i, 0), (i, pathImg.shape[1]), (0, 50, 0), 1)

    for i in range(0, pathImg.shape[0], 20):
        cv.line(pathImg, (0, i), (pathImg.shape[1], i), (0, 50, 0), 1)

    # it calculates the turning radius and angle
    theta = math.radians(wheelAngle)

    dx = int(50 * math.cos(theta))
    dy = int(50 * math.sin(theta))
    cv.line(pathImg, (wheelPos[0] - dx, wheelPos[1] + dy),
            (wheelPos[0] + dx, wheelPos[1] - dy),
            (0, 255, 0), 3)

    # Place the robot image on top of the mapping image
    pathImg[(y0 - robImg.shape[0]):y0, (x0 - int(robImg.shape[1] / 2)):
                                       (x0 - int(robImg.shape[1] / 2) + robImg.shape[1])] = robImg

    # now it draws grey frame borders
    greyColor = (100, 100, 100)
    for i in range(0, pathImg.shape[0], 100):
        cv.line(pathImg, (0, i), (int((pathImg.shape[1] - w) / 2 + 10), i), greyColor, 4)
        cv.line(pathImg, (int(pathImg.shape[1] - ((pathImg.shape[1] - w) / 2 + 10)), i),
                (pathImg.shape[1], i), greyColor, 2)

    for i in range(0, pathImg.shape[1], 100):
        cv.line(pathImg, (i, 0), (i, (pathImg.shape[0] - h + 10)), greyColor, 2)
        cv.line(pathImg, (i, (pathImg.shape[0] - 10)), (i, pathImg.shape[0]), greyColor, 2)

    # Draw the outer rectangle for the display
    cv.rectangle(pathImg, (int((pathImg.shape[1] - w) / 2), (pathImg.shape[0] - h)),
                 (int(pathImg.shape[1] - ((pathImg.shape[1] - w) / 2)), pathImg.shape[0]),
                 greyColor, 5)

    # calculate and draw the turning arc
    dx2 = int(100 * math.sin(theta))
    dy2 = int(100 * math.cos(theta))
    middlePoint = (wheelPos[0] + dx2, wheelPos[1] + dy2)
    cv.line(pathImg, cameraPos, middlePoint, (255, 0, 0), 1)
    cv.line(pathImg, wheelPos, middlePoint, (255, 0, 0), 1)
    cv.circle(pathImg, cameraPos, 6, (0, 0, 255), -1)
    cv.circle(pathImg, middlePoint, 6, (0, 0, 255), -1)
    cv.circle(pathImg, wheelPos, 6, (0, 0, 255), -1)

    # now it calculates displacement and turning radius
    x1 = middlePoint[0] - cameraPos[0]
    y1 = middlePoint[1] - cameraPos[1]

    x1 = 1 if x1 == 0 else x1  # prevent division by zero

    Bangle = math.atan(y1 / x1)  #
    d1 = math.sqrt(x1 ** 2 + y1 ** 2)
    turnRad = int((d1 / (2 * math.cos(Bangle))))

    # determine if the position is good based on the angles
    if Bangle > 0:
        if abs(180 - 2 * (Bangle * 180 / math.pi) - wheelAngle) < 45:
            goodPos = True
            arcColor = (0, 255, 0)  # green if position is good
        else:
            arcColor = (0, 0, 255)  # red if position is not good
        cv.ellipse(pathImg, ((cameraPos[0] - turnRad), cameraPos[1]), (turnRad, turnRad), 0, 0,
                   -(180 - 2 * (abs(Bangle) * 180 / math.pi)), arcColor, 4)

    else:
        if abs(180 + 2 * (Bangle * 180 / math.pi) + wheelAngle) < 45:
            goodPos = True
            arcColor = (0, 255, 0)
        else:
            arcColor = (0, 0, 255)
        cv.ellipse(pathImg, ((cameraPos[0] + turnRad), cameraPos[1]), (turnRad, turnRad), 0,
                   180, (360 - 2 * (abs(Bangle) * 180 / math.pi)), arcColor, 4)

    # crop the image to the display size
    pathImg = pathImg[(y0 - h):y0, (x0 - int(w / 2)):(x0 + int(w / 2))]
    return pathImg, goodPos, turnRad, x1
