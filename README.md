# Pushup Counter and Form Checker

This program uses pose estimation to count pushups and provide feedback on the form during pushup exercises using YOLOv8 and OpenCV.

## Features

- Counts the number of pushups performed.
- Provides real-time feedback on the form of each pushup.
- Utilizes YOLOv8 for pose estimation.
- Draws keypoints and lines on the detected pose for visual feedback.

## Prerequisites

Before using the program, ensure you have the following installed:

- Python 3.x
- OpenCV
- ultralytics (for YOLOv8)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/DorianLarouziere/CV_project.git
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the program:
 ```
   python3 pushCounting.py
```


3. Perform pushups in front of the camera.
4. Follow the feedback provided on the screen to ensure correct form.
5. The pushup count will be displayed on the screen.

## Configuration

- The YOLOv8 model weights should be named `yolov8m-pose.pt` and placed in the same directory as the script.
