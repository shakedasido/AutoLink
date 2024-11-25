import cv2 as cv
from cv2 import aruco
import numpy as np

# Load calibration data from file
calib_data = np.load("arrays.npz")
cam_mat = calib_data["mtx"]  # Camera matrix
dist_co = calib_data["dist"]  # Distortion coefficients
r_vectors = calib_data["rvecs"]  # Rotation vectors
t_vectors = calib_data["tvecs"]  # Translation vectors

# Initialize variables for marker detection
first_time = True
last_x, last_z, last_angle = 0, 0, 0
last_frame = np.zeros((600, 700, 3), dtype=np.uint8)
output_x, output_z, output_angle = 0, 1000, 0
failCount1 = 0
failCount2 = 0

MARKER_SIZE = 9  # Size of the marker in centimeters
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
param_markers = aruco.DetectorParameters()


def my_estimatePoseSingleMarkers(corners, marker_size, mtx, distortion):
    """
    Estimate the pose of single markers from their detected corners.
    
    Args:
        corners (list): Detected corners of the markers.
        marker_size (float): Size of the marker.
        mtx (ndarray): Camera matrix.
        distortion (ndarray): Distortion coefficients.
        
    Returns:
        list: Rotation vectors for each marker.
        list: Translation vectors for each marker.
        list: Auxiliary data (not used).
    """
    marker_points = np.array([[-marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, -marker_size / 2, 0],
                              [-marker_size / 2, -marker_size / 2, 0]], dtype=np.float32)
    trash = []
    rvecs = []
    tvecs = []

    for c in corners:
        _, R, t = cv.solvePnP(marker_points, c, mtx, distortion, False, cv.SOLVEPNP_IPPE_SQUARE)
        rvecs.append(R)
        tvecs.append(t)
        trash.append(None)  # Placeholder, not used
    return rvecs, tvecs, trash


def aruco_detecting(frame):
    """
    Detect ArUco markers in a given frame and estimate their pose.
    
    Args:
        frame (ndarray): The input image frame to process.

    Returns:
        tuple: Processed frame, detection status, distance to marker, and estimated pose (x, z, angle).
    """
    detection = False
    global first_time, last_x, last_z, last_angle, last_frame, failCount1, failCount2, output_x, output_z, output_angle

    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)  # Convert to grayscale
    detector = aruco.ArucoDetector(marker_dict, param_markers)
    marker_corners, marker_IDs, _ = detector.detectMarkers(gray_frame)

    if marker_corners:
        rVec, tVec, _ = my_estimatePoseSingleMarkers(marker_corners, MARKER_SIZE, cam_mat, dist_co)
        total_markers = range(len(marker_IDs))

        for ids, corners, i in zip(marker_IDs, marker_corners, total_markers):
            # Calculate rotation angles and update output if within error thresholds
            rVec2 = np.array(rVec, dtype=np.float32)
            rotation_matrix, _ = cv.Rodrigues(rVec2[i])
            _, _, _, _, _, _, euler_angles = cv.decomposeProjectionMatrix(
                np.hstack((rotation_matrix, np.zeros((3, 1)))))
            Angle = euler_angles[1]  # Angle around z-axis

            # Define error thresholds for position and angle
            x_z_play = 5  # Allowable x and z error distance
            anPlay = 20  # Allowable angle error

            # Check if the detected marker meets the error thresholds
            if (abs(tVec[i][0][0] - last_x) < x_z_play and abs(tVec[i][2][0] - last_z) < x_z_play and abs(
                    Angle - last_angle) < anPlay) or (failCount2 > 2) or first_time:
                output_z = tVec[i][2][0]
                output_x = tVec[i][0][0]
                output_angle = Angle[0]
                first_time = False
                detection = True
                failCount1 = 0
                failCount2 = 0
                last_x = tVec[i][0][0]
                last_z = tVec[i][2][0]
                last_angle = Angle
                last_frame = frame
                corners = corners.reshape(4, 2).astype(int)

                # Draw on the camera window
                cv.polylines(frame, [corners], True, (0, 255, 255), 4, cv.LINE_AA)

                # Calculate distance to marker
                distance = np.sqrt(np.sum(tVec[i] ** 2))

                # Annotate frame with marker information
                top_right = corners[0].ravel()
                bottom_right = corners[2].ravel()

                cv.putText(frame, f"id: {ids[0]} Dist: {round(distance, 2)}", top_right, cv.FONT_HERSHEY_PLAIN, 1.7,
                           (0, 0, 255), 2, cv.LINE_AA)
                cv.putText(frame, f"angle: {round(Angle[0], 2)}", (top_right[0], top_right[1] + 30),
                           cv.FONT_HERSHEY_PLAIN, 1.7, (0, 0, 255), 2, cv.LINE_AA)
                cv.putText(frame, f"x: {round(tVec[i][0][0], 1)} y: {round(tVec[i][1][0], 1)}", bottom_right,
                           cv.FONT_HERSHEY_PLAIN, 1.6, (0, 0, 255), 2, cv.LINE_AA)
            else:
                distance = 500000
                failCount2 += 1
                frame = last_frame  # Use last valid frame if detection fails

    else:
        distance = 500000
        detection = False
        failCount2 = 0
        failCount1 += 1
        if failCount1 > 10:
            failCount1 = 0
            first_time = True
        elif not first_time:
            detection = True

    # Reset output if no detection
    if not detection:
        output_x, output_z, output_angle = 0, 1000, 0

    return frame, detection, distance, output_x, output_z, output_angle
