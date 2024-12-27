import cv2
import numpy as np
import time
from threading import Thread, Lock
import io

class MockPiCamera:
    def __init__(self):
        self.resolution = (640, 480)
        self.framerate = 30

    def capture(self, output, format='rgb', use_video_port=False):
        # Generate a test pattern
        img = np.zeros((self.resolution[1], self.resolution[0], 3), dtype=np.uint8)

        # Create a simple test pattern
        cv2.putText(img, 'Camera Simulation', (50, 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Draw some shapes
        cv2.rectangle(img, (100, 100), (200, 200), (0, 255, 0), 2)
        cv2.circle(img, (400, 240), 50, (0, 0, 255), 2)

        # Add timestamp
        cv2.putText(img, time.strftime("%Y-%m-%d %H:%M:%S"),
                   (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Store the image in the output's array attribute
        if hasattr(output, 'array'):
            output.array = img.copy()

    def close(self):
        pass

class MockPiRGBArray:
    def __init__(self, camera):
        self.camera = camera
        self.array = np.zeros((camera.resolution[1], camera.resolution[0], 3), dtype=np.uint8)

    def truncate(self, size=0):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass