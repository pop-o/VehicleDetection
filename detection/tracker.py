

# import os
# import pandas as pd
# from datetime import datetime
# import numpy as np
# from time import time
# from ultralytics.solutions.solutions import BaseSolution
# from ultralytics.utils.plotting import Annotator, colors

# class ObjectCounter(BaseSolution):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.in_count = 0
#         self.out_count = 0
#         self.counted_ids = []
#         self.classwise_counts = {
#             "Four Wheeler": {"IN": 0, "OUT": 0},
#             "Two Wheeler": {"IN": 0, "OUT": 0}
#         }

#         # Define vehicle class categories
#         self.four_wheeler_classes = {2, 5, 7}  # car, bus, truck
#         self.two_wheeler_classes = {3}  # bicycle, motorcycle

#         self.region_initialized = False
#         self.trkd_ids = []
#         self.trk_pt = {}
#         self.trk_pp = {}

#         # Store IN/OUT times for each vehicle
#         self.in_out_times = {}  

#         # Initialize CSV data storage
#         self.csv_filename = self.get_daily_filename()
#         self.create_csv()

#         # Start time for video processing
#         self.start_time = time()  

#     def get_daily_filename(self):
#         """Generate a filename based on the current date."""
#         current_date = datetime.now().strftime("%Y-%m-%d")
#         return f"vehicle_count_data_{current_date}.csv"

#     def create_csv(self):
#         """Create the CSV file if it doesn't exist."""
#         if not os.path.exists(self.csv_filename):
#             header = ["Track ID", "Vehicle Type", "Action", "Date", "Time"]
#             df = pd.DataFrame(columns=header)
#             df.to_csv(self.csv_filename, index=False)
#             print(f"CSV file created: {self.csv_filename}")

#     def save_label_to_file(self, track_id, vehicle_type, action):
#         """Save the tracking info to CSV."""
#         current_time = datetime.now().strftime("%H:%M:%S")
#         current_date = datetime.now().date()

#         # Prepare data for saving
#         data = {
#             "Track ID": track_id,
#             "Vehicle Type": vehicle_type,
#             "Action": action,
#             "Date": current_date,
#             "Time": current_time
#         }

#         # Append data to CSV
#         df = pd.DataFrame([data])
#         df.to_csv(self.csv_filename, mode='a', header=False, index=False)
#         print(f"Data saved for {vehicle_type} ID {track_id} - {action}")

#     def update_in_out_times(self, track_id, action):
#         """Update entry and exit times dynamically."""
#         timestamp = self.format_time(time() - self.start_time)

#         if track_id not in self.in_out_times:
#             self.in_out_times[track_id] = {"IN": None, "OUT": None}

#         self.in_out_times[track_id][action] = timestamp
#         print(f"Vehicle {track_id} {action} at {timestamp}")

#     def format_time(self, seconds):
#         """Convert seconds to HH:MM:SS format."""
#         return str(datetime.utcfromtimestamp(seconds).strftime('%H:%M:%S'))

#     def get_vehicle_type(self, class_id):
#         """Determine if detected object is Four Wheeler or Two Wheeler."""
#         if class_id in self.four_wheeler_classes:
#             return "Four Wheeler"
#         elif class_id in self.two_wheeler_classes:
#             return "Two Wheeler"
#         return None

#     def count_objects(self, current_centroid, track_id, prev_position, cls):
#         """Count vehicles based on movement across the defined region."""
#         if prev_position is None or track_id in self.counted_ids:
#             return

#         action = None
#         vehicle_type = self.get_vehicle_type(cls)
#         if not vehicle_type:
#             return  # Ignore non-vehicle classes

#         # Check for movement across a counting region
#         if len(self.region) == 2:
#             line = self.LineString(self.region)
#             if line.intersects(self.LineString([prev_position, current_centroid])):
#                 if current_centroid[1] > prev_position[1]:  # Moving downward
#                     self.classwise_counts[vehicle_type]["OUT"] += 1
#                     action = "OUT"
#                 else:  # Moving upward
#                     self.classwise_counts[vehicle_type]["IN"] += 1
#                     action = "IN"

