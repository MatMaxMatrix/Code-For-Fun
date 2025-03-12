from common import suggerimenti

def regole_base(password: str):
    """
    Metodo Base: controlla se la password ha più di 8 caratteri e varietà di caratteri 
    (almeno una lettera maiuscola, una minuscola, un numero e un simbolo).
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

def analizza_password_base(password: str) -> dict:
    """
    Analizza la password applicando il metodo base.
    Restituisce un dizionario con l'esito del controllo.
    """
    # Gestione dei casi limite: password vuote, solo spazi o troppo lunghe
    if not password.strip():
        spiegazione = "Password vuota o composta solo da spazi."
        return {"Metodo Base": (False, spiegazione)}
    elif len(password) > 100:  # Gestione di password troppo lunghe
        spiegazione = "Password troppo lunga. Considera di accorciarla."
        return {"Metodo Base": (False, spiegazione)}
    
    # Metodo Base 
    base_ok, base_msg = regole_base(password)
    return {"Metodo Base": (base_ok, base_msg)}

if __name__ == "__main__":
    from common import test_passwords
    
    print("Test del metodo base di verifica password:")
    print("-" * 50)
    
    for password in test_passwords:
        risultato = analizza_password_base(password)
        print(f"Password: {repr(password)}")
        esito, messaggio = risultato["Metodo Base"]
        print(f"Esito: {'Sicura' if esito else 'Debole'}")
        print(f"Messaggio: {messaggio}")
        print(f"Suggerimenti: {suggerimenti(password, risultato)}")
        print("-" * 50) 