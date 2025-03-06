from paddleocr import PaddleOCR
import cv2

# Inizializzare il modello PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang="en")

# Caricare l'immagine
image_path = "car.jpg"
results = ocr.ocr(image_path, cls=True)

# Elaborare i risultati
for result in results:
    for line in result:
        text, confidence = line[1]
        print(f"Targa riconosciuta: {text}, Affidabilità: {confidence:.2f}")

        if confidence < 0.8:
            print("Attenzione: risultato con bassa affidabilità, revisione manuale consigliata.")