#         elif len(self.region) > 2:
#             polygon = self.Polygon(self.region)
#             if polygon.contains(self.Point(current_centroid)):
#                 if current_centroid[1] > prev_position[1]:  # Moving downward
#                     self.classwise_counts[vehicle_type]["OUT"] += 1
#                     action = "OUT"
#                 else:
#                     self.classwise_counts[vehicle_type]["IN"] += 1
#                     action = "IN"

#         if action:
#             self.save_label_to_file(track_id, vehicle_type, action)
#             self.update_in_out_times(track_id, action)
#             self.counted_ids.append(track_id)

#     def display_counts(self, im0):
#         """Display the counts for Four Wheeler and Two Wheeler."""
#         labels_dict = {
#             key: f"OUT {value['OUT']}  IN {value['IN']}"
#             for key, value in self.classwise_counts.items()
#             if value["OUT"] > 0 or value["IN"] > 0
#         }

#         if labels_dict:
#             self.annotator.display_analytics(im0, labels_dict, (104, 31, 17), (255, 255, 255), 10)

#     def count(self, im0):
#         """Main counting function to track vehicles and update counts."""
#         if not self.region_initialized:
#             self.initialize_region()
#             self.region_initialized = True

#         self.annotator = Annotator(im0, line_width=self.line_width)
#         self.extract_tracks(im0)
#         self.annotator.draw_region(reg_pts=self.region, color=(104, 0, 123), thickness=self.line_width * 2)

#         for box, track_id, cls in zip(self.boxes, self.track_ids, self.clss):
#             self.store_tracking_history(track_id, box)

#             current_centroid = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
#             prev_position = self.track_history[track_id][-2] if len(self.track_history[track_id]) > 1 else None
#             self.count_objects(current_centroid, track_id, prev_position, cls)
            
#             # Draw bounding box and label
#             # vehicle_type = self.get_vehicle_type(cls)
#             # if vehicle_type:
#             #     color = (0, 255, 0) if vehicle_type == "Four Wheeler" else (0, 0, 255)
#             #     label = f"{vehicle_type} ID {track_id}"
#             #     self.annotator.box_label(box, label, color=color)

#         self.display_counts(im0)
#         return im0




import os
import pandas as pd
from datetime import datetime
import numpy as np
from time import time
from ultralytics.solutions.solutions import BaseSolution
from ultralytics.utils.plotting import Annotator, colors
from shapely.geometry import LineString

