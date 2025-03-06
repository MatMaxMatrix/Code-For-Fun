import cv2
import pytesseract
import numpy as np

# Caricare l'immagine
image = cv2.imread("car.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Applicare la soglia adattiva per migliorare il contrasto
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# Rilevare i bordi e trovare i contorni
edges = cv2.Canny(thresh, 50, 200)
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Identificare le possibili regioni della targa
plate = None
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = w / h
    if 2 < aspect_ratio < 5:  # L'aspetto tipico di una targa
        plate = gray[y:y+h, x:x+w]
        break

if plate is not None:
    text = pytesseract.image_to_string(plate, config="--psm 7")
    print("Targa riconosciuta:", text.strip())
else:
    print("Nessuna targa rilevata.")