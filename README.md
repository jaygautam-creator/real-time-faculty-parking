# Real-Time Availability for Faculty Parking 🚗

A smart parking management system prototype that provides **real-time availability** of faculty parking spots. This system processes video footage to detect the status (free or occupied) of parking slots and displays the information on a web interface.

## Features
- **Real-Time Detection**: Uses computer vision to analyze parking spots in video footage.
- **Web Interface**: Displays the availability of parking spots in a grid layout.
- **REST API**: Backend built with Flask to provide parking slot status as JSON data.
- **Customizable Slots**: Easily define parking slot positions through a setup script.

## Technologies Used
- **Python**: Backend processing and computer vision.
- **OpenCV**: For image processing and parking slot detection.
- **Flask**: API and web server.
- **HTML/CSS/JavaScript**: Frontend for displaying parking slot statuses.
- **Pickle**: For storing and retrieving parking slot positions.

## Getting Started

### Prerequisites
1. Python 3.x
2. Pip (Python package manager)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/jaygautam-creator/real-time-faculty-parking.git
   cd real-time-faculty-parking
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your parking lot image (`carParkImg.png`) and video footage (`carPark.mp4`) to the project directory.

4. Define parking slot positions:
   ```bash
   python ParkingSpacePicker.py
   ```

## Usage

1. Start the server:
   ```bash
   python main.py
   ```

2. Open the web interface:
   - Navigate to `http://127.0.0.1:5000` in your web browser.

3. View real-time parking slot availability:
   - Slots are marked as:
     - 🟩 **Green**: Free
     - 🟥 **Red**: Occupied

---

## Folder Structure
```
├── ParkingSpacePicker.py   # Script for defining parking slot positions
├── main.py                 # Flask backend and OpenCV processing
├── templates/
│   └── index.html          # Frontend web interface
├── static/                 # (Optional) Add static assets like images or CSS
├── carParkImg.png          # Parking lot image for slot selection
├── carPark.mp4             # Video footage of the parking lot
└── README.md               # Project documentation
```

---

## API Endpoints

1. **GET `/parking-data`**: Returns the current status of all parking slots in JSON format.
2. **GET `/video-feed`**: Streams the video feed for real-time visualization.

---

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgements
- OpenCV tutorials and documentation.
- Flask community for backend guidance.
