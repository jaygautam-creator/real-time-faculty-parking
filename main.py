# import cv2
# import pickle
# import cvzone
# import numpy as np

# # Video feed
# cap = cv2.VideoCapture('carPark.mp4')

# with open('CarParkPos', 'rb') as f:
#     posList = pickle.load(f)

# width, height = 107, 48


# def checkParkingSpace(imgPro):
#     spaceCounter = 0

#     for pos in posList:
#         x, y = pos

#         imgCrop = imgPro[y:y + height, x:x + width]
#         # cv2.imshow(str(x * y), imgCrop)
#         count = cv2.countNonZero(imgCrop)


#         if count < 900:
#             color = (0, 255, 0)
#             thickness = 5
#             spaceCounter += 1
#         else:
#             color = (0, 0, 255)
#             thickness = 2

#         cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
#         cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
#                            thickness=2, offset=0, colorR=color)

#     cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
#                            thickness=5, offset=20, colorR=(0,200,0))
# while True:

#     if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
#         cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
#     success, img = cap.read()
#     imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
#     imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                          cv2.THRESH_BINARY_INV, 25, 16)
#     imgMedian = cv2.medianBlur(imgThreshold, 5)
#     kernel = np.ones((3, 3), np.uint8)
#     imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

#     checkParkingSpace(imgDilate)
#     cv2.imshow("Image", img)
#     # cv2.imshow("ImageBlur", imgBlur)
#     # cv2.imshow("ImageThres", imgMedian)
#     cv2.waitKey(10)
# 2nd code 
# import cv2
# import pickle
# import cvzone
# import numpy as np
# from flask import Flask, render_template, jsonify, Response

# app = Flask(__name__)

# # Video feed
# cap = cv2.VideoCapture('carPark.mp4')

# # Load parking positions
# with open('CarParkPos', 'rb') as f:
#     posList = pickle.load(f)

# width, height = 107, 48
# parking_status = []


# def checkParkingSpace(imgPro):
#     global parking_status
#     parking_status = []
#     spaceCounter = 0

#     for pos in posList:
#         x, y = pos
#         imgCrop = imgPro[y:y + height, x:x + width]
#         count = cv2.countNonZero(imgCrop)

#         if count < 900:  # Free spot
#             color = (0, 255, 0)
#             thickness = 5
#             status = "free"
#             spaceCounter += 1
#         else:  # Occupied spot
#             color = (0, 0, 255)
#             thickness = 2
#             status = "occupied"

#         parking_status.append({"position": (x, y), "status": status})

#         cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
#         cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
#                            thickness=2, offset=0, colorR=color)

#     cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
#                        thickness=5, offset=20, colorR=(0, 200, 0))


# def generate_frames():
#     while True:
#         if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
#             cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

#         success, img = cap.read()
#         if not success:
#             break

#         imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
#         imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                              cv2.THRESH_BINARY_INV, 25, 16)
#         imgMedian = cv2.medianBlur(imgThreshold, 5)
#         kernel = np.ones((3, 3), np.uint8)
#         imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

#         checkParkingSpace(imgDilate)

#         # Encode the frame as a JPEG and yield it
#         ret, buffer = cv2.imencode('.jpg', img)
#         frame = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# @app.route('/')
# def index():
#     return render_template('index.html')


# @app.route('/parking-data')
# def parking_data():
#     return jsonify(parking_status)


# @app.route('/video-feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# if __name__ == '__main__':
#     app.run(debug=True)

# 3rd code 
# from flask import Flask, jsonify, Response, render_template
# import cv2

# app = Flask(__name__)

# # Example parking slot positions
# # posList = [(100, 150), (200, 250), (300, 350)]  
# posList = [
#     (50, 100), (150, 100), (250, 100), (350, 100), (450, 100),
#     (50, 200), (150, 200), (250, 200), (350, 200), (450, 200),
#     (50, 300), (150, 300), (250, 300), (350, 300), (450, 300),
#     (50, 400), (150, 400), (250, 400), (350, 400), (450, 400),
# ]

# # # Update these with actual positions
# parking_status = []

# # Load video or camera feed
# cap = cv2.VideoCapture('carPark.mp4')

# def process_frame():
#     global parking_status
#     parking_status = []  # Clear previous statuses

#     ret, frame = cap.read()
#     if not ret:
#         return  # No frame to process

#     for pos in posList:
#         # Example crop dimensions (adjust for your parking lot video)
#         x, y, w, h = pos[0], pos[1], 50, 30  # Update w, h as needed
#         imgCrop = frame[y:y+h, x:x+w]

#         # Convert to grayscale and threshold
#         gray = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2GRAY)
#         _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

#         # Count non-zero pixels to determine slot status
#         non_zero_count = cv2.countNonZero(thresh)
#         if non_zero_count > 500:  # Adjust threshold based on your video
#             parking_status.append({"position": pos, "status": "free"})
#         else:
#             parking_status.append({"position": pos, "status": "occupied"})

# @app.route('/')
# def index():
#     return render_template('index.html')  # Ensure you have an `index.html` file in a `templates` folder

# @app.route('/parking-data')
# def parking_data():
#     process_frame()  # Update statuses on each request
#     return jsonify(parking_status)

# @app.route('/video-feed')
# def video_feed():
#     def generate():
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break
#             _, buffer = cv2.imencode('.jpg', frame)
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
#     return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == "__main__":
#     app.run(debug=True)
# 4th code 
# from flask import Flask, jsonify, Response, render_template
# import cv2

# app = Flask(__name__)

