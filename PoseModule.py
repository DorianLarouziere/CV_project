import cv2
import sys
from ultralytics import YOLO
import math

class poseDetector:
    """
    Class for detecting and analyzing poses using YOLOv8 and OpenCV.

    Attributes:
    - model: YOLO model for detecting poses.
    - keyPoints: Dictionary to store keypoints detected by the model.
    """

    def __init__(self):
        """
        Initializes the pose detector object.

        Initializes the YOLO model for pose detection and initializes an empty dictionary
        to store keypoints.
        """
        self.model = YOLO("yolov8m-pose.pt")
        self.keyPoints = dict()

    def findPose(self, img):
        """
        Detects poses in an image using the YOLO model.

        Args:
        - img: Image to detect poses in.

        Returns:
        - img: Image with detected poses.
        """
        self.results = self.model.predict(img, verbose=False)
        return img
    
    def findKeyPoints(self, img, draw=True):
        """
        Finds keypoints in an image.

        Args:
        - img: Image to find keypoints in.
        - draw: Boolean indicating whether to draw keypoints on the image (default is True).
        """
        # Extract keypoints from YOLO results and store in self.keyPoints dictionary
        kptss = self.results[0].keypoints.data
        for kpts in kptss:
            i = 0
            for kpt in kpts:
                self.keyPoints[i] = (int(kpt[0]), int(kpt[1]))
                # Draw keypoints on the image if draw is True
                if draw:
                    cv2.circle(img, (int(kpt[0]), int(kpt[1])), radius=0, color=(0, 255, 255), thickness=2)
                i += 1
        
    
    def findAngle(self, img, p1, p2, p3, draw=True):
        """
        Finds the angle between three keypoints.

        Args:
        - img: Image to draw lines and keypoints on.
        - p1: Index of the first keypoint.
        - p2: Index of the second keypoint.
        - p3: Index of the third keypoint.
        - draw: Boolean indicating whether to draw lines and keypoints on the image (default is True).

        Returns:
        - angle: Angle between the three keypoints.
        """
        # Get coordinates of the keypoints
        k1 = self.keyPoints[p1]
        k2 = self.keyPoints[p2]
        k3 = self.keyPoints[p3]
        x1, y1 = k1[0], k1[1]
        x2, y2 = k2[0], k2[1]
        x3, y3 = k3[0], k3[1]
        # Calculate the angle using arctan2 and convert to degrees
        angle = int(math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2)))
        
        # Normalize angle to be between 0 and 180 degrees
        if angle < 0:
            angle += 360
            if angle > 180:
                angle = 360 - angle
        elif angle > 100:
            angle = 360 - angle

        # Draw lines and keypoints on the image if draw is True
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            
            cv2.circle(img, (x1, y1), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        return angle
