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

