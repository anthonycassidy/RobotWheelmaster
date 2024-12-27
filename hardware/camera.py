import cv2
import io
import logging
from threading import Thread, Lock
from .mock_camera import MockPiCamera, MockPiRGBArray

class Camera:
    def __init__(self):
        self.frame = None
        self.lock = Lock()
        self.camera = MockPiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 30
        logging.info("Camera initialized with mock implementation")

        # Start background thread
        self.thread = Thread(target=self._capture_loop)
        self.thread.daemon = True
        self.thread.start()

    def _capture_loop(self):
        stream = MockPiRGBArray(self.camera)
        while True:
            try:
                self.camera.capture(stream, format='bgr', use_video_port=True)
                with self.lock:
                    # Convert frame to JPEG
                    _, buffer = cv2.imencode('.jpg', stream.array)
                    self.frame = buffer.tobytes()
                stream.truncate(0)
            except Exception as e:
                logging.error(f"Camera capture error: {str(e)}")
                continue

    def get_frame(self):
        with self.lock:
            return self.frame

    def __del__(self):
        self.camera.close()