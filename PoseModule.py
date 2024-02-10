import cv2
import sys
from ultralytics import YOLO
import math

class poseDetector():

    def __init__(self):
        self.model = YOLO("yolov8m-pose.pt")
        self.keyPoints = dict()

    def findPose(self, img):
        self.results = self.model.predict(img, verbose=False)
        return img
    
    def findKeyPoints(self, img, draw = True):
        kptss= self.results[0].keypoints.data
        for kpts in kptss:
            i = 0
            for kpt in kpts:
                self.keyPoints[i] = (int(kpt[0]),int(kpt[1]))
                if(draw):
                    cv2.circle(img, (int(kpt[0]),int(kpt[1])), radius=0, color=(0, 255, 255), thickness=2)
                i+=1
        
    
    def findAngle(self, img, p1, p2, p3, draw = True):
        k1 = self.keyPoints[p1]
        k2 = self.keyPoints[p2]
        k3 = self.keyPoints[p3]
        x1, y1 = k1[0], k1[1]
        x2, y2 = k2[0], k2[1]
        x3, y3 = k3[0], k3[1]
        angle = int(math.degrees(math.atan2(y3-y2, x3-x2) - 
                             math.atan2(y1-y2, x1-x2)))
        
        if angle < 0:
            angle += 360
            if angle > 180:
                angle = 360 - angle
        elif angle > 100:
            angle = 360 - angle

        if(draw):
            cv2.line(img, (x1, y1), (x2, y2), (255,255,255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255,255,255), 3)

            
            cv2.circle(img, (x1, y1), 5, (0,0,255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0,0,255), 2)
            cv2.circle(img, (x2, y2), 5, (0,0,255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0,0,255), 2)
            cv2.circle(img, (x3, y3), 5, (0,0,255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0,0,255), 2)
            
            cv2.putText(img, str(int(angle)), (x2-50, y2+50), 
                        cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)

        return angle
    
def main():
    detector = poseDetector()
    cap = cv2.VideoCapture(0)


    if not cap.isOpened():
        print("Error reading video file")
        sys.exit()

    while cap.isOpened():
        success, frame = cap.read()
        if success:

            detector.findPose(frame)
            detector.findKeyPoints(frame)
            angle = detector.findAngle(frame, 0, 1, 3)
            print(f"angle = {angle}")

            cv2.imshow("YOLOv8 Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()