# AirBoard: Virtual Writing Board

A real-time computer vision application that allows you to draw on your screen using hand gestures. This project leverages **OpenCV** for image processing and Google's **MediaPipe Tasks API** for robust hand landmark tracking.

## Features

* **Real-time Hand Tracking:** Uses the optimized MediaPipe Hand Landmarker model.
* **Draw Mode:** Raise only your index finger to draw on the canvas.
* **Erase Mode:** Raise your index and middle fingers to act as an eraser.
* **Clear Canvas:** Open your entire hand (5 fingers) to instantly clear the board.
* **Standby Mode:** Close your hand (fist) or lower your index/middle fingers to pause drawing.

## Prerequisites

* Python 3.8+
* Webcam

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/AirBoard.git](https://github.com/YOUR_USERNAME/AirBoard.git)
    cd AirBoard
    ```

2.  **Install the required Python libraries:**
    ```bash
    pip install opencv-python mediapipe numpy
    ```

3.  **Download the MediaPipe Model:**
    This application requires the compiled MediaPipe task model to function. Download the `hand_landmarker.task` file and place it in the root directory of this project.
    * [Download hand_landmarker.task](https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task)
    
    *Or download via terminal:*
    ```bash
    curl -o hand_landmarker.task [https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task](https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task)
    ```

## Usage

1.  Ensure `hand_landmarker.task` is in the same folder as your Python script.
2.  Run the application:
    ```bash
    python main.py
    ```
3.  A window will open displaying your webcam feed. Step back slightly so your hand is clearly visible.
4.  **Controls:**
    *  **Index Finger Up:** Draw
    *  **Index + Middle Fingers Up:** Erase
    *  **All Fingers Up:** Clear Board
    *  **Fist / Other:** Standby
5.  Press **`q`** on your keyboard to exit the application.
