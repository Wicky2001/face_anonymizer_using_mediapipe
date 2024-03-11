import cv2

import mediapipe as mp

mp_face_detection = mp.solutions.face_detection

img = cv2.imread("./img.jpg")

# Open the default webcam (usually index 0)
# if we have other webcam we can specify them as 1,2,3 etc
video = cv2.VideoCapture(0)

# Check if the webcam is opened successfully
if not video.isOpened():
    print("Error: Unable to open webcam.")
    exit()

# Loop to capture and display frames
while True:
    # Read frame from the webcam
    ret, frame = video.read()
    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(img_rgb)
        if results.detections is not None:
            for detection in results.detections:
                # print(detection.location_data.relative_bounding_box)
                relative_bbox = detection.location_data.relative_bounding_box

                H, W, _ = frame.shape
                # WE must multiply the bounding box values by the Width andHeight of the image because here we have relative bounding box
                xmin = int(relative_bbox.xmin * W)
                ymin = int(relative_bbox.ymin * H)
                width = int(relative_bbox.width * W)
                height = int(relative_bbox.height * W)
                """
                frame[ymin:ymin+height]: This specifies the range of rows in the frame matrix that you want to include in 
                the ROI. ymin represents the starting row index, and ymin+height represents the ending row index (exclusive).
                 This effectively defines the height of the ROI.

                   ,: This comma separates the row and column slicing.

                  frame[xmin:xmin+width]: This specifies the range of columns in the frame matrix that you want to include 
                  in the ROI. xmin represents the starting column index, and xmin+width represents the ending column index 
                  (exclusive). This effectively defines the width of the ROI
                """
                # cv2.rectangle(frame, (xmin, ymin), (xmin + width, ymin + width), (0, 255, 0), 1)
                # blur the image
                roi = frame[ymin:ymin + height, xmin:xmin + width]
                frame[ymin:ymin + height, xmin:xmin + width] = cv2.blur(roi, (50, 50))



        # print(results.detections[0].location_data.relative_bounding_box)

    # Check if frame is successfully read
    if not ret:
        print("Error: Unable to read frame.")
        break

    # Display the captured frame
    cv2.imshow("Webcam", frame)

    # Wait for a short delay between frames and check for key press
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

# Release the video capture object and close the window
video.release()
cv2.destroyAllWindows()
