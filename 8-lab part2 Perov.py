import cv2
import numpy as np


marker_image = cv2.imread("marker.jpg", cv2.IMREAD_GRAYSCALE)
fly_image = cv2.imread("fly64.png", cv2.IMREAD_COLOR)
camera = cv2.VideoCapture(0)
detector = cv2.ORB_create()
matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

keypoints_marker, descriptors_marker = detector.detectAndCompute(marker_image, None)

marker_center = (int(len(marker_image[0]) / 2), int(len(marker_image) / 2))

while True:
    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    keypoints_frame, descriptors_frame = detector.detectAndCompute(gray, None)
    matches = matcher.match(descriptors_marker, descriptors_frame)
    matches = sorted(matches, key=lambda x: x.distance)
    matched_frame = cv2.drawMatches(marker_image, keypoints_marker, frame, keypoints_frame, matches[:10], None)
    cv2.line(matched_frame, (marker_center[0], 0), (marker_center[0], len(matched_frame)), (0, 255, 0), 2)
    cv2.line(matched_frame, (0, marker_center[1]), (len(matched_frame[0]), marker_center[1]), (0, 255, 0), 2)
    fly_center = (marker_center[0] - int(fly_image.shape[1] / 2), marker_center[1] - int(fly_image.shape[0] / 2))
    fly_h, fly_w = fly_image.shape[:2]
    for c in range(3):
        matched_frame[fly_center[1]:fly_center[1] + fly_h, fly_center[0]:fly_center[0] + fly_w, c] = fly_image[:, :,c] * (fly_image[:,:,3] / 255.0) + matched_frame[fly_center[1]:fly_center[1] + fly_h,fly_center[0]:fly_center[0] + fly_w, c] * (1.0 - fly_image[:,:,3] / 255.0)
        cv2.imshow("Matched Frame", matched_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


camera.release()
cv2.destroyAllWindows()