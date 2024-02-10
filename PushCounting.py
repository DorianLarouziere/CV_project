import cv2
import PoseModule as pm
import sys
import numpy as np

def main():
    detector = pm.poseDetector()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error reading video file")
        sys.exit()

    count = 0
    direction = "down"
    isFormCorrect = False
    feedback = "Fix Form"

    width = cap.get(3)
    height = cap.get(4)

    while cap.isOpened():
        success, frame = cap.read()
        if success:

            detector.findPose(frame)
            detector.findKeyPoints(frame)
            elbow_angle = detector.findAngle(frame, 10, 8, 6)
            shoulder_angle = detector.findAngle(frame, 8, 6, 12)
            hip_angle = detector.findAngle(frame, 6, 12, 14)

            percentage_of_success_pushup = np.interp(elbow_angle, (90, 160), (0, 100))
            bar_progress = np.interp(elbow_angle, (90, 160), (380, 50))

            if elbow_angle > 160 & shoulder_angle > 40 & hip_angle > 160:
                isFormCorrect = True

            if isFormCorrect:
                if percentage_of_success_pushup == 0:
                    if elbow_angle <= 90 & hip_angle > 160:
                        feedback = "Up"
                        if direction == "down":
                            count += 0.5
                            direction = "up"
                    else: 
                        feedback = "Fix Form"
                
                if percentage_of_success_pushup == 100:
                    if elbow_angle > 160 & shoulder_angle > 40 & hip_angle > 160:
                        feedback = "Down"
                        if direction == "up":
                            count += 0.5
                            direction = "down"
                    else:
                        feedback = "Fix Form"


            if isFormCorrect:
                cv2.rectangle(frame, (580, 50), (600, 380), (0, 255, 0), 3)
            cv2.rectangle(frame, (580, int(bar_progress)), (600, 380), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, f'{int(percentage_of_success_pushup)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 0, 0), 2)


            #Pushup counter
            cv2.rectangle(frame, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                        (255, 0, 0), 5)
            
            #feedback 
            cv2.rectangle(frame, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
            cv2.putText(frame, feedback, (500, 40 ), cv2.FONT_HERSHEY_PLAIN, 2,
                        (0, 255, 0), 2)

            cv2.imshow("Pushup counter", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()