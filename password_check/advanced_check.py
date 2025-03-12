from common import suggerimenti, pwd_vietate
from basic_check import regole_base

def verifica_avanzata(password: str, pwd_vietate: set):
    """
    Metodo Avanzato: esegue i controlli di base e verifica se la password è presente nella lista di credenziali vietate.
    """
    base_check, base_reason = regole_base(password)
    if not base_check:
        return False, base_reason
    if password.lower() in pwd_vietate:
        return False, "Password presente nella lista di credenziali compromesse."
    return True, "Password conforme alle regole avanzate."

def analizza_password_avanzata(password: str, pwd_vietate: set = pwd_vietate) -> dict:
    """
    Analizza la password applicando il metodo avanzato.
    Restituisce un dizionario con l'esito dei controlli.
    """
    # Gestione dei casi limite: password vuote, solo spazi o troppo lunghe
    if not password.strip():
        spiegazione = "Password vuota o composta solo da spazi."
        return {
            "Metodo Base": (False, spiegazione),
            "Metodo Avanzato": (False, spiegazione)
        }
    elif len(password) > 100:  # Gestione di password troppo lunghe
        spiegazione = "Password troppo lunga. Considera di accorciarla."
        return {
            "Metodo Base": (False, spiegazione),
            "Metodo Avanzato": (False, spiegazione)
        }
    
    risultato_metodi = {}
    # Metodo Base 
    base_ok, base_msg = regole_base(password)
    risultato_metodi["Metodo Base"] = (base_ok, base_msg)
    
    # Metodo Avanzato 
    adv_ok, adv_msg = verifica_avanzata(password, pwd_vietate)
    risultato_metodi["Metodo Avanzato"] = (adv_ok, adv_msg)
    
    return risultato_metodi

if __name__ == "__main__":
    from common import test_passwords
    
    print("Test del metodo avanzato di verifica password:")
    print("-" * 50)
    
    for password in test_passwords:
        risultato = analizza_password_avanzata(password)
        print(f"Password: {repr(password)}")
        
        for metodo, (esito, messaggio) in risultato.items():
            print(f"{metodo}: {'Sicura' if esito else 'Debole'}")
            print(f"Messaggio: {messaggio}")
        
        print(f"Suggerimenti: {suggerimenti(password, risultato)}")
        print("-" * 50) 