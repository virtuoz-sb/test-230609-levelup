import cv2
import pytesseract

# Set the path to the Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Value of PI for calculations
CV_PI = 3.1415926535897932384626433832795

def preprocess_image(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    denoised = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply adaptive thresholding to create a binary image
    thresholded = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # Deskew the image to straighten any tilted text
    deskewed = deskew(thresholded)

    return deskewed

def deskew(image):
    # Apply Canny edge detection
    edges = cv2.Canny(image, 50, 150, apertureSize=3)

    # Apply Hough line transform to detect lines in the image
    lines = cv2.HoughLines(edges, 1, CV_PI / 180, 200)

    angle = 0.0
    total_angle = 0.0
    total_lines = 0

    if lines is not None:
        # Iterate over the detected lines
        for i in range(len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            total_angle += theta
            total_lines += 1

    if total_lines > 0:
        # Calculate the average angle of the detected lines
        angle = total_angle / total_lines

    # Rotate the image to deskew the text
    rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    return rotated

def extract_text(image_path):
    # Preprocess the image
    preprocessed_image = preprocess_image(image_path)

    # Extract text from the preprocessed image using Tesseract OCR
    extracted_text = pytesseract.image_to_string(preprocessed_image)

    return extracted_text

# Set the path to the input image
image_path = 'scanned_document.jpg'

# Extract text from the image
extracted_text = extract_text(image_path)

# Print the extracted text
print(extracted_text)