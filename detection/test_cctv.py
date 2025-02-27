import cv2

# Replace with your CCTV caera's RTSP or HTTP stream URL
camera_url = "rtsp://admin:admin123@NVR_IP:554/Streaming/Channels/101"

# Open the video stream
cap = cv2.VideoCapture(camera_url)

if not cap.isOpened():
    print("Failed to connect to the camera. Check the URL and network settings.")
else:
    print("Connected successfully. Press 'q' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to retrieve frame.")
            break

        cv2.imshow("CCTV Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break

cap.release()
cv2.destroyAllWindows()