# # Example parking slot positions
# # posList should contain coordinates within the frame dimensions of your video
# posList = [
#     {"slot": (1, 1), "coordinates": (50, 100)},
#     {"slot": (1, 2), "coordinates": (150, 100)},
#     {"slot": (1, 3), "coordinates": (250, 100)},
#     {"slot": (1, 4), "coordinates": (350, 100)},
#     {"slot": (1, 5), "coordinates": (450, 100)},
#     {"slot": (2, 1), "coordinates": (50, 200)},
#     {"slot": (2, 2), "coordinates": (150, 200)},
#     {"slot": (2, 3), "coordinates": (250, 200)},
#     {"slot": (2, 4), "coordinates": (350, 200)},
#     {"slot": (2, 5), "coordinates": (450, 200)},
#     {"slot": (3, 1), "coordinates": (50, 300)},
#     {"slot": (3, 2), "coordinates": (150, 300)},
#     {"slot": (3, 3), "coordinates": (250, 300)},
#     {"slot": (3, 4), "coordinates": (350, 300)},
#     {"slot": (3, 5), "coordinates": (450, 300)},
#     {"slot": (4, 1), "coordinates": (50, 400)},
#     {"slot": (4, 2), "coordinates": (150, 400)},
#     {"slot": (4, 3), "coordinates": (250, 400)},
#     {"slot": (4, 4), "coordinates": (350, 400)},
#     {"slot": (4, 5), "coordinates": (450, 400)},
# ]

# # Parking status list
# parking_status = []

# # Load video or camera feed
# cap = cv2.VideoCapture('carPark.mp4')

# def process_frame():
#     """Processes a single frame to determine parking slot statuses."""
#     global parking_status
#     parking_status = []  # Clear previous statuses

#     ret, frame = cap.read()
#     if not ret or frame is None:
#         print("Failed to read video frame.")
#         return  # No frame to process

#     frame_height, frame_width, _ = frame.shape  # Get frame dimensions

#     for slot in posList:
#         x, y = slot["coordinates"]  # Extract coordinates
#         w, h = 100, 50  # Estimated slot width and height

#         # Ensure coordinates are within frame bounds
#         if x < 0 or y < 0 or x + w > frame_width or y + h > frame_height:
#             print(f"Skipping invalid coordinates: {x}, {y}, {w}, {h}")
#             continue

#         # Crop the frame for the slot
#         imgCrop = frame[y:y+h, x:x+w]

#         if imgCrop.size == 0:  # Check if the crop is empty
#             print(f"Empty crop at coordinates: {x}, {y}, {w}, {h}")
#             continue

#         # Convert to grayscale and threshold
#         gray = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2GRAY)
#         _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

#         # Count non-zero pixels to determine slot status
#         non_zero_count = cv2.countNonZero(thresh)
#         if non_zero_count > 500:  # Adjust threshold based on your video
#             parking_status.append({"slot": slot["slot"], "status": "free"})
#         else:
#             parking_status.append({"slot": slot["slot"], "status": "occupied"})

# @app.route('/')
# def index():
#     """Serve the main page."""
#     return render_template('index.html')  # Ensure you have an `index.html` file in a `templates` folder

# @app.route('/parking-data')
# def parking_data():
#     """Return the parking slot statuses as JSON."""
#     process_frame()  # Update statuses on each request
#     return jsonify(parking_status)

# @app.route('/video-feed')
# def video_feed():
#     """Serve the video feed."""
#     def generate():
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break
#             _, buffer = cv2.imencode('.jpg', frame)
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
#     return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == "__main__":
#     app.run(debug=True)
# 5th code 
from flask import Flask, jsonify, Response, render_template
import cv2

app = Flask(__name__)

# Generate parking slot positions (24 slots per row, 12 rows split in two halves)
posList = []
for row in range(1, 13):  # 12 rows
    for col in range(1, 25):  # 24 slots per row
        x = 50 + (col - 1) * 50  # Horizontal position
        y = 50 + (row - 1) * 50  # Vertical position
        posList.append({"slot": (row, col), "coordinates": (x, y)})

# Parking status list
parking_status = []

# Load video or camera feed
cap = cv2.VideoCapture('carPark.mp4')

def process_frame():
    """Processes a single frame to determine parking slot statuses."""
    global parking_status
    parking_status = []  # Clear previous statuses

    ret, frame = cap.read()
    if not ret or frame is None:
        print("Failed to read video frame.")
        return  # No frame to process

    frame_height, frame_width, _ = frame.shape  # Get frame dimensions

    for slot in posList:
        x, y = slot["coordinates"]  # Extract coordinates
        w, h = 40, 40  # Adjusted slot dimensions

        # Ensure coordinates are within frame bounds
        if x < 0 or y < 0 or x + w > frame_width or y + h > frame_height:
            print(f"Skipping invalid coordinates: {x}, {y}, {w}, {h}")
            continue

        # Crop the frame for the slot
        imgCrop = frame[y:y+h, x:x+w]

        if imgCrop.size == 0:  # Check if the crop is empty
            print(f"Empty crop at coordinates: {x}, {y}, {w}, {h}")
            continue

        # Convert to grayscale and threshold
        gray = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # Count non-zero pixels to determine slot status
        non_zero_count = cv2.countNonZero(thresh)
        if non_zero_count > 500:  # Adjust threshold based on your video
            parking_status.append({"slot": slot["slot"], "status": "free"})
        else:
            parking_status.append({"slot": slot["slot"], "status": "occupied"})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parking-data')
def parking_data():
    process_frame()
    return jsonify(parking_status)

@app.route('/video-feed')
def video_feed():
    def generate():
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)

