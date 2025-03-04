# detection/video_feed.py
import cv2
import asyncio
from collections import defaultdict

class VideoFeedManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VideoFeedManager, cls).__new__(cls)
            cls._instance.cap = cv2.VideoCapture(r"C:\Users\HP\Desktop\VehicleDetection\cctv.mp4")  # Adjust path as needed
            cls._instance.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cls._instance.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            cls._instance.listeners = defaultdict(list)  # {consumer_id: [callback]}
            cls._instance.is_running = False
            cls._instance.frame = None
            cls._instance.loop = None  # Will be set later
            cls._instance.task = None  # Store the task reference
        return cls._instance

    async def _run(self):
        self.is_running = True
        frame_count = 0
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                break
            frame_count += 1
            if frame_count % 2 == 0:  # Process every other frame
                self.frame = cv2.resize(frame, (800, 400))
                # Notify all listeners
                for consumer_id, callbacks in self.listeners.items():
                    for callback in callbacks:
                        await callback(self.frame)
            await asyncio.sleep(0.01)  # Control frame rate
        self.cap.release()

    def start(self):
        """Start the video feed processing if not already running."""
        if not self.is_running:
            self.loop = asyncio.get_event_loop()
            self.task = self.loop.create_task(self._run())

    def register_listener(self, consumer_id, callback):
        """Register a consumer to receive frames and start the feed if needed."""
        self.listeners[consumer_id].append(callback)
        self.start()  # Start the feed when the first listener registers

    def unregister_listener(self, consumer_id, callback):
        """Unregister a consumer."""
        if consumer_id in self.listeners and callback in self.listeners[consumer_id]:
            self.listeners[consumer_id].remove(callback)
            if not self.listeners[consumer_id]:
                del self.listeners[consumer_id]
        # Stop the feed if no listeners remain
        if not self.listeners and self.is_running:
            self.stop()

    def stop(self):
        """Stop the video feed processing."""
        self.is_running = False
        if self.task:
            self.task.cancel()

# Singleton instance
video_feed = VideoFeedManager()