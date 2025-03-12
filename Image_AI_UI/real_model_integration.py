import openai

def real_model(self, user_text, image_base64):
    """
    (Interazione con il modello di IA - punto 3)
    Invia il messaggio e, se disponibile, l'immagine (codificata in base64) alle API di OpenAI.
    """
    # Creazione dei messaggi da inviare
    messages = [{
        "role": "system",
        "content": "Sei un assistente molto utile e specializzato in analisi di immagini."
    }]
    # Aggiunge il testo dell'utente
    messages.append({"role": "user", "content": user_text})
    # Se l'immagine è stata caricata, aggiunge il suo contenuto in base64
    if image_base64:
        messages.append({
            "role": "user",
            "content": "Immagine inviata.",
            "image_url": {"url": f"data:image/png;base64,{image_base64}"}
        })
    
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            temperature=0,
            messages=messages
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return f"Error: {str(e)}"