class ObjectCounter(BaseSolution):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.in_count = 0
        self.out_count = 0
        self.counted_ids = set()  # Use a set for faster lookups
        self.classwise_counts = {
            "Four Wheeler": {"IN": 0, "OUT": 0},
            "Two Wheeler": {"IN": 0, "OUT": 0}
        }
        self.four_wheeler_classes = {2, 5, 7}  # car, bus, truck
        self.two_wheeler_classes = {3}  # bicycle, motorcycle
        self.region_initialized = False
        self.track_history = {}  # Store centroid history for each track ID
        self.trkd_ids = []
        self.trk_pt = {}
        self.trk_pp = {}

        # Store IN/OUT times for each vehicle
        self.in_out_times = {}  

        # Initialize CSV data storage
        self.csv_filename = self.get_daily_filename()
        self.create_csv()

        # Start time for video processing
        self.start_time = time()  
        
    def get_daily_filename(self):
        """Generate a filename based on the current date."""
        current_date = datetime.now().strftime("%Y-%m-%d")
        return f"vehicle_count_data_{current_date}.csv"

    def create_csv(self):
        """Create the CSV file if it doesn't exist."""
        if not os.path.exists(self.csv_filename):
            header = ["Track ID", "Vehicle Type", "Action", "Date", "Time"]
            df = pd.DataFrame(columns=header)
            df.to_csv(self.csv_filename, index=False)
            print(f"CSV file created: {self.csv_filename}")

    def save_label_to_file(self, track_id, vehicle_type, action):
        """Save the tracking info to CSV."""
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().date()

        # Prepare data for saving
        data = {
            "Track ID": track_id,
            "Vehicle Type": vehicle_type,
            "Action": action,
            "Date": current_date,
            "Time": current_time
        }

        # Append data to CSV
        df = pd.DataFrame([data])
        df.to_csv(self.csv_filename, mode='a', header=False, index=False)
        print(f"Data saved for {vehicle_type} ID {track_id} - {action}")

    def update_in_out_times(self, track_id, action):
        """Update entry and exit times dynamically."""
        timestamp = self.format_time(time() - self.start_time)

        if track_id not in self.in_out_times:
            self.in_out_times[track_id] = {"IN": None, "OUT": None}

        self.in_out_times[track_id][action] = timestamp
        print(f"Vehicle {track_id} {action} at {timestamp}")

    def format_time(self, seconds):
        """Convert seconds to HH:MM:SS format."""
        return str(datetime.utcfromtimestamp(seconds).strftime('%H:%M:%S'))

    def get_vehicle_type(self, class_id):
        """Determine if detected object is Four Wheeler or Two Wheeler."""
        if class_id in self.four_wheeler_classes:
            return "Four Wheeler"
        elif class_id in self.two_wheeler_classes:
            return "Two Wheeler"
        return None

    def count_objects(self, current_centroid, track_id, prev_centroid, cls):
        """Count vehicles based on movement across the defined region."""
        if track_id in self.counted_ids or prev_centroid is None:
            return

        vehicle_type = self.get_vehicle_type(cls)
        if not vehicle_type:
            return  # Ignore non-vehicle classes

        # Define the counting region as a horizontal line
        region_line = LineString(self.region)

        # Create a line representing the vehicle's movement
        movement_line = LineString([prev_centroid, current_centroid])

        # Check if the movement line intersects the region line
        if movement_line.intersects(region_line):
            # Calculate the direction of movement
            direction_vector = np.array(current_centroid) - np.array(prev_centroid)
            angle = np.arctan2(direction_vector[1], direction_vector[0])  # Angle in radians

            # Determine direction based on the angle
            if angle > 0:  # Moving downward (OUT)
                self.classwise_counts[vehicle_type]["OUT"] += 1
                action = "OUT"
            else:  # Moving upward (IN)
                self.classwise_counts[vehicle_type]["IN"] += 1
                action = "IN"

            # Mark the vehicle as counted
            self.counted_ids.add(track_id)
            self.save_label_to_file(track_id, vehicle_type, action)
            self.update_in_out_times(track_id, action)

    def display_counts(self, im0):
        """Display the counts for Four Wheeler and Two Wheeler."""
        labels_dict = {
            key: f"OUT {value['OUT']}  IN {value['IN']}"
            for key, value in self.classwise_counts.items()
            if value["OUT"] > 0 or value["IN"] > 0
        }

        if labels_dict:
            self.annotator.display_analytics(im0, labels_dict, (104, 31, 17), (255, 255, 255), 10)

    def count(self, im0):
        """Main counting function to track vehicles and update counts."""
        if not self.region_initialized:
            self.initialize_region()
            self.region_initialized = True

        self.annotator = Annotator(im0, line_width=self.line_width)
        self.extract_tracks(im0)
        self.annotator.draw_region(reg_pts=self.region, color=(104, 0, 123), thickness=self.line_width * 2)

        for box, track_id, cls in zip(self.boxes, self.track_ids, self.clss):
            current_centroid = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)

            # Update track history
            if track_id not in self.track_history:
                self.track_history[track_id] = []
            self.track_history[track_id].append(current_centroid)

            # Get previous centroid
            prev_centroid = self.track_history[track_id][-2] if len(self.track_history[track_id]) > 1 else None

            # Count objects
            self.count_objects(current_centroid, track_id, prev_centroid, cls)

            # Draw bounding box and label
            # vehicle_type = self.get_vehicle_type(cls)
            # if vehicle_type:
            #     color = (0, 255, 0) if vehicle_type == "Four Wheeler" else (0, 0, 255)
            #     label = f"{vehicle_type} ID {track_id}"
            #     self.annotator.box_label(box, label, color=color)

        self.display_counts(im0)
        return im0
