
        imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

        checkParkingSpace(imgDilate)
        cv2.waitKey(10)

if __name__ == '__main__':
    import threading
    # Run the video processing in a separate thread
    threading.Thread(target=process_video, daemon=True).start()
    # Start Flask server
    app.run(debug=True)
