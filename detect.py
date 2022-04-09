
import cv2
import time

# Load the cascade
ear_cascade = cv2.CascadeClassifier('new_cascade.xml')


def check_file_exists(filename):
    try:
        with open(filename) as f:
            return True
    except FileNotFoundError:
        return False


def live_detect():
    # To capture video from webcam.
    cap = cv2.VideoCapture(0)
    while True:
        # Read the frame
        _, img = cap.read()
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = ear_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # Display
        cv2.imshow('img', img)
        # Stop if escape key is pressed
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    # Release the VideoCapture object
    cap.release()


def img_detect():
    # Read the frame
    # _, img = cap.read()
    img_path = input("Enter the image path: ")
    if not check_file_exists(img_path):
        print("File not found")
        return
    img = cv2.imread(img_path)
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Detect the faces
    ears = ear_cascade.detectMultiScale(gray, 1.1, 4)
    # Draw the rectangle around each ear
    print("Found {0} ears!".format(len(ears)))
    for (x, y, w, h) in ears:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    # Display
    output_path = '{0}.jpg'.format(time.time_ns())
    cv2.imwrite(output_path, img)
    print("Saved to {0}".format(output_path))
    # Stop if escape key is pressed


def detect_from_video():
    # To capture video from webcam.
    video_path = input("Enter the video path: ")
    if not check_file_exists(video_path):
        print("File not found")
        return
    cap = cv2.VideoCapture(video_path)

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    size = (frame_width, frame_height)
    output_path = '{0}.avi'.format(time.time_ns())
    result = cv2.VideoWriter(output_path,
                             cv2.VideoWriter_fourcc(*'MJPG'),
                             10, size)
    print("Saving to {0}...".format(output_path))

    fps = cap.get(cv2.CAP_PROP_FPS)
    print("Frame rate: ", int(fps), "FPS")
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count/fps
    print("Duration: ", duration, "seconds")
    total_frames = int(fps * duration)
    total_written_frames = 0
    while cap.isOpened():
        # Read the frame
        ret, img = cap.read()
        if not ret:
            break
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = ear_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # Display
        result.write(img)
        total_written_frames += 1
        print("Written {0}/{1} frames, {2}%".format(total_written_frames, total_frames, int(total_written_frames/total_frames*100)))
    # Release the VideoCapture object
    cap.release()
    result.release()
    print("Saved to {0}".format(output_path))


def choose_mode():
    print("Choose mode:")
    print("1. Live detection")
    print("2. Image detection")
    print("3. Video detection")
    mode = int(input("Enter mode: "))
    if mode == 1:
        live_detect()
    elif mode == 2:
        img_detect()
    elif mode == 3:
        detect_from_video()
    else:
        print("Invalid mode")


if __name__ == '__main__':
    choose_mode()
