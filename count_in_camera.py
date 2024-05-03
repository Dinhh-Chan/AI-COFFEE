from ultralytics import YOLO
from ultralytics.solutions import object_counter
import cv2

# Load the YOLO model
model = YOLO("yolov8n.pt")

# Open the default camera
cap = cv2.VideoCapture(0)
assert cap.isOpened(), "Error opening camera"

# Get video properties - you may need to set these manually if they're not correctly auto-detected
w, h = 640, 480  # Common default webcam resolution, adjust if your cam is different
fps = 30         # Common default, adjust according to your camera specification

# Define region points
region_points = [(0,0)]
# Initialize the video writer
video_writer = cv2.VideoWriter("object_counting_output.avi",
                               cv2.VideoWriter_fourcc(*'XVID'),
                               fps,
                               (w, h))

# Initialize Object Counter
counter = object_counter.ObjectCounter()
counter.set_args(view_img=True,
                 reg_pts=region_points,
                 classes_names=model.names,
                 draw_tracks=True,
                 line_thickness=2)

# Process frames from the camera
while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Failed to capture image from camera.")
        break

    # Track objects in the frame
    tracks = model.track(im0, persist=True, show=False, classes=0)  # If tracking all classes, set classes=None

    # Count objects and write frame to video
    im0 = counter.start_counting(im0, tracks)
    video_writer.write(im0)

# Cleanup
cap.release()
video_writer.release()
cv2.destroyAllWindows()
