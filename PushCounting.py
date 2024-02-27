# Import necessary libraries
import cv2
import PoseModule as pm
import sys
import numpy as np

# Main function
def main():
    # Initialize pose detector
    detector = pm.poseDetector()
    # Capture video from default camera
    cap = cv2.VideoCapture(0)

    # Check if the video capture is successful
    if not cap.isOpened():
        print("Error reading video file")
        sys.exit()

    # Initialize variables
    count = 0
    direction = "down"
    isFormCorrect = False
    feedback = "Fix Form"

    # Main loop for processing video frames
    while cap.isOpened():
        success, frame = cap.read()
        if success:
            # Find pose and keypoints in the frame
            detector.findPose(frame)
            detector.findKeyPoints(frame)

            # Calculate angles at various joints, for the elbow, shoulder and hip
            elbow_angle = detector.findAngle(frame, 10, 8, 6)
            shoulder_angle = detector.findAngle(frame, 8, 6, 12)
            hip_angle = detector.findAngle(frame, 6, 12, 14)

            # Interpolate the angle of the elbow to determine the percentage of success of a pushup
            percentage_of_success_pushup = np.interp(elbow_angle, (90, 160), (0, 100))

            # Check if the form of the pushup is correct
            if elbow_angle > 160 and shoulder_angle > 40 and hip_angle > 160:
                isFormCorrect = True

            if isFormCorrect:
                if percentage_of_success_pushup == 0:
                    if elbow_angle <= 90 and hip_angle > 160:
                        feedback = "Up"
                        if direction == "down":
                            count += 0.5
                            direction = "up"
                    else: 
                        feedback = "Fix Form"
                
                if percentage_of_success_pushup == 100:
                    if elbow_angle > 160 and shoulder_angle > 40 and hip_angle > 160:
                        feedback = "Down"
                        if direction == "up":
                            count += 0.5
                            direction = "down"
                    else:
                        feedback = "Fix Form"

            if isFormCorrect:
                cv2.rectangle(frame, (580, 50), (600, 380), (0, 255, 0), 3)

            # Draw pushup counter
            cv2.rectangle(frame, (0, 380), (100, 480), (255, 255, 255), cv2.FILLED)
            cv2.putText(frame, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5, (26, 7, 109), 5)
            
            # Draw feedback message
            cv2.rectangle(frame, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
            cv2.putText(frame, feedback, (500, 40 ), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

            # Display the frame
            cv2.imshow("Pushup counter", frame)
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break

    # Release the camera and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Check if the script is being run directly
if __name__ == "__main__":
    # Call the main function
    main()