import cv2
import sys
from ultralytics import YOLO

model = YOLO("yolov8m-pose.pt") # path to model file

cap = cv2.VideoCapture(0) # path to video file or webcam

keypoints = dict()

if not cap.isOpened():
    print("Error reading video file")
    sys.exit()

while cap.isOpened():
    success, frame = cap.read()
    if success:

        results = model.predict(frame, verbose=False)
        print(f"\n\nresults:{results}")
        kptss=results[0].keypoints.data
        print(f"\nkptss:{kptss}")
        for kpts in kptss:
            i = 0
            for kpt in kpts:
                print(f"\nkpt:{kpt}\n")
                print(f'X : {kpt[0]}, Y : {kpt[1]}, Z : {kpt[2]}')
                keypoints[i] = (int(kpt[0]),int(kpt[1]))
                cv2.circle(frame, (int(kpt[0]),int(kpt[1])), radius=0, color=(0, 255, 255), thickness=2)
                i+=1
        
        cv2.line(frame, keypoints[4], keypoints[2], color=(0, 165, 255), thickness=1)
        cv2.line(frame, keypoints[2], keypoints[0], color=(0, 165, 255), thickness=1)
        cv2.line(frame, keypoints[0], keypoints[1], color=(0, 165, 255), thickness=1)
        cv2.line(frame, keypoints[1], keypoints[3], color=(0, 165, 255), thickness=1)
        cv2.imshow("YOLOv8 Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()