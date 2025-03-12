from difflib import SequenceMatcher

# Elenco di password da analizzare 
passwords = [
    "Password123!", "qwerty", "SecurePass!2024",
    "admin", "Test1234", "", "aaaaaaa", "     ", "LongPassword123456789!@#"
]
# Set dinamico di password vietate
pwd_vietate = {"qwerty", "admin", "123456", "password", "abc123"}

def regole_base(password: str):
    """
    Metodo Base: controlla se la password ha più di 8 caratteri e varietà di caratteri (almeno una lettera maiuscola, una minuscola, un numero e un simbolo).
    """
    if len(password) < 8:
        return False, "Password troppo corta (minimo 8 caratteri)."
    
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)
    
    if not (has_lower and has_upper and has_digit and has_symbol):
        return False, "La password deve contenere almeno una lettera minuscola, una maiuscola, un numero e un simbolo."
    
    return True, "Password conforme alle regole di base."

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

def analizza_passwords(passwords: list, pwd_vietate: set, livello: int) -> dict:
    """
    Analizza le password applicando uno o più metodi a seconda del livello di sicurezza scelto.  
    Restituisce un dizionario con, per ogni password, l'esito dei controlli applicati.
    """
    risultati = {}
    for password in passwords:
        # gestione dei casi limite: password vuote, solo spazi o troppo lunghe
        if not password.strip():
            spiegazione = "Password vuota o composta solo da spazi."
            risultati[repr(password)] = {
                "Metodo Base": (False, spiegazione),
                "Metodo Avanzato": (False, spiegazione),
                "Metodo Euristico": (False, spiegazione),
            }
            continue
        elif len(password) > 100:  # Gestione di password troppo lunghe
            spiegazione = "Password troppo lunga. Considera di accorciarla."
            risultati[repr(password)] = {
                "Metodo Base": (False, spiegazione),
                "Metodo Avanzato": (False, spiegazione),
                "Metodo Euristico": (False, spiegazione),
            }
            continue
        
        risultato_metodi = {}
        # Metodo Base 
        base_ok, base_msg = regole_base(password)
        risultato_metodi["Metodo Base"] = (base_ok, base_msg)
        
        # Metodo Avanzato 
        if livello >= 2:
            adv_ok, adv_msg = verifica_avanzata(password, pwd_vietate)
            risultato_metodi["Metodo Avanzato"] = (adv_ok, adv_msg)
        
        # Metodo Euristico 
        if livello >= 3:
            eur_ok, eur_msg = analisi_euristica(password, pwd_vietate)
            risultato_metodi["Metodo Euristico"] = (eur_ok, eur_msg)
        
        risultati[repr(password)] = risultato_metodi
    return risultati

def suggerimenti(password: str, risultati_metodo: dict):
    """
    Fornisce suggerimenti per migliorare la password se risultata debole in uno qualsiasi dei metodi applicati.
    """
    suggerimenti_list = []
    if not risultati_metodo.get("Metodo Base", (True, ""))[0]:
        if len(password) < 8:
            suggerimenti_list.append("allunga la password (minimo 8 caratteri)")
        if not any(c.isupper() for c in password):
            suggerimenti_list.append("includi almeno una lettera maiuscola")
        if not any(c.islower() for c in password):
            suggerimenti_list.append("includi almeno una lettera minuscola")
        if not any(c.isdigit() for c in password):
            suggerimenti_list.append("includi almeno un numero")
        if not any(not c.isalnum() for c in password):
            suggerimenti_list.append("includi almeno un simbolo speciale")
    
    if "Metodo Avanzato" in risultati_metodo and not risultati_metodo["Metodo Avanzato"][0]:
        suggerimenti_list.append("Attenzione! La password provata è presente nella lista di password compromesse")
    if "Metodo Euristico" in risultati_metodo and not risultati_metodo["Metodo Euristico"][0]:
        suggerimenti_list.append("Attenzione! Evita password comuni")
    
    return suggerimenti_list if suggerimenti_list else ["Password robusta."]

# Esempio di utilizzo
try:
    livello_input = int(input("Seleziona il livello di sicurezza (1, 2 o 3): "))
    if livello_input not in [1, 2, 3]:
        print("Livello di sicurezza non valido!")
    else:
        risultati = analizza_passwords(passwords, pwd_vietate, livello_input)
        for pwd, result in risultati.items():
            print(f"Analisi per {pwd}:")
            for metodo, (esito, messaggio) in result.items():
                print(f"  {metodo}: {'Sicura' if esito else 'Debole'} - {messaggio}")
            print("\nSuggerimenti: ", suggerimenti(pwd, result))
except ValueError:
    print("Input non valido. Per favore, inserisci un numero intero.")