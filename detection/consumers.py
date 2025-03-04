
# # # detection/consumers.py
# import json
# import cv2
# import asyncio
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .tracker import ObjectCounter
# import torch

# class DetectionConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         self.is_running = False
        
#         # Initialize counter with region points for live video
#         self.region_points = [(10, 200), (1000, 200)]
#         self.counter = ObjectCounter(
#             region=self.region_points,
#             model="yolo11n.engine",
#             classes=[2, 3],  # vehicle classes
#             show_in=True,
#             show_out=True,
#             line_width=2,
#             device="cuda" if torch.cuda.is_available() else "cpu",
#             half=True
#         )

#     async def disconnect(self, close_code):
#         self.is_running = False
#         if hasattr(self, 'cap'):
#             self.cap.release()

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         if message == 'start' and not self.is_running:
#             self.is_running = True
#             asyncio.create_task(self.process_live_video())
#         elif message == 'stop':
#             self.is_running = False

#     async def process_live_video(self):
#         try:
#             # Initialize webcam capture
#             self.cap = cv2.VideoCapture(r"C:\Users\HP\Desktop\VehicleDetection\cctv.mp4")  # Use 0 for default webcam
            
#             # Set webcam resolution for better performance
#             self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#             self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

#             if not self.cap.isOpened():
#                 await self.send(text_data=json.dumps({
#                     'error': 'Failed to open webcam'
#                 }))
#                 return

#             frame_count = 0
#             while self.is_running:
#                 ret, frame = self.cap.read()
#                 if not ret:
#                     break

#                 frame_count += 1
#                 if frame_count % 3 != 0:  # Process every third frame for better performance
#                     continue

#                 # Resize frame for consistent processing
#                 frame = cv2.resize(frame, (800, 400))

#                 # Process frame with counter
#                 processed_frame = self.counter.count(frame)
#                 if frame_count % 2 == 0:  # Send every 2nd processed frame
#                     _, buffer = cv2.imencode('.jpg', processed_frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
#                     await self.send(bytes_data=buffer.tobytes())
                
#                 # Add a small delay to control frame rate
#                 await asyncio.sleep(0.01)

#         except Exception as e:
#             print(f"Error in process_live_video: {str(e)}")
#             await self.send(text_data=json.dumps({
#                 'error': str(e)
#             }))
#         finally:
#             if hasattr(self, 'cap'):
#                 self.cap.release()

#####################################################################################


# import json
# import cv2
# import asyncio
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .tracker import ObjectCounter
# import torch

# class DetectionConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         self.is_running = False
#         self.mouse_x, self.mouse_y = 0, 0  # Initialize mouse coordinates
        
#         # Initialize counter with region points for live video
#         self.region_points = [(0,212), (500, 46)]
#         self.counter = ObjectCounter(
#             region=self.region_points,
#             model="yolo11m.pt",
#             classes=[2, 3, 5, 7],  # vehicle classes
#             show_in=True,
#             show_out=True,
#             line_width=1,
#             device="cuda" if torch.cuda.is_available() else "cpu",
#             half=True
#         )

#     async def disconnect(self, close_code):
#         self.is_running = False
#         if hasattr(self, 'cap'):
#             self.cap.release()

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         if message == 'start' and not self.is_running:
#             self.is_running = True
#             asyncio.create_task(self.process_live_video())
#         elif message == 'stop':
#             self.is_running = False

#     def mouse_callback(self, event, x, y, flags, param):
#         """Callback function to capture mouse position."""
#         if event == cv2.EVENT_MOUSEMOVE:
#             self.mouse_x, self.mouse_y = x, y

#     async def process_live_video(self):
#         try:
#             # Initialize webcam capture
#             self.cap = cv2.VideoCapture(r"C:\Users\HP\Desktop\VehicleDetection\cctv.mp4")  # Use 0 for default webcam
#             # self.cap = cv2.VideoCapture(0)# Use 0 for default webcam
            
#             # Set webcam resolution for better performance
#             self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#             self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

#             if not self.cap.isOpened():
#                 await self.send(text_data=json.dumps({
#                     'error': 'Failed to open webcam'
#                 }))
#                 return

#             frame_count = 0
#             # cv2.namedWindow("Live Stream")  # Create a window to display video
#             # cv2.setMouseCallback("Live Stream", self.mouse_callback)  # Track mouse movement

#             while self.is_running:
#                 ret, frame = self.cap.read()
#                 if not ret:
#                     break

#                 frame_count += 1
#                 if frame_count % 2 != 0:  # Process every third frame for better performance
#                     continue

#                 # Resize frame for consistent processing
#                 frame = cv2.resize(frame, (800, 400))

#                 # Process frame with counter
#                 processed_frame = self.counter.count(frame)

#                 # # Draw mouse position on the frame
#                 # cv2.putText(
#                 #     processed_frame,
#                 #     f"Mouse: ({self.mouse_x}, {self.mouse_y})",
#                 #     (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
#                 # )

#                 if frame_count %2 == 0:  # Send every 2nd processed frame
#                     _, buffer = cv2.imencode('.jpg', processed_frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
#                     await self.send(bytes_data=buffer.tobytes())

#                 # Display video with mouse tracking
#                 # cv2.imshow("Live Stream", processed_frame)
#                 # if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
#                 #     break

#                 # Add a small delay to control frame rate
#                 await asyncio.sleep(0.01)

#         except Exception as e:
#             print(f"Error in process_live_video: {str(e)}")
#             await self.send(text_data=json.dumps({
#                 'error': str(e)
#             }))
#         finally:
#             if hasattr(self, 'cap'):
#                 self.cap.release()
#             cv2.destroyAllWindows()

######################################################

# detection/consumers.py
import json
import cv2
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .tracker import ObjectCounter
from .video_feed import video_feed
import torch

class DetectionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.is_running = False
        self.consumer_id = id(self)  # Unique ID for this consumer instance
        
        # Initialize counter with region points for live video
        self.region_points = [(0, 212), (500, 46)]
        self.counter = ObjectCounter(
            region=self.region_points,
            model="yolo11m.pt",
            classes=[2, 3, 5, 7],  # vehicle classes: car, motorcycle, bus, truck
            show_in=True,
            show_out=True,
            line_width=1,
            device="cuda" if torch.cuda.is_available() else "cpu",
            half=True
        )

    async def disconnect(self, close_code):
        self.is_running = False
        video_feed.unregister_listener(self.consumer_id, self.process_frame)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if message == 'start' and not self.is_running:
            self.is_running = True
            video_feed.register_listener(self.consumer_id, self.process_frame)
        elif message == 'stop':
            self.is_running = False
            video_feed.unregister_listener(self.consumer_id, self.process_frame)

    async def process_frame(self, frame):
        """Process and send frame to the client."""
        try:
            if not self.is_running:
                return

            # Process frame with counter
            processed_frame = self.counter.count(frame)

            # Encode and send frame
            _, buffer = cv2.imencode('.jpg', processed_frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
            await self.send(bytes_data=buffer.tobytes())

        except Exception as e:
            print(f"Error in process_frame: {str(e)}")
            await self.send(text_data=json.dumps({'error': str(e)}))