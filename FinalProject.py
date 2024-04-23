import cv2
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time

# Function to send email
def send_email(image):
    # Email configuration
    sender_email = "slvrholo@gmail.com"  # Your email address
    receiver_email = "silverintrigear@gmail.com"  # Receiver email address
    password = "wxue tlwt qnle epjf"  # Your email password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Package Detected"

    # Email body
    body = "A package has been detected at " + str(datetime.datetime.now())
    msg.attach(MIMEText(body, 'plain'))

    # Attach image
    img = MIMEImage(image)
    msg.attach(img)

    # Connect to email server and send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()

# Initialize the PiCamera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# Load the Haar cascade for package detection
package_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Allow the camera to warm up
time.sleep(0.1)

# Capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect packages
    packages = package_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the packages and send email notification
    for (x, y, w, h) in packages:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        send_email(cv2.imencode('.jpg', image)[1].tostring())

    # Show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    # Clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # If the 'q' key is pressed, break from the loop
    if key == ord("q"):
        break

# Cleanup
cv2.destroyAllWindows()