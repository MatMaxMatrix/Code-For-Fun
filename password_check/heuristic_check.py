from difflib import SequenceMatcher
from common import suggerimenti, pwd_vietate
from advanced_check import verifica_avanzata

def analisi_euristica(password: str, pwd_vietate: set):
    """
    Metodo Euristico: oltre ai controlli avanzati, confronta la password con quelle comuni usando la similarità.
    """
    adv_check, adv_reason = verifica_avanzata(password, pwd_vietate)
    if not adv_check:
        return False, adv_reason

    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()

    threshold = 0.8  # Soglia: 80% di somiglianza
    for pwd in pwd_vietate:
        if similar(password.lower(), pwd) >= threshold:
            return False, f"Password troppo simile a una password compromessa ('{pwd}')."
    return True, "Password conforme all'analisi euristica."

def analizza_password_euristica(password: str, pwd_vietate: set = pwd_vietate) -> dict:
    """
    Analizza la password applicando il metodo euristico.
    Restituisce un dizionario con l'esito dei controlli.
    """
    # Gestione dei casi limite: password vuote, solo spazi o troppo lunghe
    if not password.strip():
        spiegazione = "Password vuota o composta solo da spazi."
        return {
            "Metodo Base": (False, spiegazione),
            "Metodo Avanzato": (False, spiegazione),
            "Metodo Euristico": (False, spiegazione)
        }
    elif len(password) > 100:  # Gestione di password troppo lunghe
        spiegazione = "Password troppo lunga. Considera di accorciarla."
        return {
            "Metodo Base": (False, spiegazione),
            "Metodo Avanzato": (False, spiegazione),
            "Metodo Euristico": (False, spiegazione)
        }
    
    from basic_check import regole_base
    
    risultato_metodi = {}
    # Metodo Base 
    base_ok, base_msg = regole_base(password)
    risultato_metodi["Metodo Base"] = (base_ok, base_msg)
    
    # Metodo Avanzato 
    adv_ok, adv_msg = verifica_avanzata(password, pwd_vietate)
    risultato_metodi["Metodo Avanzato"] = (adv_ok, adv_msg)
    
    # Metodo Euristico 
    eur_ok, eur_msg = analisi_euristica(password, pwd_vietate)
    risultato_metodi["Metodo Euristico"] = (eur_ok, eur_msg)
    
    return risultato_metodi

if __name__ == "__main__":
    from common import test_passwords
    
    print("Test del metodo euristico di verifica password:")
    print("-" * 50)
    
    for password in test_passwords:
        risultato = analizza_password_euristica(password)
        print(f"Password: {repr(password)}")
        
        for metodo, (esito, messaggio) in risultato.items():
            print(f"{metodo}: {'Sicura' if esito else 'Debole'}")
            print(f"Messaggio: {messaggio}")
        
        print(f"Suggerimenti: {suggerimenti(password, risultato)}")
        print("-" * 50) 