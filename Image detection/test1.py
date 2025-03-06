from ultralytics import YOLO
import cv2
import pytesseract

# Caricare il modello YOLO pre-addestrato per il riconoscimento delle targhe
model = YOLO("yolov8n.pt")  # Assicurati di avere un modello addestrato sulle targhe

# Caricare l'immagine
image = cv2.imread("car.jpg")
results = model(image)
print(type(results))
print(results)

# Elaborare gli oggetti rilevati
for result in results.xyxy[0]:  
    x1, y1, x2, y2, confidence, class_id = result
    if confidence > 0.5:  # Soglia per la rilevazione
        plate = image[int(y1):int(y2), int(x1):int(x2)]
        plate_gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(plate_gray, config="--psm 7")

        print(f"Targa: {text.strip()}, Affidabilità: {confidence:.2f}")

        # Segnalare i risultati con bassa affidabilità
        if confidence < 0.7:
            print("Attenzione: risultato con bassa affidabilità, revisione manuale consigliata.")